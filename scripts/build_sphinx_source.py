#!/usr/bin/env python3
"""Generate the English Sphinx source tree from the LaTeX manuscript."""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS_SOURCE = ROOT / "docs" / "source"
GENERATED = DOCS_SOURCE / "generated"
STATIC_GENERATED = DOCS_SOURCE / "_static" / "figures" / "generated"

PANDOC = shutil.which("pandoc")
PDFTOPPM = shutil.which("pdftoppm")
PANDOC_TARGET = "markdown+tex_math_dollars+pipe_tables-simple_tables-multiline_tables-grid_tables"

SOURCE_FILES = [
    ("frontmatter/en/preface.tex", "preface.md"),
    ("quickstart/en/intensity_interferometry.tex", "quickstart_intensity_interferometry.md"),
    *[(f"chapters/en/chapter_{i:02d}.tex", f"chapter_{i:02d}.md") for i in range(0, 29)],
    *[(f"appendices/en/appendix_{letter}.tex", f"appendix_{letter}.md") for letter in "ABCDEFG"],
]

ENTRY_START_RE = re.compile(r"(?m)^@[A-Za-z]+\s*\{\s*([^,\s]+)\s*,")
LATEX_MACRO_RE = re.compile(r"\\providecommand\{\\([A-Za-z]+)\}\{(.+?)\}")
CITE_GROUP_RE = re.compile(r"\[([^\[\]\n]*@(?:\{|[A-Za-z0-9])[^\[\]\n]*)\]")
CITE_KEY_RE = re.compile(r"@\{([^}]+)\}|@([A-Za-z0-9][A-Za-z0-9.&:+_-]*)")
CITE_ROLE_RE = re.compile(r"\{cite:[pt]\}`([^`]+)`")
EMBED_RE = re.compile(r'<embed src="(figures/generated/[^"]+?)\.pdf"([^>]*)/>')
FIGURE_PATH_RE = re.compile(r'((?:src|href)="|\]\()(figures/generated/[^")]+?)\.pdf')
DISPLAY_EQUATION_RE = re.compile(
    r"\$\$\\begin\{(equation\*?|align\*?|gather\*?|multline\*?)\}\s*(.*?)\s*\\end\{\1\}\$\$",
    re.DOTALL,
)
PLAIN_DISPLAY_MATH_RE = re.compile(r"\$\$\s*(.*?)\s*\$\$", re.DOTALL)
BRACKET_DISPLAY_MATH_RE = re.compile(r"\\\[\s*(.*?)\s*\\\]", re.DOTALL)
HEADING_TARGET_RE = re.compile(r"^(#{1,6})\s+(.+?)\s+\{#([^}]+)\}\s*$", re.MULTILINE)
PANDOC_BRACKET_REF_RE = re.compile(
    r"\[\\\[([^\]]+)\\\]\]\(#[^)]+\)\{reference-type=\"(eqref|ref)\" reference=\"([^\"]+)\"\}"
)
PANDOC_NUMBERED_REF_RE = re.compile(
    r"\[([^\]]+)\]\(#([^)]+)\)\{reference-type=\"ref\" reference=\"([^\"]+)\"\}"
)
PANDOC_ATTR_REF_RE = re.compile(
    r"\[((?:\\\[[^\]]+\\\])|(?:[^\]\n]+))\]\(#([^)]+)\)\{([^}]*\breference-type\s*=\s*['\"]?(?:eqref|ref)['\"]?[^}]*)\}"
)
HTML_PANDOC_REF_RE = re.compile(
    r"<a\s+([^>]*\bdata-reference-type\s*=\s*['\"]?(?:eqref|ref)['\"]?[^>]*)>.*?</a>",
    re.DOTALL,
)
REFERENCE_TYPE_ATTR_RE = re.compile(r"\breference-type\s*=\s*['\"]?(eqref|ref)['\"]?")
REFERENCE_ATTR_RE = re.compile(r"\breference\s*=\s*['\"]?([^'\"\s}>]+)['\"]?")
DATA_REFERENCE_TYPE_ATTR_RE = re.compile(r"\bdata-reference-type\s*=\s*['\"]?(eqref|ref)['\"]?")
DATA_REFERENCE_ATTR_RE = re.compile(r"\bdata-reference\s*=\s*['\"]?([^'\"\s}>]+)['\"]?")
HTML_MATH_SPAN_RE = re.compile(r'<span class="math inline">(.+?)</span>')
CHAPTER_OPENING_RE = re.compile(r"^(:{3,}) (?:chapteropening|\{\.chapteropening\})\s*$", re.MULTILINE)
HTML_FIGURE_RE = re.compile(
    r'<figure id="([^"]+)"[^>]*>\s*<img\s+([^>]*?)\s*/>\s*<figcaption>(.*?)</figcaption>\s*</figure>',
    re.DOTALL,
)
PANDOC_TABLE_RE = re.compile(
    r"(?m)(?P<table>^(?:\|.*\|\n)+)\n?:\s+(?P<caption>.+?)\s+\{#(?P<label>tab:[^}]+)\}\s*$"
)
PANDOC_DIV_TABLE_RE = re.compile(
    r"(?m)^:::\s+\{#(?P<label>tab:[^}]+)\}\s*\n"
    r"(?P<table>(?:\|.*\|\n)+)\n?"
    r":\s+(?P<caption>.+?)\s*\n:::\s*$"
)
IMG_SRC_RE = re.compile(r'src="([^"]+)"')
IMG_WIDTH_RE = re.compile(r'width:\s*([0-9.]+)%')


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, cwd=ROOT, check=True)


