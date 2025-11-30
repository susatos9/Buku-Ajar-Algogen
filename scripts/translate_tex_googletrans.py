#!/usr/bin/env python3
"""Translate LaTeX chapter files to Indonesian using googletrans.

This script is conservative: it preserves LaTeX commands, math ($...$, $$...$$),
citations (\cite{...}), labels, and environments such as tikzpicture, align,
equation, lstlisting, and verbatim. It translates:
- chapter/section/subsection titles (the text inside braces)
- captions (the text inside \caption{...})
- paragraph text (lines not starting with '\\' and outside skipped envs)
- \item text following a \item

It writes translated files back into the same directory, making a .bak backup
for each file before overwriting.

Usage: python3 scripts/translate_tex_googletrans.py
"""

import re
import sys
from pathlib import Path

try:
    from googletrans import Translator
except Exception as e:
    print("googletrans not available. Install with: pip install googletrans==4.0.0-rc1")
    raise


SKIP_ENVS = {
    'tikzpicture', 'axis', 'lstlisting', 'verbatim', 'algorithmic', 'algorithm',
    'align', 'equation', 'tikzpicture', 'picture', 'table', 'figure'
}

TEX_DIR = Path('latex-book/chapters_id')


def placeholderize(text):
    """Replace math and citations with placeholders and return mapping."""
    placeholders = {}
    i = 0

    # replace display math $$...$$
    def repl_display(m):
        nonlocal i
        key = f"__MATHD_{i}__"
        placeholders[key] = m.group(0)
        i += 1
        return key

    text = re.sub(r"\$\$.*?\$\$", repl_display, text, flags=re.S)

    # replace inline math $...$
    def repl_inline(m):
        nonlocal i
        key = f"__MATH_{i}__"
        placeholders[key] = m.group(0)
        i += 1
        return key

    text = re.sub(r"\$(?:[^$\\]|\\.)*\$", repl_inline, text)

    # replace \cite{...}
    def repl_cite(m):
        nonlocal i
        key = f"__CITE_{i}__"
        placeholders[key] = m.group(0)
        i += 1
        return key

    text = re.sub(r"\\cite\{[^}]*\}", repl_cite, text)

    return text, placeholders


def restore_placeholders(text, placeholders):
    for k, v in placeholders.items():
        text = text.replace(k, v)
    return text


def translate_text(translator, text):
    if not text.strip():
        return text
    # googletrans may choke on very long inputs; translate paragraph-by-paragraph
    try:
        res = translator.translate(text, dest='id')
        return res.text
    except Exception as e:
        print('Translation error:', e)
        return text


def process_file(path: Path, translator: Translator):
    print('Processing', path)
    bak = path.with_suffix(path.suffix + '.bak')
    if not bak.exists():
        bak.write_bytes(path.read_bytes())

    lines = path.read_text(encoding='utf-8').splitlines()
    out_lines = []
    in_skip_env = None
    paragraph = []

    def flush_paragraph():
        nonlocal paragraph
        if not paragraph:
            return
        block = '\n'.join(paragraph).strip()
        if block:
            text_with_ph, placeholders = placeholderize(block)
            translated = translate_text(translator, text_with_ph)
            translated = restore_placeholders(translated, placeholders)
            out_lines.extend(translated.splitlines())
        else:
            out_lines.extend(paragraph)
        paragraph = []

    for line in lines:
        stripped = line.strip()
        # begin environment?
        m_begin = re.match(r"\\begin\{(\w+)\}", stripped)
        if m_begin:
            env = m_begin.group(1)
            if env in SKIP_ENVS:
                flush_paragraph()
                in_skip_env = env
                out_lines.append(line)
                continue

        m_end = re.match(r"\\end\{(\w+)\}", stripped)
        if m_end and in_skip_env:
            env = m_end.group(1)
            out_lines.append(line)
            in_skip_env = None
            continue

        if in_skip_env:
            # inside skip env: but translate \caption{...} in figure/table
            if in_skip_env in ('figure', 'table'):
                cap = re.match(r"(.*\\caption)\{(.*)\}(.*)", line)
                if cap:
                    pre, inner, post = cap.group(1), cap.group(2), cap.group(3)
                    txt, placeholders = placeholderize(inner)
                    tr = translate_text(translator, txt)
                    tr = restore_placeholders(tr, placeholders)
                    out_lines.append(f"{pre}{{{tr}}}{post}")
                else:
                    out_lines.append(line)
            else:
                out_lines.append(line)
            continue

        # headings and chapter/section-like commands: translate {...}
        cmd_match = re.match(r"(\\(?:chapter|section|subsection|subsubsection|paragraph|title|author))\{(.*)\}", stripped)
        if cmd_match:
            cmd, inner = cmd_match.group(1), cmd_match.group(2)
            txt, placeholders = placeholderize(inner)
            tr = translate_text(translator, txt)
            tr = restore_placeholders(tr, placeholders)
            out_lines.append(re.sub(r"\{.*\}", '{' + tr + '}', line, count=1))
            continue

        # caption outside environments
        cap_match = re.match(r"(.*\\caption)\{(.*)\}(.*)", line)
        if cap_match:
            pre, inner, post = cap_match.group(1), cap_match.group(2), cap_match.group(3)
            txt, placeholders = placeholderize(inner)
            tr = translate_text(translator, txt)
            tr = restore_placeholders(tr, placeholders)
            out_lines.append(f"{pre}{{{tr}}}{post}")
            continue

        # items
        item_match = re.match(r"(\\item)(.*)", line)
        if item_match and not stripped.startswith('%'):
            pre, rest = item_match.group(1), item_match.group(2)
            if rest.strip():
                txt, placeholders = placeholderize(rest)
                tr = translate_text(translator, txt)
                tr = restore_placeholders(tr, placeholders)
                out_lines.append(pre + tr)
            else:
                out_lines.append(line)
            continue

        # comments or commands => flush paragraph and copy
        if stripped.startswith('%') or stripped.startswith('\\') or stripped == '':
            flush_paragraph()
            out_lines.append(line)
            continue

        # otherwise part of a paragraph: accumulate
        paragraph.append(line)

    flush_paragraph()

    path.write_text('\n'.join(out_lines) + '\n', encoding='utf-8')


def main():
    translator = Translator()
    files = sorted(TEX_DIR.glob('*.tex'))
    if not files:
        print('No files found in', TEX_DIR)
        return
    for f in files:
        process_file(f, translator)

    # git add/commit
    try:
        import subprocess
        subprocess.run(['git', 'add', str(TEX_DIR)], check=False)
        subprocess.run(['git', 'commit', '-m', 'i18n: machine-translate chapters to Indonesian (draft)'], check=False)
    except Exception:
        pass


if __name__ == '__main__':
    main()
