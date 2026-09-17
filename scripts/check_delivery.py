#!/usr/bin/env python3
"""检查验收记录是否完整；只核对证据引用，不自动判定界面好看或测试为真。"""
import argparse
import json
from pathlib import Path

STATES = {"pass", "fail", "unverified", "not-applicable"}


def check(report, evidence_root):
    root = Path(evidence_root).resolve()
    issues, unverified, failed = [], [], []
    if not isinstance(report, dict):
        return {"status": "invalid", "issues": ["报告根节点必须是对象"],
                "failed_checks": [], "unverified_checks": []}
    if report.get("schema_version") != 1:
        issues.append("schema_version 必须为 1")
    requirements = report.get("requirements")
    checks = report.get("checks")
    if not isinstance(requirements, list) or not requirements:
        issues.append("必须声明至少一个来自用户任务的验收要求")
        requirements = []
    if not isinstance(checks, list) or not checks:
        issues.append("必须有实际检查项")
        checks = []
    raw_ids = [r.get("id") for r in requirements if isinstance(r, dict)]
    ids = [i for i in raw_ids if isinstance(i, str) and i.strip()]
    if len(ids) != len(requirements) or len(set(ids)) != len(ids):
        issues.append("requirement id 必须非空且唯一")
    covered, relevant, seen = set(), set(), set()
    for entry in checks:
        if not isinstance(entry, dict):
            issues.append("检查项必须为对象")
            continue
        identifier = entry.get("id")
        if not isinstance(identifier, str) or not identifier.strip() or identifier in seen:
            issues.append("check id 必须非空且唯一")
        seen.add(str(identifier))
        reqs = entry.get("requirements", [])
        if not isinstance(reqs, list) or any(not isinstance(r, str) for r in reqs):
            issues.append(f"{identifier}: requirements 必须为字符串数组")
            continue
        if not reqs or set(reqs) - set(ids):
            issues.append(f"{identifier}: 引用的 requirement 不存在或为空")
        covered.update(reqs)
        state = entry.get("status")
        if state != "not-applicable":
            relevant.update(reqs)
        if not isinstance(state, str) or state not in STATES:
            issues.append(f"{identifier}: 未知检查状态")
        if state == "fail":
            failed.append(identifier)
        if state == "unverified":
            unverified.append(identifier)
        if not isinstance(entry.get("observation"), str) or not entry["observation"].strip():
            issues.append(f"{identifier}: 缺少实际观察或无法验证的原因")
        evidence = entry.get("evidence", [])
        if not isinstance(evidence, list) or any(not isinstance(e, str) for e in evidence):
            issues.append(f"{identifier}: evidence 必须为路径数组")
            continue
        if state == "pass" and not evidence:
            issues.append(f"{identifier}: pass 没有证据文件引用")
        for name in evidence:
            try:
                path = (root / name).resolve()
                usable = path.is_relative_to(root) and path.is_file() and path.stat().st_size > 0
            except (OSError, ValueError, RuntimeError):
                usable = False
            if not usable:
                issues.append(f"{identifier}: 证据不存在、为空或超出 evidence root: {name}")
    if set(ids) - covered:
        issues.append("未覆盖要求: " + ", ".join(sorted(set(ids) - covered)))
    required = {r["id"] for r in requirements if isinstance(r, dict)
                and isinstance(r.get("id"), str) and r.get("required", True)}
    if required - relevant:
        issues.append("必需要求不能全部标为 not-applicable: " + ", ".join(sorted(required - relevant)))
    state = "invalid" if issues else "has_failures" if failed else "incomplete" if unverified else "evidence_record_complete"
    return {"status": state, "issues": issues, "failed_checks": failed,
            "unverified_checks": unverified,
            "limit": "记录完整不等于产品验收通过；Agent 仍需读取证据、复核内容与实际主流程。"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report")
    parser.add_argument("--evidence-root", required=True)
    args = parser.parse_args()
    try:
        report = json.loads(Path(args.report).read_text(encoding="utf-8"))
        if not isinstance(report, dict):
            raise ValueError("报告根节点必须是对象")
        result = check(report, args.evidence_root)
    except (OSError, ValueError, TypeError) as exc:
        parser.exit(2, str(exc) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["status"] == "evidence_record_complete" else 2)


if __name__ == "__main__":
    main()
