import re


STYLE = {
    "p": "margin:0 0 1.6em;line-height:1.85;",
    "h3": "font-size:18px;line-height:1.6;font-weight:700;color:#253041;margin:32px 0 14px;",
    "section_blockquote": "margin:46px 0 22px;padding:14px 18px;border-left:5px solid #466a9c;background:#f5f6f8;color:#2f3036;border-radius:8px;",
    "section_p": "margin:0;font-size:21px;line-height:1.5;font-weight:700;color:#2f3036;font-family:'Source Han Serif SC','Noto Serif CJK SC','Songti SC','SimSun',serif;letter-spacing:0.08em;",
    "quote_wrap": "margin:28px 0;border-radius:8px;overflow:hidden;",
    "quote_table": "width:100%;border-collapse:collapse;",
    "quote_bar_td": "width:5px;background:#466a9c;",
    "quote_body_td": "background:#f7f9ff;padding:16px 18px;",
    "quote_p": "margin:0;font-size:17px;line-height:1.75;font-weight:700;color:#263044;",
    "list_p": "margin:0 0 0.9em;line-height:1.75;",
    "ul_marker": "display:inline-block;width:1.15em;color:#466a9c;font-weight:700;vertical-align:top;",
    "ol_marker": "display:inline-block;width:1.8em;color:#466a9c;font-weight:700;vertical-align:top;",
    "strong": "font-weight:800;color:#111827;",
    "a": "color:#466a9c;text-decoration:none;border-bottom:1px solid rgba(70,106,156,0.25);",
    "table": "width:100%;border-collapse:collapse;margin:26px 0 32px;font-size:15px;line-height:1.75;",
    "th": "border:1px solid #c2cdde;padding:10px 12px;text-align:left;background:#f5f6f8;color:#2f3036;font-weight:700;",
    "td": "border:1px solid #c2cdde;padding:10px 12px;text-align:left;color:#374151;",
    "hr": "border:none;height:1px;background:#c2cdde;margin:44px 0;",
    "code_inline": "background:#f3f4f6;color:#374151;padding:2px 6px;border-radius:5px;font-size:0.92em;font-family:'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace;",
}


_re_bold = re.compile(r"\*\*(.+?)\*\*")
_re_highlight = re.compile(r"==(.+?)==")
_re_inline_code = re.compile(r"`([^`]+)`")
_re_md_link = re.compile(r"\[([^\]]+)\]\((https?://[^\s)]+)\)")
_re_url_in_parens = re.compile(r"[(（](https?://[^\s)）]+)[)）]")


