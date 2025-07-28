import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
TMP_REVIEW = ROOT / "_tmp-review"
INDEX_MD = ROOT / "index.md"
INDEX_HTML = ROOT / "index.html"


def build_tree() -> dict:
    tree: dict = {}
    for path in sorted(TMP_REVIEW.rglob("*")):
        if path.is_file():
            parts = path.relative_to(TMP_REVIEW).parts
            node = tree
            for part in parts[:-1]:
                node = node.setdefault(part, {})
            node.setdefault("__files", []).append(path.relative_to(TMP_REVIEW))
    return tree


def render(node: dict, indent: str = "  ") -> tuple[list[str], list[str]]:
    md_lines: list[str] = []
    html_lines: list[str] = []

    for d in sorted(k for k in node.keys() if k != "__files"):
        md_lines.append(f"{indent}<li>{d}")
        md_lines.append(f"{indent}  <ul>")
        html_lines.append(f"{indent}<li>{d}")
        html_lines.append(f"{indent}  <ul>")
        sub_md, sub_html = render(node[d], indent + "  ")
        md_lines.extend(sub_md)
        html_lines.extend(sub_html)
        md_lines.append(f"{indent}  </ul></li>")
        html_lines.append(f"{indent}  </ul></li>")

    for rel in sorted(node.get("__files", [])):
        url_md = "{{ '/tmp-review/%s' | relative_url }}" % rel.as_posix()
        url_html = f"tmp-review/{rel.as_posix()}"
        md_lines.append(f"{indent}<li><a href=\"{url_md}\">{rel.name}</a></li>")
        html_lines.append(f"{indent}<li><a href=\"{url_html}\">{rel.name}</a></li>")

    return md_lines, html_lines


header = """---
title: 리류 모음
layout: default
---

<ul>\n"""

footer = "</ul>\n"

tree = build_tree()
md_body, html_body = render(tree)

content_md = header + "\n".join(md_body) + "\n" + footer
content_html = "<ul>\n" + "\n".join(html_body) + "\n</ul>\n"

for index, content in ((INDEX_MD, content_md), (INDEX_HTML, content_html)):
    index.parent.mkdir(parents=True, exist_ok=True)
    index.write_text(content, encoding="utf-8")
