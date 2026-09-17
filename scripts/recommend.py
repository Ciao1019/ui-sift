#!/usr/bin/env python3
"""离线候选检索：框架硬过滤、意图匹配、解释排序；不执行安装。"""
import argparse
import json
import re
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
FRAMEWORK_ALIASES = {"next": "react", "nextjs": "react", "nuxt": "vue", "templ": "go-templ"}


def load_catalog():
    resources = json.loads((DATA / "resources.json").read_text(encoding="utf-8"))["resources"]
    components = json.loads((DATA / "components.json").read_text(encoding="utf-8"))["components"]
    intents = json.loads((DATA / "intents.json").read_text(encoding="utf-8"))["intents"]
    return {r["id"]: r for r in resources}, components, intents


def term_mentions(query, term):
    """返回每次明确词语提及是否处于局部否定中；不做完整语义解析。"""
    query = query.casefold()
    pattern = re.escape(term.casefold())
    if term.isascii():
        pattern = r"(?<![a-z0-9])" + pattern + r"(?![a-z0-9])"
    result = []
    for match in re.finditer(pattern, query):
        prefix = re.split(r"[,，。;；!?！？\n]", query[:match.start()])[-1]
        negated = re.search(r"(?:不需要|不要|无需|不用|禁止|不做|\bwithout\b|\bno\b|\bnot\b|\bavoid\b)[^,，。;；]{0,18}$", prefix)
        result.append(bool(negated))
    return result


def find_intents(query, definitions):
    found = []
    for intent in definitions:
        if any(False in term_mentions(query, term) for term in intent["terms"]):
            found.append(intent["id"])
    return found


def recommend(query, framework="unknown", intents=None, profile_data=None, limit=5,
              no_new_dependencies=False, motion=1):
    resources, components, definitions = load_catalog()
    profile_data = {} if profile_data is None else profile_data
    if not isinstance(profile_data, dict):
        raise ValueError("profile 根节点必须是对象")
    if not isinstance(profile_data.get("packages", []), list) or any(
            not isinstance(p, dict) or not isinstance(p.get("dependencies", {}), dict)
            for p in profile_data.get("packages", [])):
        raise ValueError("profile packages 必须为含 dependencies 对象的数组")
    framework = FRAMEWORK_ALIASES.get(framework, framework)
    if framework == "auto":
        frameworks = profile_data.get("frameworks", [])
        if not isinstance(frameworks, list) or len(frameworks) != 1 or not isinstance(frameworks[0], str):
            raise ValueError("自动框架判断不唯一：请指定目标 package 或 --framework。")
        framework = frameworks[0]
    valid = {"react", "vue", "angular", "svelte", "go-templ", "html", "unknown"}
    if framework not in valid:
        raise ValueError("不支持的框架；可使用 unknown 并人工核对。")
    selected = list(dict.fromkeys(intents if intents is not None else find_intents(query, definitions)))
    unknown = set(selected) - {i["id"] for i in definitions}
    if unknown:
        raise ValueError("未知 intent: " + ", ".join(sorted(unknown)))
    installed = {name for package in profile_data.get("packages", [])
                 for name in package.get("dependencies", {})}
    candidates, exclusions = [], []
    for component in components:
        resource = resources[component["source"]]
        matched = sorted(set(selected) & set(component["intents"]))
        mentions = [negative for term in (resource["id"], resource["name"])
                    for negative in term_mentions(query, term)]
        named = False in mentions
        if mentions and all(mentions):
            exclusions.append({"id": component["id"], "reason": "来源被明确排除"})
            continue
        if not matched and not named:
            continue
        compatible = framework == "unknown" or framework in resource["frameworks"]
        inspiration = resource["frameworks"] == ["inspiration"]
        if not compatible and not inspiration:
            exclusions.append({"id": component["id"], "reason": "框架不兼容",
                               "frameworks": resource["frameworks"]})
            continue
        if component["motion"] > motion:
            exclusions.append({"id": component["id"], "reason": "超出本次动效强度"})
            continue
        reused_packages = sorted(installed & set(resource["packages"]))
        specific = [term for term in component.get("query_terms", [])
                    if False in term_mentions(query, term)]
        score = 10 * len(matched) + (3 if named else 0) + (2 if reused_packages else 0)
        score += 4 if specific else 0
        score -= component["integration_cost"]
        if inspiration:
            score -= 6
        reason = ["意图匹配: " + ", ".join(matched)] if matched else ["名称命中，仍需确认具体用途"]
        if specific:
            reason.append("具体能力匹配: " + ", ".join(specific))
        if reused_packages:
            reason.append("存在相关包声明: " + ", ".join(reused_packages))
        candidates.append({"id": component["id"], "source": resource["id"],
                           "name": component["name"], "score": score, "reasons": reason,
                           "use": "inspiration_only" if inspiration or no_new_dependencies else "candidate",
                           "docs": resource["docs"], "caution": resource["caution"],
                           "agent_docs": resource["agent_docs"], "skill_status": resource["skill_status"],
                           "mcp_kind": resource["mcp_kind"], "mcp_endpoint": resource["mcp_endpoint"],
                           "api_verified": False, "install_command": None})
    candidates.sort(key=lambda c: (-c["score"], c["id"]))
    return {"schema_version": 1, "query": query, "framework": framework, "intents": selected,
            "mode": "reuse_or_local_implementation" if no_new_dependencies else "shortlist",
            "candidates": candidates[:limit], "excluded": exclusions,
            "next_step": "先搜索本地实现与调用，再读取入选项的官方文档并核对许可和依赖。",
            "limits": ["分数只解释关键词排序，不衡量美观、质量或生产可用性。",
                       "不理解全部自然语言否定与复杂约束；可用 --intent 明确意图。",
                       "未联网确认当前 API，不生成猜测的安装命令。",
                       "无匹配意味着目录覆盖不足，不代表市场上不存在方案。"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query")
    parser.add_argument("--framework", default="unknown")
    parser.add_argument("--intent", action="append")
    parser.add_argument("--profile")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--motion", type=int, choices=[0, 1, 2], default=1)
    parser.add_argument("--no-new-dependencies", action="store_true")
    args = parser.parse_args()
    if not 1 <= args.limit <= 25:
        parser.error("--limit 需在 1 至 25 之间")
    try:
        profile_data = json.loads(Path(args.profile).read_text(encoding="utf-8")) if args.profile else None
        result = recommend(args.query, args.framework, args.intent, profile_data,
                           args.limit, args.no_new_dependencies, args.motion)
    except (OSError, ValueError, TypeError) as exc:
        parser.exit(2, str(exc) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
