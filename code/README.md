# Chapter Plotting Code

This directory contains one Python plotting script per chapter.

Run one chapter:

```bash
python code/chapter_01.py
```

Run all chapters:

```bash
for f in code/chapter_*.py; do python "$f"; done
```

Each chapter script may generate more than one figure. The current catalog
contains 55 generated figures. Output is written to:

```text
figures/generated/chapter_XX/
```

The default numerical values are teaching values for scaling and interpretation.
Replace them with instrument, catalog, or paper-specific values before treating
a plot as a research result.
