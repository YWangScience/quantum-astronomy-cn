#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第 22 章图像脚本

运行方式：
    python code/chapter_22.py

输出目录：
    figures/generated/chapter_22/

备注：
    本脚本只生成本章需要的公式图。每张图的注释说明它对应的公式族、
    变量含义和阅读方式。默认参数用于展示标度关系，不代表某一次真实观测。
"""

from __future__ import annotations

from pathlib import Path

from plot_recipes import draw_figure
from plot_style import ROOT


OUTDIR = ROOT / "figures" / "generated" / "chapter_22"


def main() -> None:

    # 图 1: 研究路线图中的技术成熟度、科学回报、成本和风险张力。近期项目应优先落在高成熟度且可校准的区域。
    # 输出文件: figures/generated/chapter_22/ch22_roadmap_trade_space.pdf
    draw_figure('ch22_roadmap_trade_space.pdf', OUTDIR)

    # 图 2: 从课程实验、探测器和恒星 SII 样本到多通道相关、瞬变跟进和量子网络 pathfinder 的阶段性时间线。
    # 输出文件: figures/generated/chapter_22/ch22_program_timeline.pdf
    draw_figure('ch22_program_timeline.pdf', OUTDIR)

    # 图 3: 路线图门槛矩阵。每个阶段都要同时满足光子率、计时、校准、pipeline 和科学样本的验收指标。
    # 输出文件: figures/generated/chapter_22/ch22_milestone_gates.pdf
    draw_figure('ch22_milestone_gates.pdf', OUTDIR)

    # 图 4: proposal 中必须交付的数据产品链。从事件表到相关函数、可见度、似然、后验和公开归档。
    # 输出文件: figures/generated/chapter_22/ch22_data_product_stack.pdf
    draw_figure('ch22_data_product_stack.pdf', OUTDIR)

    # 图 5: 风险登记图。高概率高影响的风险需要在项目开始前配套缓解方案和失败判据。
    # 输出文件: figures/generated/chapter_22/ch22_risk_register.pdf
    draw_figure('ch22_risk_register.pdf', OUTDIR)


if __name__ == "__main__":
    main()
