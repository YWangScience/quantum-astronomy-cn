#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第 16 章图像脚本

运行方式：
    python code/chapter_16.py

输出目录：
    figures/generated/chapter_16/

备注：
    本脚本只生成本章需要的公式图。每张图的注释说明它对应的公式族、
    变量含义和阅读方式。默认参数用于展示标度关系，不代表某一次真实观测。
"""

from __future__ import annotations

from pathlib import Path

from plot_recipes import draw_figure
from plot_style import ROOT


OUTDIR = ROOT / "figures" / "generated" / "chapter_16"


def main() -> None:

    # 图 1: CMB 黑体光场。左图画 Planck 谱强度，右图画每个模式的平均光子占据数。
    # 这张图对应本章的黑体公式和热光数量级。
    # 输出文件: figures/generated/chapter_16/ch16_cmb_blackbody.pdf
    draw_figure('ch16_cmb_blackbody.pdf', OUTDIR)

    # 图 2: CMB 角功率谱和 cosmic variance。左图显示声学峰的标度结构；
    # 右图显示每个多极矩只有 2 ell + 1 个天空模式时产生的样本方差。
    # 输出文件: figures/generated/chapter_16/ch16_cmb_power_spectrum.pdf
    draw_figure('ch16_cmb_power_spectrum.pdf', OUTDIR)

    # 图 3: 暴胀涨落的两模压缩图像。左图显示模式穿出视界后动量象限被压窄；
    # 右图用相空间椭圆展示 squeezing 参数增大时的相干相关。
    # 输出文件: figures/generated/chapter_16/ch16_squeezed_modes.pdf
    draw_figure('ch16_squeezed_modes.pdf', OUTDIR)

    # 图 4: 原初非高斯模板。左图比较 local、equilateral、orthogonal 形状；
    # 右图给出 Planck 2018 对三个 f_NL 参数的代表性约束。
    # 输出文件: figures/generated/chapter_16/ch16_non_gaussian_templates.pdf
    draw_figure('ch16_non_gaussian_templates.pdf', OUTDIR)

    # 图 5: B 模和张量标量比。左图比较 lensing B 模与不同 r 的 tensor B 模；
    # 右图显示 BICEP/Keck 约束随观测季节改进的量级。
    # 输出文件: figures/generated/chapter_16/ch16_bmode_constraints.pdf
    draw_figure('ch16_bmode_constraints.pdf', OUTDIR)

    # 图 6: 宇宙双折射。左图显示偏振角旋转如何产生 EB；
    # 右图显示 cosmic birefringence beta 与仪器角 alpha 的退化。
    # 输出文件: figures/generated/chapter_16/ch16_birefringence_eb.pdf
    draw_figure('ch16_birefringence_eb.pdf', OUTDIR)


if __name__ == "__main__":
    main()
