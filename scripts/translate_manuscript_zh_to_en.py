#!/usr/bin/env python3
"""Translate the Chinese LaTeX manuscript into English with an LLM."""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
API_URL = "https://api.openai.com/v1/chat/completions"
MODEL = os.environ.get("QA_TRANSLATION_MODEL", "gpt-4.1-mini")
API_KEY = os.environ.get("OPENAI_API_KEY")

FILE_MAP = [
    ("frontmatter/zh/preface.tex", "frontmatter/en/preface.tex"),
    ("quickstart/zh/intensity_interferometry.tex", "quickstart/en/intensity_interferometry.tex"),
    *[(f"chapters/zh/chapter_{i:02d}.tex", f"chapters/en/chapter_{i:02d}.tex") for i in range(1, 23)],
    *[(f"appendices/zh/appendix_{letter}.tex", f"appendices/en/appendix_{letter}.tex") for letter in "ABCDEFG"],
]

LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
CITE_RE = re.compile(r"\\cite[tpa]?\*?(?:\[[^\]]*\])?\{([^}]+)\}")
REF_RE = re.compile(r"\\(?:eqref|ref|autoref|cref|Cref)\{([^}]+)\}")
INCLUDE_RE = re.compile(r"\\(?:includegraphics|input)\b")
BEGIN_RE = re.compile(r"\\begin\{([^}]+)\}")
END_RE = re.compile(r"\\end\{([^}]+)\}")

SYSTEM_PROMPT = """You translate a Chinese LaTeX astronomy manuscript into natural English.

Rules:
- Preserve all LaTeX structure and commands.
- Preserve all labels, citation keys, references, macros, math, figure paths, and environment names exactly.
- Translate only the human-readable Chinese prose, including chapter/section titles, captions, table text, and formula-explanation text.
- Do not add commentary.
- Do not summarize, omit, or reorder content.
- Keep units, symbols, and CGS conventions exactly as written in the source.
- Return only valid LaTeX for the translated file."""


def extract_signature(pattern: re.Pattern[str], text: str) -> list[str]:
    found: list[str] = []
    for match in pattern.findall(text):
        if isinstance(match, tuple):
            found.extend([part for part in match if part])
        else:
            found.append(match)
    return found


def check_translation(source: str, translated: str, source_path: str) -> None:
    checks = [
        ("labels", LABEL_RE),
        ("refs", REF_RE),
        ("begins", BEGIN_RE),
        ("ends", END_RE),
    ]
    for name, pattern in checks:
        src = extract_signature(pattern, source)
        dst = extract_signature(pattern, translated)
        if src != dst:
            raise RuntimeError(f"{source_path}: {name} changed during translation")

    src_cites = sorted(set(extract_signature(CITE_RE, source)))
    dst_cites = sorted(set(extract_signature(CITE_RE, translated)))
    if src_cites != dst_cites:
        raise RuntimeError(f"{source_path}: citation keys changed during translation")

    if source.count("\\includegraphics") != translated.count("\\includegraphics"):
        raise RuntimeError(f"{source_path}: includegraphics count changed during translation")
    if source.count("\\input{") != translated.count("\\input{"):
        raise RuntimeError(f"{source_path}: input count changed during translation")


def translate_text(source_path: str, text: str) -> str:
    if not API_KEY:
        raise SystemExit("OPENAI_API_KEY is required")

    payload = {
        "model": MODEL,
        "temperature": 0.1,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Translate the following LaTeX file from Chinese to English.\n"
                    f"Source path: {source_path}\n\n{text}"
                ),
            },
        ],
    }
    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(request, timeout=300) as response:
        data = json.load(response)
    return data["choices"][0]["message"]["content"].strip() + "\n"


def main() -> int:
    failures: list[str] = []
    for source_rel, target_rel in FILE_MAP:
        source_path = ROOT / source_rel
        target_path = ROOT / target_rel
        target_path.parent.mkdir(parents=True, exist_ok=True)

        source_text = source_path.read_text(encoding="utf-8")
        print(f"Translating {source_rel} -> {target_rel}", flush=True)
        try:
            translated = translate_text(source_rel, source_text)
            check_translation(source_text, translated, source_rel)
            target_path.write_text(translated, encoding="utf-8")
        except (RuntimeError, urllib.error.URLError, TimeoutError, KeyError) as exc:
            failures.append(f"{source_rel}: {exc}")
        time.sleep(0.5)

    if failures:
        print("Translation failed for the following files:", file=sys.stderr)
        for item in failures:
            print(f"  - {item}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
