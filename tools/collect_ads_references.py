#!/usr/bin/env python3
"""Collect NASA ADS BibTeX references for the quantum astronomy textbook.

The output is intentionally chapter-centric: each chapter receives a rotating
pool of 20--30 ADS bibcodes, while references.bib contains the unique BibTeX
records exported from ADS. The ADS API token must be supplied through the
ADS_API_TOKEN environment variable.
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ADS_API = "https://api.adsabs.harvard.edu/v1"
FIELDS = "bibcode,title,author,year,citation_count,doctype,pub"
ROWS_PER_QUERY = 8
TARGET_PER_CHAPTER = 25
SKIP_BIBCODES = {
    # ADS exports this proceedings author list in a form that BibTeX plainnat
    # cannot parse reliably: "Helmerson, Kristian, Vanderfei Salvador".
    "2005AIPC..770..399J",
}


@dataclass(frozen=True)
class ChapterQuerySet:
    title: str
    queries: tuple[str, ...]


SEED_QUERIES: tuple[str, ...] = (
    'title:"The Quantum Theory of Optical Coherence" author:"Glauber"',
    'title:"Optical Coherence and Quantum Optics" author:"Mandel"',
    'title:"Statistical Optics" author:"Goodman"',
    'title:"A Test of a New Type of Stellar Interferometer on Sirius"',
    'title:"The angular diameters of 32 stars"',
    'title:"Quantum Theory of Superresolution for Two Incoherent Optical Point Sources"',
    'title:"Longer-Baseline Telescopes Using Quantum Repeaters"',
    'title:"Planck 2018 results. VI. Cosmological parameters"',
)


CHAPTER_QUERIES: dict[str, ChapterQuerySet] = {
    "1": ChapterQuerySet(
        "数学和物理基础",
        (
            'title:"optical coherence" OR abs:"optical coherence"',
            'title:"statistical optics" OR abs:"statistical optics"',
            'title:"Fourier optics" OR abs:"Fourier optics"',
            'abs:"Fisher information" abs:astronomy',
        ),
    ),
    "2": ChapterQuerySet(
        "为什么需要量子天文学",
        (
            'title:"intensity interferometry" OR abs:"intensity interferometry"',
            'title:"Hanbury Brown Twiss" OR abs:"Hanbury Brown Twiss"',
            'title:"photon bunching" abs:stars',
            'abs:"photon statistics" abs:astronomy',
        ),
    ),
    "3": ChapterQuerySet(
        "量子光学基础",
        (
            'title:"quantum optics" abs:coherence',
            'title:"photon detection" OR abs:"photoelectric detection"',
            'title:"thermal light" abs:"quantum optics"',
            'title:"squeezed light" OR abs:"squeezed light"',
        ),
    ),
    "4": ChapterQuerySet(
        "光子统计与相干函数",
        (
            'title:"second order coherence" OR abs:"second order coherence"',
            'title:"photon statistics" OR abs:"photon statistics"',
            'title:bunching abs:stars',
            'title:"higher order coherence" OR abs:"higher order coherence"',
        ),
    ),
    "5": ChapterQuerySet(
        "空间相干与强度干涉",
        (
            'title:"stellar intensity interferometry" OR abs:"stellar intensity interferometry"',
            'title:"Cherenkov Telescope Array" abs:"intensity interferometry"',
            'title:VERITAS abs:"intensity interferometry"',
            'title:Narrabri title:"intensity interferometer"',
        ),
    ),
    "6": ChapterQuerySet(
        "探测器、时钟和事件表",
        (
            'title:"single photon detector" OR abs:"single photon detector"',
            'title:"superconducting nanowire" OR abs:"superconducting nanowire"',
            'title:"time tagging" abs:astronomy',
            'title:"White Rabbit" abs:timing',
        ),
    ),
    "7": ChapterQuerySet(
        "事件表的数据分析",
        (
            'title:"photon correlation" abs:astronomy',
            'abs:"Poisson process" abs:astronomy',
            'abs:"Fisher information" abs:interferometry',
            'abs:"intensity interferometry" abs:"data analysis"',
        ),
    ),
    "8": ChapterQuerySet(
        "量子估计、Rayleigh 限制和亚分辨信息",
        (
            'title:"quantum superresolution" OR abs:"quantum superresolution"',
            'title:Rayleigh title:superresolution',
            'title:SPADE OR abs:"spatial mode demultiplexing"',
            'title:"quantum Fisher information" abs:imaging',
        ),
    ),
    "9": ChapterQuerySet(
        "天体辐射机制的量子语言",
        (
            'title:"radiation mechanisms" abs:astrophysics',
            'title:"cyclotron maser" abs:astrophysics',
            'title:"astrophysical maser" OR abs:"astrophysical maser"',
            'abs:"photon statistics" abs:astrophysical',
        ),
    ),
    "10": ChapterQuerySet(
        "恒星作为量子光源",
        (
            'title:"stellar intensity interferometry"',
            'title:"angular diameters" abs:stars abs:interferometry',
            'title:"limb darkening" abs:interferometry',
            'title:Cepheid abs:"Baade-Wesselink"',
        ),
    ),
    "11": ChapterQuerySet(
        "白矮星、中子星和强场物理",
        (
            'title:"neutron star" abs:polarimetry',
            'title:"vacuum birefringence" OR abs:"vacuum birefringence"',
            'title:"Crab pulsar" abs:optical',
            'title:"white dwarf" abs:polarimetry',
        ),
    ),
    "12": ChapterQuerySet(
        "黑洞、吸积盘和 photon ring",
        (
            'title:"Event Horizon Telescope" abs:M87',
            'title:"photon ring" abs:"black hole"',
            'title:"black hole" abs:interferometry',
            'title:"accretion disk" abs:"optical variability"',
        ),
    ),
    "13": ChapterQuerySet(
        "爆发、瞬变和多信使量子天文学",
        (
            'title:"fast radio burst" OR abs:"fast radio burst"',
            'title:"gamma-ray burst" abs:afterglow',
            'title:kilonova abs:GW170817',
            'title:"tidal disruption" abs:event',
        ),
    ),
    "14": ChapterQuerySet(
        "传播效应：等离子体、尘埃和引力透镜",
        (
            'title:"interstellar scattering" OR abs:"interstellar scattering"',
            'title:"Faraday rotation" OR abs:"Faraday rotation"',
            'title:"plasma lensing" OR abs:"plasma lensing"',
            'title:"gravitational lensing" abs:"time delay"',
        ),
    ),
    "15": ChapterQuerySet(
        "暗物质、轴子和偏振量子通道",
        (
            'title:axion abs:polarimetry',
            'title:"cosmic birefringence" OR abs:"cosmic birefringence"',
            'title:"dark matter" abs:lensing',
            'title:"vacuum birefringence" abs:"neutron star"',
        ),
    ),
    "16": ChapterQuerySet(
        "宇宙学中的量子问题",
        (
            'title:"Planck 2018 results"',
            'title:"cosmic microwave background" abs:"blackbody spectrum"',
            'title:"CMB polarization" OR abs:"CMB polarization"',
            'title:"cosmic birefringence" OR abs:"cosmic birefringence"',
        ),
    ),
    "17": ChapterQuerySet(
        "量子网络望远镜",
        (
            'title:"quantum repeaters" abs:telescopes',
            'title:"quantum networks" abs:astronomy',
            'title:"distributed entanglement" abs:imaging',
            'title:"quantum telescopy" OR abs:"quantum telescopy"',
        ),
    ),
    "18": ChapterQuerySet(
        "观测设计、误差预算和可行性计算",
        (
            'title:"intensity interferometry" abs:"signal-to-noise"',
            'title:"Cherenkov Telescope Array" abs:"intensity interferometry"',
            'title:"single photon detector" abs:timing',
            'title:"stellar intensity interferometry"',
        ),
    ),
    "19": ChapterQuerySet(
        "第一代量子天文学科学案例",
        (
            'title:"Type Ia supernova" abs:"intensity interferometry"',
            'title:"angular diameter" abs:"intensity interferometry"',
            'title:"Eta Carinae" abs:laser',
            'title:Cepheid abs:interferometry',
        ),
    ),
    "20": ChapterQuerySet(
        "教学实验和计算实验",
        (
            'title:"teaching quantum optics" OR abs:"teaching quantum optics"',
            'title:"photon counting" abs:experiment',
            'title:"Hanbury Brown Twiss" abs:laboratory',
            'title:"computational imaging" abs:quantum',
        ),
    ),
    "21": ChapterQuerySet(
        "常见误区",
        (
            'title:"Hanbury Brown Twiss" OR abs:"Hanbury Brown Twiss"',
            'title:"intensity interferometry" OR abs:"intensity interferometry"',
            'title:"quantum superresolution" OR abs:"quantum superresolution"',
            'title:"photon statistics" OR abs:"photon statistics"',
        ),
    ),
    "22": ChapterQuerySet(
        "从白皮书到研究计划",
        (
            'title:"intensity interferometry" abs:"white paper"',
            'title:"quantum astronomy" OR abs:"quantum astronomy"',
            'title:"coherence" abs:astrophysics',
            'title:"quantum networks" abs:telescopes',
        ),
    ),
}


def ads_request(token: str, path: str, *, method: str = "GET", params=None, payload=None):
    url = f"{ADS_API}{path}"
    data = None
    headers = {"Authorization": f"Bearer {token}"}
    if params:
        url += "?" + urllib.parse.urlencode(params, doseq=True)
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=90) as response:
        return json.loads(response.read().decode("utf-8"))


def search_ads(token: str, query: str, rows: int = ROWS_PER_QUERY) -> list[dict]:
    params = {
        "q": query,
        "fl": FIELDS,
        "rows": rows,
        "sort": "citation_count desc",
    }
    result = ads_request(token, "/search/query", params=params)
    return result.get("response", {}).get("docs", [])


def export_bibtex(token: str, bibcodes: list[str]) -> str:
    chunks: list[str] = []
    for start in range(0, len(bibcodes), 80):
        chunk = bibcodes[start:start + 80]
        result = ads_request(token, "/export/bibtex", method="POST", payload={"bibcode": chunk})
        chunks.append(result.get("export", "").strip())
        time.sleep(0.25)
    return normalize_bibtex("\n\n".join(part for part in chunks if part).strip()) + "\n"


def normalize_bibtex(text: str) -> str:
    return (
        text
        .replace("\u2010", "-")
        .replace("\u2011", "-")
        .replace("\u2012", "-")
        .replace("\u2013", "--")
        .replace("\u2014", "---")
    )


def compact_title(doc: dict) -> str:
    title = doc.get("title") or []
    if isinstance(title, list):
        return " ".join(title)
    return str(title)


def record_from_doc(doc: dict, query: str, chapter: str | None = None) -> dict:
    return {
        "bibcode": doc.get("bibcode"),
        "title": compact_title(doc),
        "author": doc.get("author") or [],
        "year": doc.get("year"),
        "citation_count": doc.get("citation_count"),
        "doctype": doc.get("doctype"),
        "pub": doc.get("pub"),
        "query": query,
        "chapter": chapter,
    }


def append_unique(items: list[str], bibcode: str | None) -> None:
    if bibcode and bibcode not in SKIP_BIBCODES and bibcode not in items:
        items.append(bibcode)


def main() -> int:
    token = os.environ.get("ADS_API_TOKEN")
    if not token:
        print("Set ADS_API_TOKEN before running.")
        return 2

    metadata = ROOT / "metadata"
    metadata.mkdir(exist_ok=True)

    records: dict[str, dict] = {}
    failures: list[dict] = []
    seed_bibcodes: list[str] = []

    for query in SEED_QUERIES:
        try:
            docs = search_ads(token, query, rows=1)
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as exc:
            failures.append({"scope": "seed", "query": query, "error": str(exc)})
            continue
        if not docs:
            failures.append({"scope": "seed", "query": query, "error": "no ADS result"})
            continue
        rec = record_from_doc(docs[0], query)
        if rec["bibcode"]:
            records[rec["bibcode"]] = rec
            append_unique(seed_bibcodes, rec["bibcode"])
            print(f"seed {rec['bibcode']}: {rec['title']}")
        time.sleep(0.15)

    chapter_map: dict[str, list[str]] = {}
    chapter_records: dict[str, list[dict]] = {}

    for chapter, query_set in CHAPTER_QUERIES.items():
        chapter_bibcodes: list[str] = []
        chapter_docs: list[dict] = []
        for query in query_set.queries:
            try:
                docs = search_ads(token, query)
            except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as exc:
                failures.append({"scope": f"chapter {chapter}", "query": query, "error": str(exc)})
                continue
            if not docs:
                failures.append({"scope": f"chapter {chapter}", "query": query, "error": "no ADS result"})
                continue
            for doc in docs:
                rec = record_from_doc(doc, query, chapter)
                bibcode = rec["bibcode"]
                if not bibcode or bibcode in SKIP_BIBCODES:
                    continue
                records.setdefault(bibcode, rec)
                append_unique(chapter_bibcodes, bibcode)
                chapter_docs.append(rec)
            time.sleep(0.15)

        for bibcode in seed_bibcodes:
            append_unique(chapter_bibcodes, bibcode)

        if len(chapter_bibcodes) < TARGET_PER_CHAPTER:
            for bibcode in records:
                append_unique(chapter_bibcodes, bibcode)
                if len(chapter_bibcodes) >= TARGET_PER_CHAPTER:
                    break

        chapter_map[chapter] = chapter_bibcodes[:TARGET_PER_CHAPTER]
        chapter_records[chapter] = chapter_docs
        print(f"chapter {chapter}: {len(chapter_map[chapter])} references | {query_set.title}")

    all_bibcodes: list[str] = []
    for bibcode in seed_bibcodes:
        append_unique(all_bibcodes, bibcode)
    for chapter in sorted(chapter_map, key=lambda item: int(item)):
        for bibcode in chapter_map[chapter]:
            append_unique(all_bibcodes, bibcode)

    if all_bibcodes:
        (ROOT / "references.bib").write_text(export_bibtex(token, all_bibcodes), encoding="utf-8")

    (metadata / "ads_records.json").write_text(
        json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (metadata / "ads_chapter_records.json").write_text(
        json.dumps(chapter_records, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (metadata / "ads_failures.json").write_text(
        json.dumps(failures, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (metadata / "citation_map.json").write_text(
        json.dumps(chapter_map, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    lines = ["# ADS Citation Report", "", "## Summary", ""]
    lines.append(f"- Unique ADS BibTeX entries exported: {len(all_bibcodes)}")
    lines.append(f"- Target references per chapter: {TARGET_PER_CHAPTER}")
    lines.append("")
    lines.append("## Chapter citation map")
    lines.append("")
    for chapter in sorted(chapter_map, key=lambda item: int(item)):
        title = CHAPTER_QUERIES[chapter].title
        refs = chapter_map[chapter]
        lines.append(f"### Chapter {chapter}: {title}")
        lines.append(f"- References assigned: {len(refs)}")
        for bibcode in refs:
            rec = records.get(bibcode, {})
            title_text = rec.get("title", "")
            year = rec.get("year", "")
            lines.append(f"- `{bibcode}` ({year}) {title_text}")
        lines.append("")
    lines.append("## Search failures")
    lines.append("")
    if failures:
        for failure in failures:
            lines.append(f"- {failure['scope']}: {failure['error']} | query: `{failure['query']}`")
    else:
        lines.append("- None")
    (ROOT / "citation_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Wrote {len(all_bibcodes)} unique BibTeX entries to references.bib")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
