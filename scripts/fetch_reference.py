#!/usr/bin/env python3
"""按来源下载一份官方文本或 registry 到显式路径；不执行内容或修改项目。"""
import argparse
import hashlib
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from recommend import load_catalog


def allowed_hosts(resource):
    return {urllib.parse.urlsplit(resource[key]).hostname
            for key in ("docs", "agent_docs", "llms") if resource.get(key)}


def validate_url(url, hosts):
    parts = urllib.parse.urlsplit(url)
    if (parts.scheme != "https" or parts.hostname not in hosts or parts.username
            or parts.password or parts.port not in (None, 443)):
        raise ValueError("仅允许该来源已记录官方域名的 HTTPS 地址；新域名先人工核验。")


class OfficialRedirect(urllib.request.HTTPRedirectHandler):
    def __init__(self, hosts):
        self.hosts = hosts

    def redirect_request(self, request, fp, code, message, headers, new_url):
        validate_url(new_url, self.hosts)
        if re.search(r"/(?:authentication|login|signin)(?:[/?#]|$)", new_url, re.I):
            raise ValueError("地址跳转到登录页，未取得公开资料。")
        return super().redirect_request(request, fp, code, message, headers, new_url)


def validate_payload(body, content_type, kind):
    try:
        text = body.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValueError("响应不是可用的 UTF-8 文本") from exc
    html = "text/html" in content_type.lower() or bool(re.match(
        r"\s*<(?:!doctype\s+html|html|head|body)(?:\s|>)", text[:4096], re.I))
    if kind != "page" and html:
        raise ValueError("预期结构化或纯文本资料，实际收到 HTML；可能是首页回退或登录页。")
    if not text.strip():
        raise ValueError("响应内容为空")
    if kind in {"json", "registry"}:
        value = json.loads(text)
        if kind == "registry":
            if not isinstance(value, dict) or not isinstance(value.get("files"), list):
                raise ValueError("不是含 files 的 registry item；索引应使用 --kind json。")
            if not value["files"]:
                raise ValueError("registry item 没有源码文件")
            for item in value["files"]:
                if not isinstance(item, dict) or not isinstance(item.get("content"), str):
                    raise ValueError("registry 文件缺少内联文本 content；需另行核对下载方式")
        return {"format": kind, "file_count": len(value["files"]) if kind == "registry" else None}
    return {"format": "html-page" if html else "text"}


def fetch(source, url, kind, output, max_bytes=2_000_000, timeout=15):
    resources, _, _ = load_catalog()
    if source not in resources:
        raise ValueError("未知来源 id")
    resource = resources[source]
    url = url or resource.get("llms")
    if not url:
        raise ValueError("没有已记录的 llms 入口；请从官方页核对 --url。")
    hosts = allowed_hosts(resource)
    validate_url(url, hosts)
    output = Path(output)
    if output.exists() or output.is_symlink():
        raise ValueError("目标已存在，拒绝覆盖；请选择新的任务缓存文件。")
    opener = urllib.request.build_opener(OfficialRedirect(hosts))
    request = urllib.request.Request(url, headers={"User-Agent": "UISift/1.0 ReferenceReader"})
    with opener.open(request, timeout=timeout) as response:
        validate_url(response.url, hosts)
        body = response.read(max_bytes + 1)
        if len(body) > max_bytes:
            raise ValueError("响应超过大小限制，请选用更具体的组件文档。")
        metadata = validate_payload(body, response.headers.get("Content-Type", ""), kind)
        final_url = response.url
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("xb") as handle:
        handle.write(body)
    return {"source": source, "url": final_url, "output": str(output.resolve()),
            "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest(), **metadata,
            "status": "downloaded_unreviewed", "executed": False,
            "next_step": "读取内容并核对版本、许可与依赖；registry 文件尚未安装到项目。"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source")
    parser.add_argument("--url")
    parser.add_argument("--kind", choices=["text", "json", "registry", "page"], default="text")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    try:
        result = fetch(args.source, args.url, args.kind, args.out)
    except (OSError, ValueError, urllib.error.URLError) as exc:
        print(json.dumps({"status": "not_downloaded", "reason": str(exc)}, ensure_ascii=False))
        raise SystemExit(2)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
