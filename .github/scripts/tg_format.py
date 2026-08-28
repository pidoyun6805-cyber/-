#!/usr/bin/env python3
"""마크다운 브리핑을 텔레그램 HTML 메시지 조각으로 변환한다.

텔레그램은 표를 지원하지 않고 한 통이 4096자로 제한되므로,
표는 라벨 줄로 펴고 굵게/링크만 HTML 태그로 바꾼 뒤 줄 단위로 자른다.
"""
import html
import os
import re
import sys

LIMIT = 3500  # 바이트. 한글 3바이트 기준이라 4096자 제한에 여유가 있다.


def strip_front_matter(text):
    if text.startswith("﻿"):
        text = text[1:]
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4:].lstrip("\n")
    return text


def convert(text):
    out = []
    for raw in text.split("\n"):
        line = raw.rstrip()

        # 표 구분선(|---|---|)은 버린다
        if re.fullmatch(r"\s*\|[\s:|-]+\|\s*", line):
            continue

        # 표 행은 "• 셀 — 셀" 형태로 편다
        if line.startswith("|") and line.endswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            cells = [c for c in cells if c]
            if not cells:
                continue
            line = "• " + "  —  ".join(cells)

        esc = html.escape(line, quote=False)
        esc = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<a href="\2">\1</a>', esc)
        esc = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", esc)

        heading = re.match(r"^(#{1,6})\s+(.*)$", esc)
        if heading:
            esc = "<b>" + heading.group(2) + "</b>"

        out.append(esc)
    return out


def chunk(lines):
    parts, buf = [], ""
    for line in lines:
        candidate = buf + line + "\n"
        if len(candidate.encode("utf-8")) > LIMIT and buf:
            parts.append(buf)
            buf = ""
        buf += line + "\n"
    if buf.strip():
        parts.append(buf)
    return parts


def main():
    with open(sys.argv[1], encoding="utf-8") as fh:
        text = fh.read()
    parts = chunk(convert(strip_front_matter(text)))
    os.makedirs("parts", exist_ok=True)
    for i, part in enumerate(parts, 1):
        with open("parts/%02d.txt" % i, "w", encoding="utf-8") as fh:
            fh.write(part)
    print(len(parts))


if __name__ == "__main__":
    main()
