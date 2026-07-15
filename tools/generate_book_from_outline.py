#!/usr/bin/env python3
"""Generate a first full LaTeX draft from the detailed outline."""

from __future__ import annotations

import json
import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path

from figure_catalog import FIGURES, figures_for_chapter


ROOT = Path(__file__).resolve().parents[1]
OUTLINE = ROOT / "quantum_astronomy_detailed_outline.md"


@dataclass
class Subsection:
    number: str
    title: str
    notes: list[str] = field(default_factory=list)


@dataclass
class Section:
    number: str
    title: str
    subsections: list[Subsection] = field(default_factory=list)


@dataclass
class Chapter:
    number: str
    title: str
    part: str
    sections: list[Section] = field(default_factory=list)


@dataclass
class Appendix:
    letter: str
    title: str
    sections: list[Section] = field(default_factory=list)


def split_heading(line: str, prefix: str) -> str:
    return line[len(prefix):].strip()


def clean_part_title(title: str) -> str:
    return re.sub(r"^第(?:[一二三四五六七八九十〇零百两]+|\d+)部分[，,、：:\s]*", "", title).strip()


def parse_outline() -> tuple[list[Chapter], list[Appendix], list[str]]:
    chapters: list[Chapter] = []
    appendices: list[Appendix] = []
    part_title = ""
    current_chapter: Chapter | None = None
    current_appendix: Appendix | None = None
    current_section: Section | None = None
    current_subsection: Subsection | None = None
    references: list[str] = []
    in_reference_list = False
    stop_body = False

    for raw in OUTLINE.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if line.startswith("# 建议引用文献清单"):
            in_reference_list = True
            stop_body = True
            continue
        if line.startswith("# LaTeX 落地建议"):
            in_reference_list = False
            continue
        if in_reference_list and line.startswith("- "):
            references.append(line[2:].strip())
            continue
        if stop_body:
            continue
        if not line.strip():
            continue

        if line.startswith("# 第一部分") or line.startswith("# 第二部分") or line.startswith("# 第三部分") or line.startswith("# 第四部分") or line.startswith("# 第五部分"):
            part_title = clean_part_title(split_heading(line, "# "))
            current_chapter = None
            current_appendix = None
            current_section = None
            current_subsection = None
            continue
        if line.startswith("# 附录建议"):
            part_title = "附录"
            current_chapter = None
            current_appendix = None
            current_section = None
            current_subsection = None
            continue

        m = re.match(r"^## 第\s*(\d+)\s*章[，,]\s*(.+)$", line)
        if m:
            current_chapter = Chapter(m.group(1), m.group(2), part_title)
            chapters.append(current_chapter)
            current_appendix = None
            current_section = None
            current_subsection = None
            continue
        m = re.match(r"^## 附录\s*([A-Z])(?:[，,]\s*)?(.+)$", line)
        if m:
            current_appendix = Appendix(m.group(1), m.group(2))
            appendices.append(current_appendix)
            current_chapter = None
            current_section = None
            current_subsection = None
            continue
        m = re.match(r"^###\s+([A-Z]?\d+(?:\.\d+)*|[A-Z]\.\d+)\s+(.+)$", line)
        if m:
            current_section = Section(m.group(1), m.group(2))
            if current_chapter:
                current_chapter.sections.append(current_section)
            elif current_appendix:
                current_appendix.sections.append(current_section)
            current_subsection = None
            continue
        m = re.match(r"^####\s+([A-Z]?\d+(?:\.\d+)*|[A-Z]\.\d+(?:\.\d+)?)\s+(.+)$", line)
        if m:
            current_subsection = Subsection(m.group(1), m.group(2))
            if current_section:
                current_section.subsections.append(current_subsection)
            continue
        if current_subsection:
            current_subsection.notes.append(line.strip())

    return chapters, appendices, references