def clean_generated_dirs() -> None:
    shutil.rmtree(GENERATED, ignore_errors=True)
    shutil.rmtree(STATIC_GENERATED, ignore_errors=True)
    GENERATED.mkdir(parents=True, exist_ok=True)
    STATIC_GENERATED.mkdir(parents=True, exist_ok=True)


def convert_figures() -> None:
    if PDFTOPPM is None:
        raise SystemExit("pdftoppm is required to render PDF figures to PNG.")

    source_root = ROOT / "figures" / "generated"
    for source in sorted(source_root.rglob("*")):
        if not source.is_file():
            continue

        rel = source.relative_to(source_root)
        if source.suffix.lower() == ".pdf":
            target = (STATIC_GENERATED / rel).with_suffix(".png")
            target.parent.mkdir(parents=True, exist_ok=True)
            run([
                PDFTOPPM,
                "-png",
                "-singlefile",
                "-r",
                "180",
                str(source),
                str(target.with_suffix("")),
            ])
        elif source.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
            target = STATIC_GENERATED / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)


def bib_entries_by_key(bib: str) -> dict[str, str]:
    matches = list(ENTRY_START_RE.finditer(bib))
    entries: dict[str, str] = {}
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(bib)
        entries[match.group(1).strip()] = bib[start:end].strip()
    return entries


def cited_keys_from_generated_markdown() -> list[str]:
    keys: list[str] = []
    for path in sorted(GENERATED.glob("*.md")):
        if path.name == "bibliography.md":
            continue
        text = path.read_text(encoding="utf-8")
        for match in CITE_ROLE_RE.finditer(text):
            for key in match.group(1).split(","):
                key = key.strip()
                if key and key not in keys:
                    keys.append(key)
    return keys


def clean_web_bibtex(bib: str) -> str:
    bib = bib.replace("{Takahashi}, H., and {Takahashi}", "{Takahashi}, H. and {Takahashi}")
    bib = bib.replace("{Thompson}, Tibaldo, L., D. J", "{Thompson}, D.~J. and {Tibaldo}, L.")
    bib = re.sub(r"\\ensuremath\{([^{}]+)\}", r"\1", bib)
    return bib


def make_web_bib() -> None:
    macros: dict[str, str] = {}
    macro_source = (ROOT / "shared" / "ads_journal_macros.tex").read_text(encoding="utf-8")
    for name, value in LATEX_MACRO_RE.findall(macro_source):
        value = value.replace(r"\&", "&")
        value = value.replace(r"\ensuremath{^\circ}", "deg")
        macros[name] = value
    macros.update({
        "textdegree": "deg",
        "textregistered": "(R)",
    })

    source_bib = (ROOT / "references.bib").read_text(encoding="utf-8")
    entries = bib_entries_by_key(source_bib)
    cited_keys = cited_keys_from_generated_markdown()
    selected_entries: list[str] = []
    missing_keys: list[str] = []
    for key in cited_keys:
        entry = entries.get(key)
        if entry is None:
            missing_keys.append(key)
            continue
        selected_entries.append(entry)

    bib = "\n\n".join(selected_entries) + "\n"
    for name, value in sorted(macros.items(), key=lambda item: len(item[0]), reverse=True):
        bib = bib.replace("{\\" + name + "}", "{" + value + "}")
        bib = bib.replace("\\" + name, value)
    bib = clean_web_bibtex(bib)

    (GENERATED / "references_web.bib").write_text(bib, encoding="utf-8")
    print(f"Selected {len(selected_entries)} cited references for the web bibliography.")
    if missing_keys:
        print("Missing bibliography keys: " + ", ".join(missing_keys))