def _escape_html(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _inline_format(text: str) -> str:
    text = _escape_html(text)
    text = _re_md_link.sub(r'<a href="\2" style="' + STYLE["a"] + r'">\1</a>', text)
    text = _re_url_in_parens.sub(
        r'（<a href="\1" style="' + STYLE["a"] + r'">\1</a>）', text
    )
    text = _re_inline_code.sub(r'<code style="' + STYLE["code_inline"] + r'">\1</code>', text)
    text = _re_highlight.sub(r'<strong style="' + STYLE["strong"] + r'">\1</strong>', text)
    text = _re_bold.sub(r'<strong style="' + STYLE["strong"] + r'">\1</strong>', text)
    return text


def _render_section_title(text: str) -> str:
    return (
        f'<blockquote style="{STYLE["section_blockquote"]}">'
        f'<p style="{STYLE["section_p"]}">{text}</p>'
        f"</blockquote>"
    )


def _render_quote(text: str) -> str:
    return (
        f'<section style="{STYLE["quote_wrap"]}">'
        f'<table style="{STYLE["quote_table"]}"><tr>'
        f'<td style="{STYLE["quote_bar_td"]}"></td>'
        f'<td style="{STYLE["quote_body_td"]}"><p style="{STYLE["quote_p"]}">{text}</p></td>'
        f"</tr></table>"
        f"</section>"
    )


def _render_ul_item(text: str) -> str:
    return (
        f'<p style="{STYLE["list_p"]}">'
        f'<span style="{STYLE["ul_marker"]}">•</span>'
        f'<span style="display:inline;">{text}</span>'
        f"</p>"
    )


def _render_ol_item(num: str, text: str) -> str:
    marker = f"{num}."
    return (
        f'<p style="{STYLE["list_p"]}">'
        f'<span style="{STYLE["ol_marker"]}">{_escape_html(marker)}</span>'
        f'<span style="display:inline;">{text}</span>'
        f"</p>"
    )


def md_to_wechat_inline_body(md: str) -> str:
    lines = md.splitlines()
    out: list[str] = []

    i = 0
    in_table = False
    table_header: list[str] = []
    table_rows: list[list[str]] = []

    def flush_table():
        nonlocal in_table, table_header, table_rows
        if not in_table:
            return
        out.append(f'<table style="{STYLE["table"]}">')
        if table_header:
            out.append("<thead><tr>")
            for c in table_header:
                out.append(f'<th style="{STYLE["th"]}">{_inline_format(c.strip())}</th>')
            out.append("</tr></thead>")
        out.append("<tbody>")
        for r in table_rows:
            out.append("<tr>")
            for c in r:
                out.append(f'<td style="{STYLE["td"]}">{_inline_format(c.strip())}</td>')
            out.append("</tr>")
        out.append("</tbody></table>")
        in_table = False
        table_header = []
        table_rows = []

    def split_table_row(row: str) -> list[str]:
        row = row.strip()
        if row.startswith("|"):
            row = row[1:]
        if row.endswith("|"):
            row = row[:-1]
        return [c.strip() for c in row.split("|")]

    paragraph_buf: list[str] = []

    def flush_paragraph():
        nonlocal paragraph_buf
        if not paragraph_buf:
            return
        text = " ".join(s.strip() for s in paragraph_buf if s.strip())
        out.append(f'<p style="{STYLE["p"]}">{_inline_format(text)}</p>')
        paragraph_buf = []

    while i < len(lines):
        line = lines[i].rstrip("\n")
        stripped = line.strip()

        if in_table:
            if stripped and "|" in stripped:
                if re.fullmatch(r"[:\-\s|]+", stripped):
                    i += 1
                    continue
                table_rows.append(split_table_row(stripped))
                i += 1
                continue
            flush_table()

        if not stripped:
            flush_paragraph()
            i += 1
            continue

        if re.fullmatch(r"-{3,}|_{3,}|\*{3,}", stripped):
            flush_paragraph()
            out.append(f'<hr style="{STYLE["hr"]}" />')
            i += 1
            continue

        if stripped.startswith(">"):
            flush_paragraph()
            quote_lines: list[str] = []
            while i < len(lines):
                s = lines[i].rstrip("\n").strip()
                if not s.startswith(">"):
                    break
                quote_lines.append(s[1:].lstrip())
                i += 1
            quote_text = _inline_format(" ".join(q.strip() for q in quote_lines if q.strip()))
            out.append(_render_quote(quote_text))
            continue

        if stripped.startswith("#"):
            flush_paragraph()
            level = len(stripped) - len(stripped.lstrip("#"))
            text = _inline_format(stripped[level:].strip())
            if level == 2:
                out.append(_render_section_title(text))
            elif level >= 3:
                out.append(f'<h3 style="{STYLE["h3"]}">{text}</h3>')
            i += 1
            continue

        if "|" in stripped and i + 1 < len(lines) and re.fullmatch(r"[:\-\s|]+", lines[i + 1].strip()):
            flush_paragraph()
            in_table = True
            table_header = split_table_row(stripped)
            table_rows = []
            i += 2
            continue

        m_ol = re.match(r"^(\d+)\.\s+(.*)$", stripped)
        if m_ol:
            flush_paragraph()
            num = m_ol.group(1)
            text = _inline_format(m_ol.group(2))
            out.append(_render_ol_item(num, text))
            i += 1
            continue

        if stripped.startswith("- "):
            flush_paragraph()
            text = _inline_format(stripped[2:].strip())
            out.append(_render_ul_item(text))
            i += 1
            continue

        paragraph_buf.append(stripped)
        i += 1

    flush_paragraph()
    flush_table()
    return "\n  ".join(out).strip()


def render_wechat_inline(md: str, title: str) -> str:
    body = md_to_wechat_inline_body(md)
    safe_title = _inline_format(title)
    return (
        f'<section style="margin:0;padding:24px 0 40px;background:#ffffff;color:#2f3437;font-family:-apple-system,BlinkMacSystemFont,\'PingFang SC\',\'Hiragino Sans GB\',\'Microsoft YaHei\',\'Noto Sans CJK SC\',sans-serif;font-size:17px;line-height:1.85;letter-spacing:0.03em;word-break:break-word;">\n'
        f'  <h1 style="font-size:26px;line-height:1.45;font-weight:700;color:#2f3036;font-family:\'Source Han Serif SC\',\'Noto Serif CJK SC\',\'Songti SC\',\'SimSun\',serif;letter-spacing:0.08em;margin:0 0 28px;">{safe_title}</h1>\n'
        f"  {body}\n"
        f"</section>"
    )