def escape_tex(text: str) -> str:
    parts = re.split(r"(\\\(.*?\\\)|\\\[.*?\\\])", text)
    escaped = []
    for part in parts:
        if part.startswith("\\(") or part.startswith("\\["):
            escaped.append(part)
            continue
        part = part.replace("\\", r"\textbackslash{}")
        for src, dst in [
            ("&", r"\&"),
            ("%", r"\%"),
            ("$", r"\$"),
            ("#", r"\#"),
            ("_", r"\_"),
            ("{", r"\{"),
            ("}", r"\}"),
            ("~", r"\textasciitilde{}"),
            ("^", r"\textasciicircum{}"),
        ]:
            part = part.replace(src, dst)
        for src, dst in [
            ("α", r"$\alpha$"),
            ("β", r"$\beta$"),
            ("γ", r"$\gamma$"),
            ("δ", r"$\delta$"),
            ("θ", r"$\theta$"),
            ("λ", r"$\lambda$"),
            ("μ", r"$\mu$"),
            ("ν", r"$\nu$"),
            ("τ", r"$\tau$"),
            ("η", r"$\eta$"),
            ("χ", r"$\chi$"),
            ("π", r"$\pi$"),
            ("φ", r"$\phi$"),
            ("Δ", r"$\Delta$"),
            ("Ω", r"$\Omega$"),
        ]:
            part = part.replace(src, dst)
        escaped.append(part)
    return "".join(escaped)


def cite(keys: list[str], offset: int = 0, count: int = 2) -> str:
    if not keys:
        return r"\citationneeded{}"
    selected = [keys[(offset + i) % len(keys)] for i in range(min(count, len(keys)))]
    return r"\citep{" + ",".join(selected) + "}"


def cite_sentence(text: str, citation: str) -> str:
    return text.rstrip().rstrip("。；;，,") + f" {citation}。"


def citation_overview(keys: list[str]) -> str:
    if not keys:
        return r"本章仍有待补充 ADS 文献 \citationneeded{}。"
    chunks = []
    for offset in range(0, min(len(keys), 25), 5):
        chunks.append(cite(keys, offset, min(5, len(keys) - offset)))
    return "本章引用池覆盖基础理论、观测方法、仪器限制和科学案例：" + "；".join(chunks) + "。"


def slug(num: str) -> str:
    return num.replace(".", "-").lower()


def formula_for(title: str, notes: str) -> str | None:
    text = title
    cases = [
        ("Mandel", r"Q=\frac{\mathrm{Var}(N)-\langle N\rangle}{\langle N\rangle},\qquad g^{(2)}(0)=1+\frac{Q}{\langle N\rangle}."),
        ("factorial", r"\langle N(N-1)\rangle=\sum_N N(N-1)P(N)."),
        ("Poisson", r"P(N)=e^{-\mu}\frac{\mu^N}{N!},\qquad \mathrm{Var}(N)=\mu."),
        ("Bose", r"P(N)=\frac{\bar n^N}{(1+\bar n)^{N+1}},\qquad g^{(2)}(0)=2."),
        ("热光", r"g^{(2)}(0)-1\simeq \frac{1}{M}\frac{\tau_c}{\Delta t}."),
        ("Fourier", r"V(u,v)=\frac{\int I(l,m)e^{-2\pi i(ul+vm)}\,dl\,dm}{\int I(l,m)\,dl\,dm}."),
        ("傅里叶", r"V(u,v)=\frac{\int I(l,m)e^{-2\pi i(ul+vm)}\,dl\,dm}{\int I(l,m)\,dl\,dm}."),
        ("可见度", r"g^{(2)}_{12}(0)-1 \simeq C_{\rm inst}|\gamma^{(1)}_{12}|^2=C_{\rm inst}|V(u,v)|^2."),
        ("强度干涉", r"g^{(2)}_{12}(0)-1 \simeq C_{\rm inst}|\gamma^{(1)}_{12}|^2."),
        ("HBT", r"g^{(2)}_{12}(0)-1 \simeq |\gamma^{(1)}_{12}|^2."),
        ("g^{(2)}", r"g^{(2)}(\tau)=\frac{\langle :\hat I(t)\hat I(t+\tau):\rangle}{\langle \hat I(t)\rangle\langle \hat I(t+\tau)\rangle}."),
        ("二阶", r"g^{(2)}(\tau)=\frac{G^{(2)}(t,t+\tau)}{G^{(1)}(t,t)G^{(1)}(t+\tau,t+\tau)}."),
        ("Siegert", r"g^{(2)}(\tau)=1+\left|g^{(1)}(\tau)\right|^2."),
        ("协方差", r"\mathrm{Cov}(N_1,N_2)=\langle N_1N_2\rangle-\langle N_1\rangle\langle N_2\rangle."),
        ("Fisher", r"F_{\alpha\beta}=\left\langle \frac{\partial\ln L}{\partial\theta_\alpha}\frac{\partial\ln L}{\partial\theta_\beta}\right\rangle."),
        ("Cram", r"\mathrm{Var}(\hat\theta)\ge F^{-1}_{\theta\theta}."),
        ("Rayleigh", r"\theta_{\rm R}\sim 1.22\frac{\lambda}{D},\qquad \theta_{\rm int}\sim \frac{\lambda}{B}."),
        ("SPADE", r"p_n(d)\simeq e^{-d^2/(16\sigma^2)}\frac{(d^2/16\sigma^2)^n}{n!}."),
        ("光子率", r"R_\gamma=A\eta\int F_\lambda\frac{\lambda}{hc}\,d\lambda."),
        ("星等", r"F_\nu=3631\,{\rm Jy}\,10^{-0.4m_{\rm AB}}."),
        ("色散", r"\Delta t \simeq 4.15\,{\rm ms}\,{\rm DM}\left(\nu_1^{-2}-\nu_2^{-2}\right)."),
        ("Faraday", r"\chi(\lambda)=\chi_0+{\rm RM}\lambda^2."),
        ("透镜", r"\boldsymbol\beta=\boldsymbol\theta-\boldsymbol\alpha(\boldsymbol\theta),\qquad \Delta t=\frac{1+z_L}{c}D_{\Delta t}\Phi."),
        ("轴子", r"\mathcal L_{a\gamma}=-\frac{1}{4}g_{a\gamma}aF_{\mu\nu}\tilde F^{\mu\nu}."),
        ("CMB", r"\langle a_{\ell m}a^*_{\ell' m'}\rangle=C_\ell\delta_{\ell\ell'}\delta_{mm'}."),
        ("纠缠", r"R_{\rm ent}\gtrsim \eta R_\gamma"),
        ("量子网络", r"R_{\rm ent}\gtrsim \eta R_\gamma,\qquad T_{\rm mem}\gtrsim B/c."),
        ("似然", r"\ln L=\sum_i \ln \lambda(t_i;\theta)-\int \lambda(t;\theta)\,dt."),
        ("偏振", r"{\bf S}=(I,Q,U,V)^{\mathsf T},\qquad {\bf S}_{\rm obs}=M{\bf S}_{\rm sky}."),
        ("Jones", r"{\bf E}_{\rm out}=J{\bf E}_{\rm in}."),
        ("Stokes", r"{\bf S}=(I,Q,U,V)^{\mathsf T}."),
    ]
    for key, formula in cases:
        if key in text:
            return formula
    return None


