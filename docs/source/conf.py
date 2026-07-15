from pathlib import Path

project = "Quantum Astronomy"
author = "Yu Wang"
copyright = "2026, Yu Wang"

extensions = [
    "myst_nb",
    "sphinxcontrib.bibtex",
]

source_suffix = {
    ".md": "myst-nb",
}
master_doc = "index"

myst_enable_extensions = [
    "amsmath",
    "attrs_block",
    "attrs_inline",
    "colon_fence",
    "dollarmath",
    "html_image",
]
myst_heading_anchors = 3
nb_execution_mode = "off"
numfig = True
numfig_format = {
    "figure": "Figure %s",
    "table": "Table %s",
    "code-block": "Listing %s",
}

bibtex_bibfiles = ["generated/references_web.bib"]
bibtex_default_style = "plain"
bibtex_reference_style = "author_year"

html_theme = "sphinx_book_theme"
html_title = "Quantum Astronomy"
html_logo = "_static/figures/generated/cover-en.png"
html_favicon = "_static/figures/generated/cover-en.png"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_extra_path = ["CNAME", ".nojekyll"]

html_theme_options = {
    "repository_url": "https://github.com/YWangScience/quantum-astronomy",
    "use_repository_button": True,
    "use_issues_button": True,
    "use_download_button": True,
    "path_to_docs": "docs/source",
    "home_page_in_toc": True,
}

html_context = {
    "default_mode": "light",
}

mathjax3_config = {
    "tex": {
        "macros": {
            "bm": [r"\boldsymbol{#1}", 1],
            "symbf": [r"\mathbf{#1}", 1],
        },
    },
}

exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
]

nitpicky = False

# Keep paths predictable when running the generator or Sphinx from any cwd.
ROOT = Path(__file__).resolve().parents[2]
