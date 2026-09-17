#!/usr/bin/env python3
"""只读扫描前端工程；不读取环境文件、不执行项目脚本、不联网。"""
import argparse
import json
import os
import re
from pathlib import Path

SKIP = {"node_modules", "vendor", "dist", "build", "coverage", "target", "__pycache__"}
FRAMEWORKS = {"react": "react", "next": "react", "vue": "vue", "nuxt": "vue",
              "svelte": "svelte", "@sveltejs/kit": "svelte", "@angular/core": "angular"}
UI_PACKAGES = {"@base-ui/react", "radix-ui", "@radix-ui/react-dialog", "react-aria-components",
               "antd", "@astryxdesign/core", "@lobehub/ui", "@assistant-ui/react", "platejs"}
MOTION_PACKAGES = {"motion", "framer-motion", "gsap", "motion-v"}
ICON_PACKAGES = {"lucide-react", "@phosphor-icons/react", "@heroicons/react", "@tabler/icons-react"}
SOURCE_EXTENSIONS = {".tsx", ".jsx", ".vue", ".svelte", ".templ"}
LOCKS = {"bun.lock", "bun.lockb", "pnpm-lock.yaml", "yarn.lock", "package-lock.json"}


def read_json(path, warnings):
    try:
        if path.stat().st_size > 1_000_000:
            raise ValueError("文件超过扫描大小限制")
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("根节点不是对象")
        return data
    except (OSError, ValueError) as exc:
        warnings.append({"file": str(path.name), "reason": str(exc)})
        return {}


def object_field(data, key, path, warnings):
    value = data.get(key, {})
    if not isinstance(value, dict):
        warnings.append({"file": path, "reason": key + " 不是对象，已跳过"})
        return {}
    return value


def profile(root, max_files=10000, max_depth=7):
    root = Path(root).resolve()
    if not root.is_dir():
        raise ValueError("项目目录不存在")
    if max_files < 1 or max_depth < 0:
        raise ValueError("扫描数量必须为正数，深度不能为负数")
    warnings, packages, components, inventory, styles, locks = [], [], [], [], [], []
    seen = 0
    truncated = False
    for current, dirs, files in os.walk(root, followlinks=False):
        here = Path(current)
        depth = len(here.relative_to(root).parts)
        dirs[:] = sorted(d for d in dirs if not d.startswith('.') and d not in SKIP
                         and not (here / d).is_symlink() and depth < max_depth)
        for name in sorted(files):
            if name.startswith('.'):
                continue
            seen += 1
            if seen > max_files:
                truncated = True
                break
            path = here / name
            if path.is_symlink():
                continue
            relative = path.relative_to(root).as_posix()
            if name == "package.json":
                data = read_json(path, warnings)
                deps = {}
                for key in ("dependencies", "devDependencies", "peerDependencies"):
                    if isinstance(data.get(key), dict):
                        # 仅保留版本声明；不读取 scripts 的命令字符串或 registry 凭证。
                        deps.update({k: (v if re.fullmatch(r"[\w.*^~<>=|+ :/-]+", v)
                                         and "://" not in v else "[非版本引用，请在本地核对]")
                                     for k, v in data[key].items() if isinstance(v, str)})
                packages.append({"manifest": relative, "frameworks": sorted(set(
                    FRAMEWORKS[k] for k in deps if k in FRAMEWORKS)),
                    "dependencies": deps, "package_manager": (
                        data.get("packageManager") if isinstance(data.get("packageManager"), str)
                        and re.fullmatch(r"[\w.@+-]+", data["packageManager"]) else None),
                    "available_checks": sorted(k for k in object_field(data, "scripts", relative, warnings)
                                               if k in {"test", "lint", "build", "typecheck"})})
            elif name == "components.json":
                data = read_json(path, warnings)
                components.append({"file": relative, "style": data.get("style"),
                                   "base": data.get("base"), "rsc": data.get("rsc"),
                                   "icon_library": data.get("iconLibrary"),
                                   "registry_names": sorted(object_field(data, "registries", relative, warnings))})
            elif name in LOCKS:
                locks.append(relative)
            elif path.suffix in SOURCE_EXTENSIONS and len(inventory) < 500:
                inventory.append(relative)
            elif path.suffix == ".css" and name in {"globals.css", "global.css", "theme.css", "tokens.css", "index.css"}:
                try:
                    with path.open(encoding="utf-8") as handle:
                        css = handle.read(262144)
                    styles.append({"file": relative, "token_names": sorted(set(
                        re.findall(r"(--[A-Za-z][\w-]*)\s*:", css)))[:160]})
                except (OSError, UnicodeError):
                    warnings.append({"file": relative, "reason": "无法读取样式文件"})
        if truncated:
            break
    deps = {k: v for package in packages for k, v in package["dependencies"].items()}
    frameworks = set(f for package in packages for f in package["frameworks"])
    if any(path.endswith(".templ") for path in inventory):
        frameworks.add("go-templ")
    return {"schema_version": 1, "root": str(root), "frameworks": sorted(frameworks),
            "packages": packages, "components_configs": components, "lockfiles": locks,
            "ui_packages": sorted(UI_PACKAGES & deps.keys()),
            "motion_packages": sorted(MOTION_PACKAGES & deps.keys()),
            "icon_packages": sorted(ICON_PACKAGES & deps.keys()),
            "component_file_candidates": inventory, "styles": styles,
            "scan": {"files_seen": min(seen, max_files), "truncated": truncated,
                     "max_depth": max_depth, "component_inventory_limit": 500},
            "warnings": warnings,
            "limits": ["文件名只证明可能有组件，不证明接入业务或支持某功能。",
                       "package 版本是声明范围，不是 lockfile 解析后的版本。",
                       "monorepo 的框架合并结果不能代替目标 package 选择。"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project")
    parser.add_argument("--max-files", type=int, default=10000)
    args = parser.parse_args()
    if args.max_files < 1:
        parser.error("--max-files 必须为正数")
    try:
        result = profile(args.project, args.max_files)
    except (ValueError, OSError) as exc:
        parser.exit(2, str(exc) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
