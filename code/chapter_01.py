#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第 01 章图像脚本

运行方式：
    python code/chapter_01.py

输出目录：
    figures/generated/chapter_01/

备注：
    本脚本只生成第一章正文使用的基础概念图。更专门的干涉、相关、
    偏振和信息量图像由后续章节的脚本生成。
"""

from __future__ import annotations

from pathlib import Path

from plot_recipes import draw_figure
from plot_style import ROOT


OUTDIR = ROOT / "figures" / "generated" / "chapter_01"


def main() -> None:

    # 图 1: 复振幅相量和两束光干涉。左图把复数相位画成平面上的箭头，右图显示相位差怎样控制相长和相消。
    # 输出文件: figures/generated/chapter_01/ch01_phase_interference.pdf
    draw_figure('ch01_phase_interference.pdf', OUTDIR)

    # 图 2: Poisson 计数分布。均值为 mu 时，方差也是 mu，shot noise 的尺度为 sqrt(mu)。
    # 输出文件: figures/generated/chapter_01/ch01_photon_count_statistics.pdf
    draw_figure('ch01_photon_count_statistics.pdf', OUTDIR)


if __name__ == "__main__":
    main()
