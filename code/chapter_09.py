#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第 09 章图像脚本

运行方式：
    python code/chapter_09.py

输出目录：
    figures/generated/chapter_09/

备注：
    本脚本只生成本章需要的公式图。每张图的注释说明它对应的公式族、
    变量含义和阅读方式。默认参数用于展示标度关系，不代表某一次真实观测。
"""

from __future__ import annotations

from pathlib import Path

from plot_recipes import draw_figure
from plot_style import ROOT


OUTDIR = ROOT / "figures" / "generated" / "chapter_09"


def main() -> None:

    # 图 1: 比较单模热光、多模热光、相干态和窄相干谱线成分的二阶相干函数。
    # 横轴按相干时间 tau_c 归一化，纵轴显示 g2 的聚束或近 Poisson 行为。
    # 输出文件: figures/generated/chapter_09/ch09_radiation_g2_diagnostics.pdf
    draw_figure('ch09_radiation_g2_diagnostics.pdf', OUTDIR)

    # 图 2: 亮温尺度图。用 log10(T_b/K) 对比热源、HII 区、非相干射电上限、
    # 脉冲星巨脉冲和 FRB，说明何时必须引入相干发射。
    # 输出文件: figures/generated/chapter_09/ch09_brightness_temperature_scale.pdf
    draw_figure('ch09_brightness_temperature_scale.pdf', OUTDIR)

    # 图 3: 热光聚束峰被时间 bin、偏振、空间和光谱模式数稀释的标度。
    # 输出文件: figures/generated/chapter_09/ch09_thermal_mode_dilution.pdf
    draw_figure('ch09_thermal_mode_dilution.pdf', OUTDIR)

    # 图 4: 黑体、自由自由、同步辐射和逆康普顿谱的示意形状。
    # 这些曲线只展示常见谱形和截断，不代替具体源的辐射转移模型。
    # 输出文件: figures/generated/chapter_09/ch09_spectral_mechanisms.pdf
    draw_figure('ch09_spectral_mechanisms.pdf', OUTDIR)

    # 图 5: 亮温、偏振和二阶相干对比度共同组成辐射机制诊断平面。
    # 点大小表示聚束对比度量级，横轴高亮温区域提示相干发射约束。
    # 输出文件: figures/generated/chapter_09/ch09_diagnostic_plane.pdf
    draw_figure('ch09_diagnostic_plane.pdf', OUTDIR)


if __name__ == "__main__":
    main()