def pandoc_convert(source: Path) -> str:
    if PANDOC is None:
        raise SystemExit("pandoc is required to generate MyST Markdown.")

    completed = subprocess.run(
        [
            PANDOC,
            str(source),
            "-f",
            "latex",
            "-t",
            PANDOC_TARGET,
            "--wrap=none",
        ],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    return completed.stdout


def citation_keys(raw: str) -> list[str]:
    keys: list[str] = []
    for braced, bare in CITE_KEY_RE.findall(raw):
        key = braced or bare
        if key not in keys:
            keys.append(key)
    return keys


def replace_citation_groups(markdown: str) -> str:
    def group_repl(match: re.Match[str]) -> str:
        keys = citation_keys(match.group(1))
        if not keys:
            return match.group(0)
        return "{cite:p}`" + ",".join(keys) + "`"

    markdown = CITE_GROUP_RE.sub(group_repl, markdown)
    markdown = re.sub(
        r"@\{([^}]+)\}",
        lambda match: "{cite:t}`" + match.group(1) + "`",
        markdown,
    )
    markdown = re.sub(
        r"(?<![\w`])@([0-9][A-Za-z0-9.&:+_-]*)",
        lambda match: "{cite:t}`" + match.group(1) + "`",
        markdown,
    )
    return markdown


def replace_pdf_figures(markdown: str) -> str:
    def embed_repl(match: re.Match[str]) -> str:
        png_rel = Path(match.group(1)).with_suffix(".png")
        image_src = "../_static/" + png_rel.as_posix()
        return f'<img src="{image_src}"{match.group(2)}/>'

    markdown = EMBED_RE.sub(embed_repl, markdown)
    markdown = FIGURE_PATH_RE.sub(
        lambda match: match.group(1) + "../_static/" + Path(match.group(2)).with_suffix(".png").as_posix(),
        markdown,
    )
    markdown = markdown.replace('src="figures/generated/cover-en.png"', 'src="../_static/figures/generated/cover-en.png"')
    return markdown


def replace_heading_targets(markdown: str) -> str:
    def heading_repl(match: re.Match[str]) -> str:
        level, title, target = match.groups()
        return f"({target})=\n{level} {title}"

    return HEADING_TARGET_RE.sub(heading_repl, markdown)


def replace_html_figures(markdown: str) -> str:
    def figure_repl(match: re.Match[str]) -> str:
        figure_id, image_attrs, caption = match.groups()
        src_match = IMG_SRC_RE.search(image_attrs)
        if src_match is None:
            return match.group(0)

        width_match = IMG_WIDTH_RE.search(image_attrs)
        width_option = f":width: {width_match.group(1)}%\n" if width_match else ""
        caption = caption.strip()
        return (
            f"\n\n```{{figure}} {src_match.group(1)}\n"
            f":name: {figure_id}\n"
            f"{width_option}\n"
            f"{caption}\n"
            "```\n\n"
        )

    return HTML_FIGURE_RE.sub(figure_repl, markdown)


def replace_pandoc_tables(markdown: str) -> str:
    """Turn labelled Pandoc pipe tables into numbered MyST table directives."""

    def table_repl(match: re.Match[str]) -> str:
        table = match.group("table").rstrip()
        caption = match.group("caption").strip()
        label = match.group("label")
        return (
            f"\n\n:::{{table}} {caption}\n"
            f":name: {label}\n\n"
            f"{table}\n"
            ":::\n"
        )

    markdown = PANDOC_DIV_TABLE_RE.sub(table_repl, markdown)
    return PANDOC_TABLE_RE.sub(table_repl, markdown)


def replace_display_equations(markdown: str) -> str:
    def math_directive(body: str, environment: str | None = None) -> str:
        label_match = re.search(r"\\label\{([^}]+)\}", body)
        label = label_match.group(1) if label_match else None
        body = re.sub(r"\s*\\label\{[^}]+\}", "", body).strip()
        if environment and not environment.startswith("equation"):
            body = f"\\begin{{{environment}}}\n{body}\n\\end{{{environment}}}"

        options = f":label: {label}\n" if label else ""
        return f"\n\n```{{math}}\n{options}{body}\n```\n\n"

    def equation_repl(match: re.Match[str]) -> str:
        environment, body = match.groups()
        return math_directive(body, environment)

    markdown = DISPLAY_EQUATION_RE.sub(equation_repl, markdown)
    markdown = PLAIN_DISPLAY_MATH_RE.sub(lambda match: math_directive(match.group(1)), markdown)
    markdown = BRACKET_DISPLAY_MATH_RE.sub(lambda match: math_directive(match.group(1)), markdown)
    return markdown


def replace_pandoc_refs(markdown: str) -> str:
    def reference_role(reference_type: str, reference: str) -> str:
        if reference_type == "eqref" or reference.startswith("eq:"):
            return f"{{eq}}`{reference}`"
        if reference.startswith(("fig:", "tab:")):
            return f"{{numref}}`{reference}`"
        return f"{{ref}}`{reference}`"

    def bracket_repl(match: re.Match[str]) -> str:
        _display, reference_type, reference = match.groups()
        return reference_role(reference_type, reference)

    def html_repl(match: re.Match[str]) -> str:
        attrs = match.group(1)
        reference_type_match = DATA_REFERENCE_TYPE_ATTR_RE.search(attrs)
        reference_match = DATA_REFERENCE_ATTR_RE.search(attrs)
        if reference_type_match is None or reference_match is None:
            return match.group(0)
        reference_type = reference_type_match.group(1)
        reference = reference_match.group(1)
        return reference_role(reference_type, reference)

    def attr_repl(match: re.Match[str]) -> str:
        _display, target, attrs = match.groups()
        reference_type_match = REFERENCE_TYPE_ATTR_RE.search(attrs)
        reference_match = REFERENCE_ATTR_RE.search(attrs)
        if reference_type_match is None:
            return match.group(0)
        reference_type = reference_type_match.group(1)
        reference = reference_match.group(1) if reference_match else target
        return reference_role(reference_type, reference)

    markdown = HTML_PANDOC_REF_RE.sub(html_repl, markdown)
    markdown = PANDOC_ATTR_REF_RE.sub(attr_repl, markdown)
    markdown = PANDOC_BRACKET_REF_RE.sub(bracket_repl, markdown)
    def numbered_repl(match: re.Match[str]) -> str:
        _display, _html_target, reference = match.groups()
        return reference_role("ref", reference)

    markdown = PANDOC_NUMBERED_REF_RE.sub(numbered_repl, markdown)
    return markdown


def clean_html_math_spans(markdown: str) -> str:
    def span_repl(match: re.Match[str]) -> str:
        content = match.group(1)
        if content.startswith("$") and content.endswith("$"):
            return content
        return match.group(0)

    return HTML_MATH_SPAN_RE.sub(span_repl, markdown)


def replace_chapter_openings(markdown: str) -> str:
    return CHAPTER_OPENING_RE.sub(
        lambda match: f"{match.group(1)}{{admonition}} Chapter opening\n:class: chapter-opening",
        markdown,
    )


def polish_markdown(markdown: str) -> str:
    markdown = replace_chapter_openings(markdown)
    markdown = markdown.replace("::: flushright\nYu Wang\\\nJuly 2026\n:::", '<div class="signature">Yu Wang<br>July 2026</div>')
    markdown = replace_citation_groups(markdown)
    markdown = replace_pdf_figures(markdown)
    markdown = replace_heading_targets(markdown)
    markdown = replace_html_figures(markdown)
    markdown = replace_pandoc_tables(markdown)
    markdown = replace_pandoc_refs(markdown)
    markdown = replace_display_equations(markdown)
    markdown = clean_html_math_spans(markdown)
    return markdown.strip() + "\n"


def convert_sources() -> None:
    for source_name, target_name in SOURCE_FILES:
        source = ROOT / source_name
        target = GENERATED / target_name
        markdown = polish_markdown(pandoc_convert(source))
        target.write_text(markdown, encoding="utf-8")

    (GENERATED / "bibliography.md").write_text(
        "# Bibliography\n\n```{bibliography}\n:style: plain\n```\n",
        encoding="utf-8",
    )


def main() -> None:
    clean_generated_dirs()
    convert_figures()
    convert_sources()
    make_web_bib()
    print(f"Generated Sphinx source in {GENERATED.relative_to(ROOT)}")
    print(f"Generated PNG figures in {STATIC_GENERATED.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