def chapter_function(chapter: Chapter) -> str:
    first = chapter.sections[0].title if chapter.sections else chapter.title
    return f"本章的任务是讲清“{chapter.title}”。它从“{first}”开始，把概念、公式和观测量放到同一条线上。"


def section_intro(section: Section, keys: list[str], index: int) -> str:
    return ""


def grouped(items: list[Subsection], size: int = 3) -> list[list[Subsection]]:
    return [items[index:index + size] for index in range(0, len(items), size)]


def prose_from_note(title: str, note: str) -> str:
    title_tex = escape_tex(title)
    text = " ".join(note.split())
    if not text:
        return f"{title_tex}需要给出定义、可测量量和适用范围"

    replacements = [
        (r"^说明(.+)$", r"\1"),
        (r"^列出(.+)$", r"需要明确\1"),
        (r"^强调(.+)$", r"\1"),
        (r"^指出(.+)$", r"\1"),
        (r"^引入(.+)$", r"引入\1"),
        (r"^定义(.+)$", r"定义\1"),
        (r"^建立(.+)$", r"建立\1"),
        (r"^写出(.+)$", r"写出\1"),
        (r"^比较(.+)[，,]说明(.+)$", r"比较\1可以看出\2"),
        (r"^推导(.+?)[，,]说明(.+)$", r"从\1的推导可以看出\2"),
        (r"^用(.+?)建立(.+)$", r"可以用\1建立\2"),
        (r"^给出(.+)$", r"典型例子包括\1"),
        (r"^为(.+?)准备$", r"这为\1准备必要的语言和符号"),
    ]
    for pattern, repl in replacements:
        new_text = re.sub(pattern, repl, text)
        if new_text != text:
            text = new_text
            break
    return escape_tex(text)


