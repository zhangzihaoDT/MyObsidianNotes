import re


_re_bold = re.compile(r"\*\*(.+?)\*\*")
_re_highlight = re.compile(r"==(.+?)==")
_re_inline_code = re.compile(r"`([^`]+)`")
_re_md_link = re.compile(r"\[([^\]]+)\]\((https?://[^\s)]+)\)")
_re_url_in_parens = re.compile(r"[(（](https?://[^\s)）]+)[)）]")


def _read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _extract_style_block(skill_md_path: str) -> str:
    raw = _read_text(skill_md_path)
    start = raw.find("<style>")
    end = raw.find("</style>", start)
    if start == -1 or end == -1:
        raise RuntimeError("SKILL.md 未找到 <style>...</style> 模板")
    return raw[start : end + len("</style>")].strip()


def _escape_html(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _inline_format(text: str) -> str:
    text = _escape_html(text)
    text = _re_md_link.sub(r'<a href="\2">\1</a>', text)
    text = _re_url_in_parens.sub(r'（<a href="\1">\1</a>）', text)
    text = _re_inline_code.sub(r"<code>\1</code>", text)
    text = _re_highlight.sub(r"<strong>\1</strong>", text)
    text = _re_bold.sub(r"<strong>\1</strong>", text)
    return text


def _is_pull_quote(raw_lines: list[str], prev_non_empty_line: str = "") -> bool:
    non_empty = [line.strip() for line in raw_lines if line.strip()]
    if len(non_empty) != 1:
        return False
    plain = re.sub(r"[*_`=#>\[\]\(\)!-]", "", non_empty[0]).strip()
    if len(plain) <= 28:
        return True
    if prev_non_empty_line.rstrip().endswith(("：", ":")) and len(plain) <= 72:
        return True
    return False


def _render_quote(raw_lines: list[str], prev_non_empty_line: str = "") -> list[str]:
    quote_text = _inline_format(" ".join(q.strip() for q in raw_lines if q.strip()))
    if _is_pull_quote(raw_lines, prev_non_empty_line):
        return [f'<p class="pull-quote">{quote_text}</p>']
    return ["<blockquote>", f"  <p>{quote_text}</p>", "</blockquote>"]


def _flatten_vertical_flow(lines: list[str]) -> str | None:
    non_empty = [line.strip() for line in lines if line.strip()]
    if len(non_empty) < 3 or len(non_empty) % 2 == 0:
        return None
    arrow_pattern = re.compile(r"^[↓⇣⇩⭣]+$")
    nodes: list[str] = []
    for idx, part in enumerate(non_empty):
        if idx % 2 == 0:
            nodes.append(part)
            continue
        if not arrow_pattern.fullmatch(part):
            return None
    return " → ".join(nodes)


def _render_code_block(lines: list[str]) -> list[str]:
    flow_text = _flatten_vertical_flow(lines)
    if flow_text:
        return [f"<pre><code>{_escape_html(flow_text)}</code></pre>"]
    code = _escape_html("\n".join(lines)).strip("\n")
    return [f"<pre><code>{code}</code></pre>"]


def md_to_preview_body(md: str) -> str:
    lines = md.splitlines()
    out: list[str] = []

    i = 0
    in_ul = False
    in_ol = False
    in_table = False
    table_header: list[str] = []
    table_rows: list[list[str]] = []

    def prev_non_empty_line(before_index: int) -> str:
        j = before_index - 1
        while j >= 0:
            candidate = lines[j].strip()
            if candidate:
                return candidate
            j -= 1
        return ""

    def close_lists():
        nonlocal in_ul, in_ol
        if in_ul:
            out.append("</ul>")
            in_ul = False
        if in_ol:
            out.append("</ol>")
            in_ol = False

    def flush_table():
        nonlocal in_table, table_header, table_rows
        if not in_table:
            return
        out.append("<table>")
        if table_header:
            out.append("<thead><tr>")
            for c in table_header:
                out.append(f"<th>{_inline_format(c.strip())}</th>")
            out.append("</tr></thead>")
        out.append("<tbody>")
        for r in table_rows:
            out.append("<tr>")
            for c in r:
                out.append(f"<td>{_inline_format(c.strip())}</td>")
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
        out.append(f"<p>{_inline_format(text)}</p>")
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
            close_lists()
            i += 1
            continue

        if re.fullmatch(r"-{3,}|_{3,}|\*{3,}", stripped):
            flush_paragraph()
            close_lists()
            out.append("<hr />")
            i += 1
            continue

        if stripped.startswith("```"):
            flush_paragraph()
            close_lists()
            code_lines: list[str] = []
            i += 1
            while i < len(lines):
                current = lines[i].rstrip("\n")
                if current.strip().startswith("```"):
                    i += 1
                    break
                code_lines.append(current)
                i += 1
            out.extend(_render_code_block(code_lines))
            continue

        if stripped.startswith(">"):
            flush_paragraph()
            close_lists()
            quote_lines: list[str] = []
            prev_line = prev_non_empty_line(i)
            while i < len(lines):
                s = lines[i].rstrip("\n").strip()
                if not s.startswith(">"):
                    break
                quote_lines.append(s[1:].lstrip())
                i += 1
            out.extend(_render_quote(quote_lines, prev_line))
            continue

        if stripped.startswith("#"):
            flush_paragraph()
            close_lists()
            level = len(stripped) - len(stripped.lstrip("#"))
            text = _inline_format(stripped[level:].strip())
            if level == 1:
                out.append(f"<h1>{text}</h1>")
            elif level == 2:
                out.append(f"<h2>{text}</h2>")
            else:
                out.append(f"<h3>{text}</h3>")
            i += 1
            continue

        if "|" in stripped and i + 1 < len(lines) and re.fullmatch(r"[:\-\s|]+", lines[i + 1].strip()):
            flush_paragraph()
            close_lists()
            in_table = True
            table_header = split_table_row(stripped)
            table_rows = []
            i += 2
            continue

        m_ol = re.match(r"^(\d+)\.\s+(.*)$", stripped)
        if m_ol:
            flush_paragraph()
            if in_ul:
                out.append("</ul>")
                in_ul = False
            if not in_ol:
                out.append("<ol>")
                in_ol = True
            out.append(f"<li>{_inline_format(m_ol.group(2))}</li>")
            i += 1
            continue

        if stripped.startswith("- "):
            flush_paragraph()
            if in_ol:
                out.append("</ol>")
                in_ol = False
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{_inline_format(stripped[2:].strip())}</li>")
            i += 1
            continue

        paragraph_buf.append(stripped)
        i += 1

    flush_paragraph()
    close_lists()
    flush_table()
    return "\n  ".join(out).strip()


def render_preview(md: str, title: str, skill_md_path: str) -> str:
    style = _extract_style_block(skill_md_path)
    body = md_to_preview_body(md)
    safe_title = _inline_format(title)
    return f'{style}\n\n<section class="zihaology-essay">\n  <h1>{safe_title}</h1>\n  {body}\n</section>'
