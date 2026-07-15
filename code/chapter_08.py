#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第 08 章图像脚本

运行方式：
    python code/chapter_08.py

输出目录：
    figures/generated/chapter_08/

备注：
    本脚本只生成本章需要的公式图。每张图的注释说明它对应的公式族、
    变量含义和阅读方式。默认参数用于展示标度关系，不代表某一次真实观测。
"""

from __future__ import annotations

from pathlib import Path

from plot_recipes import draw_figure
from plot_style import ROOT


OUTDIR = ROOT / "figures" / "generated" / "chapter_08"


def main() -> None:

    # 图 1: 数值积分两个不相干高斯点源的像面概率密度，比较直接成像和理想模式测量
    # 对分离参数 s 的 Fisher 信息；横轴用点扩散函数宽度 sigma 归一化。
    # 输出文件: figures/generated/chapter_08/ch08_rayleigh_information.pdf
    draw_figure('ch08_rayleigh_information.pdf', OUTDIR)

    # 图 2: 高斯点扩散函数下，理想 Hermite-Gaussian 模式排序的模式概率
    # p_n=exp(-Q)Q^n/n!，其中 Q=s^2/(16 sigma^2)。
    # 输出文件: figures/generated/chapter_08/ch08_spade_probabilities.pdf
    draw_figure('ch08_spade_probabilities.pdf', OUTDIR)

    # 图 3: 用 Cramer-Rao 下界比较亚分辨双源在直接成像、理想模式测量、
    # 以及存在模式匹配系统误差时的分离误差随光子数的变化。
    # 输出文件: figures/generated/chapter_08/ch08_cramer_rao_bound.pdf
    draw_figure('ch08_cramer_rao_bound.pdf', OUTDIR)

    # 图 4: 对照同一组双点源在直接像面和 Hermite-Gaussian 模式输出中的表现；
    # 小分离时像面曲线几乎重合，但模式概率已经给出可计数的参数信号。
    # 输出文件: figures/generated/chapter_08/ch08_direct_image_vs_modes.pdf
    draw_figure('ch08_direct_image_vs_modes.pdf', OUTDIR)

    # 图 5: 均匀圆盘恒星的平方可见度和对角直径的 Fisher 权重随基线变化；
    # 用来说明强度干涉阵列为什么要把基线放在可见度斜率大的区域。
    # 输出文件: figures/generated/chapter_08/ch08_visibility_fisher_design.pdf
    draw_figure('ch08_visibility_fisher_design.pdf', OUTDIR)


if __name__ == "__main__":
    main()