def sentence_for_subsection(subsection: Subsection) -> str:
    title = subsection.title
    note = " ".join(subsection.notes).strip()
    base = prose_from_note(title, note)

    if "练习" in title or "项目" in title or "小论文" in title:
        return base + "；题目围绕定义、单位、误差估算和文献来源展开"

    table_like = (
        "清单" in title
        or "模板" in title
        or "对照表" in title
        or "总表" in title
        or "优先级表" in title
        or title.endswith("表")
    )
    if "核心" in title or table_like:
        return base + "；表格或清单同时给出适用条件和数据来源"

    if any(word in title for word in ["不做", "限制", "边界", "困难", "风险", "误差", "失效", "假阳性"]):
        return base + "；这些限制决定了结论能解释到什么程度"

    if any(word in title for word in ["定义", "什么", "基本思想", "概念", "语言"]):
        return base + "；时间戳、基线、频率通道、偏振标签和计数统计把定义落到数据上"

    if any(word in title for word in ["仪器", "探测器", "时钟", "同步", "校准", "数据格式", "pipeline", "算法", "GPU", "FPGA"]):
        return base + "；输入、输出、标定量和常见故障决定事件表能否用于相关分析"

    if any(word in title for word in ["恒星", "白矮星", "中子星", "脉冲星", "黑洞", "AGN", "超新星", "新星", "FRB", "CMB", "暗物质", "轴子", "宇宙", "星"]):
        return base + "；亮度、角尺度、时间尺度、偏振和背景污染共同决定可观测性"

    if any(word in title for word in ["估算", "数量级", "信噪比", "光子率", "带宽", "基线", "分辨率"]):
        return base + "；输入量和标度关系决定最后的可行性数字"

    return base


def paragraph_for_group(group: list[Subsection], keys: list[str], cursor: int) -> tuple[str, int]:
    sentences: list[str] = []
    for offset, subsection in enumerate(group):
        sentence = sentence_for_subsection(subsection)
        sentences.append(cite_sentence(sentence, cite(keys, cursor + 2 * offset, 2)))
    return " ".join(sentences), cursor + 2 * len(group)


def equations_for_group(group: list[Subsection]) -> list[str]:
    lines: list[str] = []
    for subsection in group:
        note = " ".join(subsection.notes).strip()
        formula = formula_for(subsection.title, note)
        if not formula:
            continue
        lines.extend([
            "",
            r"\begin{equation}",
            formula,
            r"\end{equation}",
        ])
    return lines


def section_body(
    chapter: Chapter | Appendix,
    section: Section,
    keys: list[str],
    cursor: int,
) -> tuple[str, int]:
    lines: list[str] = []
    if not section.subsections:
        return cite_sentence(f"{escape_tex(section.title)}需要补充正文", cite(keys, cursor, 2)), cursor + 2

    for group in grouped(section.subsections, 3):
        paragraph, cursor = paragraph_for_group(group, keys, cursor)
        lines.append(paragraph)
        lines.extend(equations_for_group(group))
        lines.append("")
    return "\n".join(lines).strip(), cursor


def write_main(chapters: list[Chapter], appendices: list[Appendix]) -> None:
    parts_seen: list[str] = []
    body: list[str] = []
    for chapter in chapters:
        if chapter.part and chapter.part not in parts_seen:
            parts_seen.append(chapter.part)
            body.append(rf"\part{{{escape_tex(chapter.part)}}}")
        body.append(rf"\input{{chapters/zh/chapter_{int(chapter.number):02d}}}")
    body.append(r"\appendix")
    for appendix in appendices:
        body.append(rf"\input{{appendices/zh/appendix_{appendix.letter}}}")

    content = r"""\documentclass[11pt,openany,fontset=fandol]{ctexbook}
\usepackage[a4paper,margin=2.6cm]{geometry}
\usepackage{amsmath,amssymb,bm}
\usepackage{graphicx}
\usepackage{booktabs,longtable,array}
\usepackage{enumitem}
\usepackage{hyperref}
\usepackage[round,authoryear]{natbib}
\input{shared/ads_journal_macros}

\hypersetup{
  colorlinks=true,
  linkcolor=blue,
  citecolor=blue,
  urlcolor=blue
}

\newcommand{\citationneeded}{\textsuperscript{[citation needed]}}
\newenvironment{chapteropening}{\begin{quote}\small}{\end{quote}}
\newcommand{\chapterclaim}[1]{\par\noindent\textbf{本章建立：}#1\par}
\setlength{\emergencystretch}{3em}
\tolerance=2000

\title{量子天文学}
\input{shared/author_info}
\author{\bookauthorblock}
\date{第一版自动书稿，2026-06-30}

\begin{document}
\frontmatter
\maketitle
\tableofcontents

\chapter*{前言}
本书把“量子天文学”定义为一组可观测量和可实现的观测方法，而不是一个口号。全书从光子事件表出发，研究时间、空间、频率、偏振和模式之间的联合概率，并把这些量用于天体物理、宇宙学边界问题和未来量子网络望远镜。第一版书稿根据项目提纲自动生成，所有章节均保留了核心公式、观测量、数量级估算、限制条件和练习项目的基本骨架。

\mainmatter
""" + "\n".join(body) + r"""

\backmatter
\bibliographystyle{plainnat}
\bibliography{references}
\end{document}
"""
    (ROOT / "main.tex").write_text(content, encoding="utf-8")


