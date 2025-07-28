import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
TMP_REVIEW = ROOT / "_tmp-review"
INDEX_MD = ROOT / "index.md"
INDEX_HTML = ROOT / "index.html"

header = """---
title: 리류 모음
layout: default
---

<ul>
"""
footer = "</ul>\n"

items_md = []
items_html = []
for path in sorted(TMP_REVIEW.rglob('*')):
    if path.is_file():
        rel = path.relative_to(TMP_REVIEW)
        url_md = "{{ '/tmp-review/%s' | relative_url }}" % rel.as_posix()
        url_html = f"tmp-review/{rel.as_posix()}"
        items_md.append(f"  <li><a href=\"{url_md}\">{rel.name}</a></li>")
        items_html.append(f"  <li><a href=\"{url_html}\">{rel.name}</a></li>")

content_md = header + "\n".join(items_md) + "\n" + footer
content_html = "<ul>\n" + "\n".join(items_html) + "\n</ul>\n"

for index, content in [(INDEX_MD, content_md), (INDEX_HTML, content_html)]:
    index.parent.mkdir(parents=True, exist_ok=True)
    index.write_text(content, encoding='utf-8')
