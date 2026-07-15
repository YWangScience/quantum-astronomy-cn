#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第 19 章图像脚本

运行方式：
    python code/chapter_19.py

输出目录：
    figures/generated/chapter_19/

备注：
    本脚本只生成本章需要的公式图。每张图的注释说明它对应的公式族、
    变量含义和阅读方式。默认参数用于展示标度关系，不代表某一次真实观测。
"""

from __future__ import annotations

from pathlib import Path

from plot_recipes import draw_figure
from plot_style import ROOT


OUTDIR = ROOT / "figures" / "generated" / "chapter_19"


def main() -> None:

    # 图 1: 把第一代候选目标放在典型星等和角尺度平面中，快速判断哪些目标同时够亮且能被现有基线解析。
    # 输出文件: figures/generated/chapter_19/ch19_science_case_feasibility.pdf
    draw_figure('ch19_science_case_feasibility.pdf', OUTDIR)

    # 图 2: 双星平方可见度随基线的振荡，展示分离角和流量比怎样进入第一代双星观测。
    # 输出文件: figures/generated/chapter_19/ch19_binary_visibility.pdf
    draw_figure('ch19_binary_visibility.pdf', OUTDIR)

    # 图 3: 新星和超新星膨胀半径随时间增长，转成角直径和所需基线后可判断触发观测的时效。
    # 输出文件: figures/generated/chapter_19/ch19_transient_expansion.pdf
    draw_figure('ch19_transient_expansion.pdf', OUTDIR)

    # 图 4: 自然激光候选的 photon statistics 取决于有效模式数和线宽，窄线会提高可解析相关 contrast。
    # 输出文件: figures/generated/chapter_19/ch19_natural_laser_statistics.pdf
    draw_figure('ch19_natural_laser_statistics.pdf', OUTDIR)

    # 图 5: Crab 光学脉冲的相位窗和时间误差，用于判断相位分辨光子统计是否可执行。
    # 输出文件: figures/generated/chapter_19/ch19_crab_phase_windows.pdf
    draw_figure('ch19_crab_phase_windows.pdf', OUTDIR)

    # 图 6: 科学价值、技术成熟度和系统误差风险给出第一代项目排序。
    # 输出文件: figures/generated/chapter_19/ch19_priority_matrix.pdf
    draw_figure('ch19_priority_matrix.pdf', OUTDIR)


if __name__ == "__main__":
    main()