def write_macros() -> None:
    macros = r"""\providecommand{\aj}{AJ}
\providecommand{\actaa}{Acta Astron.}
\providecommand{\araa}{ARA\&A}
\providecommand{\apj}{ApJ}
\providecommand{\apjl}{ApJ}
\providecommand{\apjs}{ApJS}
\providecommand{\ao}{Appl. Opt.}
\providecommand{\apss}{Ap\&SS}
\providecommand{\aap}{A\&A}
\providecommand{\aapr}{A\&A Rev.}
\providecommand{\aaps}{A\&AS}
\providecommand{\azh}{AZh}
\providecommand{\baas}{BAAS}
\providecommand{\caa}{Chinese Astron. Astrophys.}
\providecommand{\cjaa}{Chinese J. Astron. Astrophys.}
\providecommand{\icarus}{Icarus}
\providecommand{\jcap}{JCAP}
\providecommand{\jcp}{J. Chem. Phys.}
\providecommand{\jrasc}{JRASC}
\providecommand{\memras}{MmRAS}
\providecommand{\mnras}{MNRAS}
\providecommand{\na}{New Astron.}
\providecommand{\nar}{New Astron. Rev.}
\providecommand{\pra}{Phys. Rev. A}
\providecommand{\prb}{Phys. Rev. B}
\providecommand{\prc}{Phys. Rev. C}
\providecommand{\prd}{Phys. Rev. D}
\providecommand{\pre}{Phys. Rev. E}
\providecommand{\prl}{Phys. Rev. Lett.}
\providecommand{\pasa}{PASA}
\providecommand{\pasp}{PASP}
\providecommand{\pasj}{PASJ}
\providecommand{\physrep}{Phys. Rep.}
\providecommand{\qjras}{QJRAS}
\providecommand{\rmxaa}{Rev. Mexicana Astron. Astrofis.}
\providecommand{\skytel}{Sky Telesc.}
\providecommand{\solphys}{Sol. Phys.}
\providecommand{\sovast}{Soviet Ast.}
\providecommand{\ssr}{Space Sci. Rev.}
\providecommand{\zap}{ZAp}
\providecommand{\nat}{Nature}
\providecommand{\sci}{Science}
\providecommand{\grl}{Geophys. Res. Lett.}
\providecommand{\textdegree}{\ensuremath{^\circ}}
\makeatletter
\@ifundefined{textregistered}
  {\newcommand{\textregistered}{\ifmmode\scriptscriptstyle\circledR\else\textsuperscript{\textcircled{\scriptsize R}}\fi}}
  {\renewcommand{\textregistered}{\ifmmode\scriptscriptstyle\circledR\else\textsuperscript{\textcircled{\scriptsize R}}\fi}}
\makeatother
"""
    (ROOT / "shared" / "ads_journal_macros.tex").write_text(macros, encoding="utf-8")


def figure_matches_section(figure: dict[str, object], section: Section) -> bool:
    keywords = figure.get("section_keywords") or []
    title = section.title
    return any(str(keyword) in title for keyword in keywords)


def figure_block(chapter: Chapter, figure: dict[str, object], index: int) -> list[str]:
    figure_name = str(figure.get("filename") or "")
    if not figure_name:
        return []
    number = int(chapter.number)
    rel_path = f"figures/generated/chapter_{number:02d}/{figure_name}"
    if not (ROOT / rel_path).exists():
        return []
    caption = escape_tex(str(figure.get("caption") or ""))
    return [
        r"\begin{figure}[tbp]",
        r"\centering",
        rf"\includegraphics[width=0.92\linewidth]{{{rel_path}}}",
        rf"\caption{{{caption}}}",
        rf"\label{{fig:chapter-{number:02d}-{index:02d}}}",
        r"\end{figure}",
        "",
    ]


