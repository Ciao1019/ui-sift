"""从 skills.sh 的公开索引更新安装量徽章，不收集用户数据或发送安装事件。"""
import argparse
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path


def find_install_count(payload, repository, skill):
    if not isinstance(payload, dict) or not isinstance(payload.get("skills"), list):
        raise ValueError("skills.sh 响应缺少 skills 数组")
    expected_id = (repository + "/" + skill).casefold()
    matches = []
    for item in payload["skills"]:
        if not isinstance(item, dict):
            raise ValueError("skills.sh 返回了无效的索引项")
        if str(item.get("id", "")).casefold() != expected_id:
            continue
        if str(item.get("source", "")).casefold() != repository.casefold():
            raise ValueError("目标记录的来源与仓库不一致")
        count = item.get("installs")
        if isinstance(count, bool) or not isinstance(count, int) or count < 0:
            raise ValueError("安装次数必须为非负整数")
        matches.append(count)
    if len(matches) > 1:
        raise ValueError("目标 skill 出现重复统计记录")
    return matches[0] if matches else None


def fetch_install_count(repository, skill):
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
        raise ValueError("repository 应为 owner/repo")
    params = urllib.parse.urlencode({
        "q": skill, "owner": repository.split("/")[0], "limit": 100,
    })
    request = urllib.request.Request(
        "https://skills.sh/api/search?" + params,
        headers={"User-Agent": "UI-Sift-Install-Stats/1.0", "Accept": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        body = response.read(1_000_001)
    if len(body) > 1_000_000:
        raise ValueError("索引响应超过大小限制")
    return find_install_count(json.loads(body.decode("utf-8")), repository, skill)


def write_badge(output, count):
    if count is not None and (isinstance(count, bool) or not isinstance(count, int) or count < 0):
        raise ValueError("安装次数必须为非负整数或 None")
    badge = {
        "schemaVersion": 1,
        "label": "npx installs",
        "message": "pending" if count is None else str(count),
        "color": "lightgrey" if count is None else "18181b",
        "cacheSeconds": 300,
    }
    text = json.dumps(badge, indent=2) + "\n"
    output = Path(output)
    if output.exists() and output.read_text(encoding="utf-8") == text:
        return False
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")
    return True


def update(repository, skill, output):
    # 网络或解析失败会直接报错，保留上一次有效记录，不能写成零次。
    count = fetch_install_count(repository, skill)
    changed = write_badge(output, count)
    return {"status": "pending" if count is None else "available",
            "tracked_installs": count, "changed": changed}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--skill", default="ui-sift")
    parser.add_argument("--output", default=".github/badges/installs.json")
    args = parser.parse_args()
    try:
        result = update(args.repository, args.skill, args.output)
    except (OSError, ValueError) as exc:
        parser.exit(1, str(exc) + "\n")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
