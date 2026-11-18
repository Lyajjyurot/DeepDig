#!/usr/bin/env python3
"""DeepDig 结构与规则校验。

用法：
    python3 scripts/validate_skill.py

退出码 0 表示全部通过，1 表示存在失败项。
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "SKILL.md"

REQUIRED_HEADINGS = ["## 触发", "## 铁律", "## 流程", "## 评级诚实", "## 高频异常", "## 参考"]
REQUIRED_TEMPLATE_MARKERS = ["其他（请说明）", "DECIDED", "RABBIT HOLE", "NO-GO", "贴合度"]
MAX_BODY_LINES = 60
MAX_DESCRIPTION_CHARS = 200
MAX_QUESTIONS = 8

REQUIRED_REPO_FILES = [
    "README.md",
    "LICENSE",
    "CONTRIBUTING.md",
    ".gitattributes",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/feature_request.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/workflows/validate.yml",
]
LINKED_DOCS = ["README.md", "CONTRIBUTING.md"]

results: list[tuple[bool, str]] = []


def check(ok: bool, message: str) -> None:
    results.append((ok, message))


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """返回 (frontmatter 字典, 正文)。仅支持单行 key: "value" 形式。"""
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    raw = text[4:end]
    body = text[end + 4 :].lstrip("\n")
    data: dict[str, str] = {}
    for line in raw.splitlines():
        match = re.match(r'^([A-Za-z0-9_-]+):\s*"(.*)"\s*$', line.strip())
        if match:
            data[match.group(1)] = match.group(2)
    return data, body


def main() -> int:
    if not SKILL.exists():
        print("[FAIL] 缺少 SKILL.md")
        return 1

    text = SKILL.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(text)

    check(bool(meta), "SKILL.md 含合法 frontmatter")
    dir_name = re.sub(r"-(?:main|master)$", "", ROOT.name)
    check(
        meta.get("name", "").lower() == dir_name.lower(),
        f"frontmatter name 与目录名一致（{dir_name}）",
    )
    description = meta.get("description", "")
    check(bool(description), "frontmatter 含 description")
    check(
        len(description) <= MAX_DESCRIPTION_CHARS,
        f"description 不超过 {MAX_DESCRIPTION_CHARS} 字符（当前 {len(description)}）",
    )

    body_lines = [line for line in body.splitlines() if line.strip()]
    check(
        len(body.splitlines()) <= MAX_BODY_LINES,
        f"SKILL.md 正文不超过 {MAX_BODY_LINES} 行（当前 {len(body.splitlines())}）",
    )
    check(len(body_lines) > 0, "SKILL.md 正文非空")

    for heading in REQUIRED_HEADINGS:
        check(heading in body, f"包含章节：{heading}")

    check("DeepDig" in body, "SKILL.md 出现 Skill 名称 DeepDig")
    check("8 问" in body, f"SKILL.md 声明最多 {MAX_QUESTIONS} 问")
    check("DeepDig" in description and "明确" in description, "description 声明仅显式提到 DeepDig 时触发")

    referenced = set(re.findall(r"`((?:references|examples)/[^`]+)`", body))
    for rel in sorted(referenced):
        if rel.endswith("/"):
            check((ROOT / rel).is_dir(), f"引用的目录存在：{rel}")
        else:
            check((ROOT / rel).exists(), f"引用的文件存在：{rel}")

    templates = ROOT / "references" / "templates.md"
    if templates.exists():
        content = templates.read_text(encoding="utf-8")
        for marker in REQUIRED_TEMPLATE_MARKERS:
            check(marker in content, f"templates.md 含要素：{marker}")
    else:
        check(False, "存在 references/templates.md")

    examples = sorted((ROOT / "examples").glob("*.md"))
    check(len(examples) >= 2, f"至少提供 2 个示例（当前 {len(examples)}）")
    for example in examples:
        content = example.read_text(encoding="utf-8")
        questions = len(re.findall(r"^\*\*Q\d+", content, flags=re.MULTILINE))
        fallbacks = content.count("其他（请说明）")
        check(
            questions == 0 or fallbacks >= questions,
            f"{example.name}：{questions} 个问题均有「其他（请说明）」选项",
        )
        check(
            questions <= MAX_QUESTIONS,
            f"{example.name}：问题数不超过 {MAX_QUESTIONS}（当前 {questions}）",
        )

    for rel in REQUIRED_REPO_FILES:
        check((ROOT / rel).exists(), f"开源所需文件存在：{rel}")

    for name in LINKED_DOCS:
        doc = ROOT / name
        if not doc.exists():
            check(False, f"存在文档：{name}")
            continue
        for target in re.findall(r"\]\(([^)\s]+)\)", doc.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            path = target.split("#", 1)[0]
            if path:
                check((doc.parent / path).exists(), f"{name} 相对链接有效：{target}")

    failed = [message for ok, message in results if not ok]
    for ok, message in results:
        print(f"[{'OK' if ok else 'FAIL'}] {message}")

    print()
    if failed:
        print(f"校验未通过：{len(failed)} 项失败")
        return 1
    print(f"校验通过：{len(results)} 项全部满足")
    return 0


if __name__ == "__main__":
    sys.exit(main())
