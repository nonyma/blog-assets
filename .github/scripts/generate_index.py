import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
TMP_REVIEW = ROOT / "_tmp-review"
INDEX_FILES = [ROOT / "index.md", ROOT / "index.html"]

header = """---
title: 리류 모음
layout: default
---

<ul>
"""
footer = "</ul>\n"

items = []
for path in sorted(TMP_REVIEW.rglob('*')):
    if path.is_file():
        rel = path.relative_to(TMP_REVIEW)
        url = "{{ '/tmp-review/%s' | relative_url }}" % rel.as_posix()
        items.append(f"  <li><a href=\"{url}\">{rel.name}</a></li>")

content = header + "\n".join(items) + "\n" + footer

for index in INDEX_FILES:
    index.parent.mkdir(parents=True, exist_ok=True)
    if index.suffix == '.html':
        # Strip Jekyll front matter for the HTML copy
        stripped = content.split("---", 2)[2]
        index.write_text(stripped.lstrip(), encoding='utf-8')
    else:
        index.write_text(content, encoding='utf-8')