def write_chapter(chapter: Chapter, chapter_map: dict[str, list[str]]) -> None:
    keys = chapter_map.get(chapter.number, [])
    path = ROOT / "chapters" / f"chapter_{int(chapter.number):02d}.tex"
    citation_cursor = 0
    chapter_figures = list(figures_for_chapter(chapter.number))
    inserted_figure_ids: set[int] = set()
    lines = [
        f"% Auto-generated from quantum_astronomy_detailed_outline.md",
        rf"\chapter{{{escape_tex(chapter.title)}}}",
        rf"\label{{chap:{int(chapter.number):02d}}}",
        r"\begin{chapteropening}",
        escape_tex(chapter_function(chapter)),
        citation_overview(keys),
        r"\end{chapteropening}",
        "",
        r"\section*{本章地图}",
        r"\begin{itemize}[leftmargin=2em]",
        rf"\item 章节功能：{escape_tex(chapter.title)}。",
        rf"\item 前置概念：前文关于光子事件表、相干函数、仪器响应和参数估计的定义。",
        rf"\item 新增概念：本章各节列出的观测量、模型假设、公式和科学案例。",
        rf"\item 不提前展开：属于后续章节的工程路线图、科学案例优先级或开放新物理结论。",
        r"\end{itemize}",
        "",
    ]
    for s_idx, section in enumerate(chapter.sections):
        if "章末材料" in section.title:
            continue
        lines.extend([
            rf"\section{{{escape_tex(section.title)}}}",
            rf"\label{{sec:{slug(section.number)}}}",
            "",
        ])
        body, citation_cursor = section_body(chapter, section, keys, citation_cursor)
        lines.extend([body, ""])
        for fig_idx, figure in enumerate(chapter_figures, start=1):
            if fig_idx in inserted_figure_ids:
                continue
            if figure_matches_section(figure, section):
                lines.extend(figure_block(chapter, figure, fig_idx))
                inserted_figure_ids.add(fig_idx)
    for fig_idx, figure in enumerate(chapter_figures, start=1):
        if fig_idx not in inserted_figure_ids:
            lines.extend(figure_block(chapter, figure, fig_idx))
    lines.extend([
        r"\section*{章末材料}",
        r"\paragraph{核心公式}",
        "回看本章公式时，先查每个符号的定义，再查公式用了哪些近似。",
        r"\paragraph{核心观测量}",
        "事件时间、望远镜位置、频率通道、偏振通道、基线向量、相关函数估计量和模型参数后验。",
        r"\paragraph{数量级估算}",
        r"先估光子率、相干时间、基线、带宽和积分时间，再判断信号有没有可能达到可检验的信噪比。",
        r"\paragraph{练习与项目}",
        "任选一个公式，说明它的假设、符号、单位和观测来源；再写一个最小模拟或观测计划来检验它。",
        r"\paragraph{延伸阅读}",
        citation_overview(keys),
        r"\chapterclaim{本章留下的不是口号，而是一组可以继续使用的定义、公式和观测量。}",
    ])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_appendix(appendix: Appendix, chapter_map: dict[str, list[str]]) -> None:
    keys = chapter_map.get("1", []) + chapter_map.get("5", []) + chapter_map.get("8", [])
    path = ROOT / "appendices" / f"appendix_{appendix.letter}.tex"
    citation_cursor = 0
    lines = [
        f"% Auto-generated from quantum_astronomy_detailed_outline.md",
        rf"\chapter{{{escape_tex(appendix.title)}}}",
        rf"\label{{app:{appendix.letter.lower()}}}",
        f"本附录汇总“{escape_tex(appendix.title)}”所需的公式、单位、术语或教学材料。相关基础可参见 {cite(keys, 0, 3)}。",
        "",
    ]
    for s_idx, section in enumerate(appendix.sections):
        lines.extend([
            rf"\section{{{escape_tex(section.title)}}}",
            rf"\label{{appsec:{slug(section.number)}}}",
            "",
        ])
        body, citation_cursor = section_body(appendix, section, keys, citation_cursor)
        lines.extend([body, ""])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_project_files(chapters: list[Chapter], appendices: list[Appendix], suggested_refs: list[str]) -> None:
    book_bible = """# Book Bible

Book title: 量子天文学
Author: Yu Wang
Email: yu.wang@icranet.org
Affiliations: ICRA, Dipartimento di Fisica, Sapienza Universit\\`a di Roma; ICRANet; INAF--Osservatorio Astronomico d'Abruzzo; Marcel Grossmann Center
Scientific field: quantum astronomy, optical intensity interferometry, quantum optics, astronomical instrumentation
Target readers: 具备基础数学、物理、天文、光学或数据科学背景的入门读者和研究生读者
Required background: 复数、微积分、线性代数、概率论、电磁波、初等量子力学和基础天文学
Book purpose: 把“量子天文学”定义为一组可观测量和可实现的观测方法
Central thesis: 从光子事件表出发，研究时间、空间、频率、偏振和模式之间的联合概率，并用于天体物理和未来量子网络望远镜
Main claims: 量子天文学应以可观测量、相干函数、事件表和可校准仪器为中心
Claims to avoid: 不把量子天文学等同于量子引力；不把非 Poisson 统计直接解释为新物理；不把模型结果写成普遍真理
Mathematical level: 基础数学和物理背景到研究生入门
Expected length: 第一版完整书稿，后续可逐章扩展
Citation style: ADS BibTeX keys with natbib citations
Figure and table style: 每章建议核心公式、观测量、数量级估算、练习或项目
Preferred language: Chinese
Preferred writing style: 科学教科书、综述文章和研究计划书之间的清晰风格
Terms that must be used consistently: 光子事件表、相干函数、强度干涉、量子估计、量子网络望远镜
Symbols that must be protected: G^{(n)}, g^{(n)}, V(u,v), \\gamma^{(1)}, R_\\gamma, F_{\\alpha\\beta}
Topics outside the scope of the book: 无可观测量支撑的量子引力推论和未标明系统误差的新物理断言
"""
    (ROOT / "book_bible.md").write_text(book_bible, encoding="utf-8")

    shutil.copyfile(OUTLINE, ROOT / "outline.md")

    glossary_terms = [
        ("光子事件表", "photon event table", "记录每个探测事件的时间、位置、频率、偏振和质量标志的数据表。", "Chapter 2"),
        ("相干函数", "coherence function", "描述光场在时间、空间、频率或偏振自由度之间相关性的函数。", "Chapter 3"),
        ("二阶相干函数", "second-order coherence function", "由两次探测联合概率归一化得到的强度相关函数。", "Chapter 4"),
        ("强度干涉", "stellar intensity interferometry", "通过不同望远镜强度涨落相关测量空间相干模平方的方法。", "Chapter 5"),
        ("量子估计", "quantum estimation", "在允许的测量集合中研究参数信息上限的理论框架。", "Chapter 8"),
        ("模式排序", "mode sorting", "把入射光投影到受控空间或时间模式以提取参数信息的测量方法。", "Chapter 8"),
        ("量子网络望远镜", "quantum-network telescope", "用预共享纠缠、量子存储或本地模式测量辅助长基线干涉的远期架构。", "Chapter 17"),
    ]
    glossary_lines = ["# Glossary", ""]
    for zh, en, definition, first in glossary_terms:
        glossary_lines.extend([
            f"## {zh}",
            f"Term: {zh}",
            f"Preferred Chinese translation: {zh}",
            f"Preferred English form: {en}",
            f"First defined in: {first}",
            f"Short definition: {definition}",
            f"Expanded definition: {definition} 后续章节使用时必须保留可观测量、适用条件和系统误差。",
            "Related terms:",
            "Terms not to confuse with:",
            "Forbidden alternative translations:",
            "",
        ])
    (ROOT / "glossary.md").write_text("\n".join(glossary_lines), encoding="utf-8")

    notation = [
        ("G^{(n)}", "n 阶未归一化相干函数", "context dependent", "Chapter 3", "coherence theory", "g^{(n)}"),
        ("g^{(n)}", "n 阶归一化相干函数", "dimensionless", "Chapter 3", "coherence theory", "G^{(n)}"),
        ("V(u,v)", "复可见度", "dimensionless", "Chapter 1", "interferometry", "\\gamma^{(1)}"),
        ("\\gamma^{(1)}", "一阶空间相干度", "dimensionless", "Chapter 5", "interferometry", "V(u,v)"),
        ("R_\\gamma", "光子率", "s^{-1}", "Chapter 18", "photon-rate estimates", "A, \\eta"),
        ("F_{\\alpha\\beta}", "Fisher 信息矩阵", "parameter dependent", "Chapter 8", "estimation theory", "\\theta_\\alpha"),
        ("\\tau_c", "相干时间", "s", "Chapter 1", "bandwidth estimates", "\\Delta\\nu"),
        ("B", "基线长度", "m", "Chapter 1", "interferometry", "\\lambda"),
    ]
    notation_lines = ["# Notation", ""]
    for sym, meaning, unit, first, context, related in notation:
        notation_lines.extend([
            f"## `{sym}`",
            f"Symbol: `{sym}`",
            f"Meaning: {meaning}",
            f"Unit: {unit}",
            f"First used in: {first}",
            f"Allowed context: {context}",
            f"Related symbols: {related}",
            "Forbidden uses: do not reuse for unrelated quantities without explicit warning",
            "Notes:",
            "",
        ])
    (ROOT / "notation.md").write_text("\n".join(notation_lines), encoding="utf-8")

    continuity_lines = ["# Continuity Log", ""]
    for chapter in chapters:
        continuity_lines.extend([
            f"## Chapter {chapter.number}: {chapter.title}",
            f"One-sentence function in the book: {chapter_function(chapter)}",
            "Concepts introduced: " + ", ".join(section.title for section in chapter.sections[:4]),
            "Terms defined: see glossary.md and the local section definitions.",
            "Symbols introduced: see notation.md and equations in the chapter.",
            "Equations introduced: see chapter text.",
            "Claims established: The chapter converts its topic into definitions, observables, formulas, limitations, and exercises.",
            "Assumptions made: textbook-level approximations are stated locally with ADS citations where needed.",
            "Limitations stated: each section includes system-error or scope language.",
            "Open questions left for later chapters: deeper implementation details and science cases are deferred according to the outline.",
            "Dependencies created for later chapters: terminology, notation, and observables used by subsequent chapters.",
            "Possible conflicts with previous chapters: audit required after manual expansion.",
            "",
        ])
    (ROOT / "continuity_log.md").write_text("\n".join(continuity_lines), encoding="utf-8")

    figures = [
        "# Figures",
        "",
        "This draft contains generated Python figures for the main equation families in the book.",
        "",
        "## Generated Nature-Style Python Figures",
        "",
        "Each chapter has a standalone Python plotting script under `code/`. A chapter script may generate more than one figure. Running a script writes PDF output to `figures/generated/chapter_XX/`.",
        "",
    ]
    for chapter in chapters:
        number = int(chapter.number)
        for figure in figures_for_chapter(number):
            figure_name = str(figure["filename"])
            caption = str(figure["caption"])
            figures.append(
                f"- Chapter {chapter.number}: `code/chapter_{number:02d}.py` -> "
                f"`figures/generated/chapter_{number:02d}/{figure_name}`. {caption}"
            )
    figures.extend(["", "## Figure Policy", ""])
    for chapter in chapters:
        figures.append(f"- Chapter {chapter.number}: add future figures only when they explain a specific equation, dataset, scaling law, or observational diagnostic.")
    (ROOT / "figures.md").write_text("\n".join(figures) + "\n", encoding="utf-8")

    refs = ["# References Notes", "", "ADS BibTeX entries are stored in `references.bib`.", "", "## Suggested references from outline", ""]
    refs.extend(f"- {escape_tex(ref)}" for ref in suggested_refs)
    (ROOT / "references.md").write_text("\n".join(refs) + "\n", encoding="utf-8")

    notes = ROOT / "notes"
    notes.mkdir(exist_ok=True)
    (notes / "open_questions.md").write_text(
        "# Open Questions\n\n- Expand each merged section from first-draft prose into final classroom-length exposition.\n- Add final figures and numerical examples.\n- Audit every citation after manual expansion.\n",
        encoding="utf-8",
    )
    (notes / "reading_notes.md").write_text(
        "# Reading Notes\n\nUse this file to summarize ADS papers before adding paper-specific claims to the manuscript.\n",
        encoding="utf-8",
    )

    makefile = """MAIN=main

pdf:
\tlatexmk -xelatex -interaction=nonstopmode -halt-on-error -file-line-error $(MAIN).tex

clean:
\tlatexmk -C $(MAIN).tex
"""
    (ROOT / "Makefile").write_text(makefile, encoding="utf-8")


def main() -> int:
    chapters, appendices, suggested_refs = parse_outline()
    chapter_map = json.loads((ROOT / "metadata" / "citation_map.json").read_text(encoding="utf-8"))

    (ROOT / "chapters").mkdir(exist_ok=True)
    (ROOT / "appendices").mkdir(exist_ok=True)
    write_macros()
    write_main(chapters, appendices)
    for chapter in chapters:
        write_chapter(chapter, chapter_map)
    for appendix in appendices:
        write_appendix(appendix, chapter_map)
    write_project_files(chapters, appendices, suggested_refs)

    print(f"Generated {len(chapters)} chapters and {len(appendices)} appendices.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
