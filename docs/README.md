# Web Book Build

The GitHub Pages site is generated from the English LaTeX manuscript.

Local build:

```sh
python3 -m venv .venv-docs
. .venv-docs/bin/activate
python -m pip install -r docs/requirements.txt
python scripts/build_sphinx_source.py
sphinx-build -b html docs/source docs/_build/html
```

The generator writes MyST Markdown to `docs/source/generated/` and PNG figures to `docs/source/_static/figures/generated/`. These generated files are ignored by git; GitHub Actions regenerates them before deploying.
