#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第 12 章图像脚本

运行方式：
    python code/chapter_12.py

输出目录：
    figures/generated/chapter_12/

备注：
    本脚本只生成本章需要的公式图。每张图的注释说明它对应的公式族、
    变量含义和阅读方式。默认参数用于展示标度关系，不代表某一次真实观测。
"""

from __future__ import annotations

from pathlib import Path

from plot_recipes import draw_figure
from plot_style import ROOT


OUTDIR = ROOT / "figures" / "generated" / "chapter_12"


def main() -> None:

    # 图 1: 黑洞的自然长度、时间和角尺度。
    # 左图给出 t_g=GM/c^3 随质量的线性标度；右图比较不同距离下的 shadow 角直径。
    # 输出文件: figures/generated/chapter_12/ch12_black_hole_scales.pdf
    draw_figure('ch12_black_hole_scales.pdf', OUTDIR)

    # 图 2: 标准薄盘的光学/紫外半光半径和轨道、热时间标度。
    # 图中半径采用 R_lambda 正比 lambda^(4/3) 的标度，橙色区提示微透镜常给出更大的光学盘。
    # 输出文件: figures/generated/chapter_12/ch12_accretion_disk_radii.pdf
    draw_figure('ch12_accretion_disk_radii.pdf', OUTDIR)

    # 图 3: BLR 反响映射半径-光度关系，以及旋转 BLR 的谱线差分相位。
    # 左图把时间延迟变成物理半径；右图说明谱线红蓝翼的 photocenter 偏移怎样进入干涉相位。
    # 输出文件: figures/generated/chapter_12/ch12_blr_reverberation_interferometry.pdf
    draw_figure('ch12_blr_reverberation_interferometry.pdf', OUTDIR)

    # 图 4: 42 微角秒量级环状结构的长基线可见度。
    # 窄环在 Glambda 基线出现慢衰减振荡，较厚吸积流会更快被解析掉。
    # 输出文件: figures/generated/chapter_12/ch12_photon_ring_visibility.pdf
    draw_figure('ch12_photon_ring_visibility.pdf', OUTDIR)

    # 图 5: 阻尼随机游走模型的自相关和功率谱。
    # 阻尼时间越长，相关函数衰减越慢，PSD 的低频平台延伸到更低频。
    # 输出文件: figures/generated/chapter_12/ch12_variability_autocorrelation.pdf
    draw_figure('ch12_variability_autocorrelation.pdf', OUTDIR)

    # 图 6: Hawking 温度和蒸发时间随质量的数量级。
    # 恒星质量和超大质量黑洞的 T_H 远低于 CMB，蒸发时间远超宇宙年龄。
    # 输出文件: figures/generated/chapter_12/ch12_hawking_temperature_scale.pdf
    draw_figure('ch12_hawking_temperature_scale.pdf', OUTDIR)


if __name__ == "__main__":
    main()
