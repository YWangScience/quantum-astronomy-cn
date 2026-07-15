#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第 15 章图像脚本

运行方式：
    python code/chapter_15.py

输出目录：
    figures/generated/chapter_15/

备注：
    本脚本只生成本章需要的公式图。每张图的注释说明它对应的公式族、
    变量含义和阅读方式。默认参数用于展示标度关系，不代表某一次真实观测。
"""

from __future__ import annotations

from pathlib import Path

from plot_recipes import draw_figure
from plot_style import ROOT


OUTDIR = ROOT / "figures" / "generated" / "chapter_15"


def main() -> None:

    # 图 1: 轴子-光子转换。左图展示动量失配 qL 破坏相干转换；
    # 右图给出相干极限下 P_{a->gamma} 随磁场和路径长度的量级。
    # 输出文件: figures/generated/chapter_15/ch15_axion_conversion.pdf
    draw_figure('ch15_axion_conversion.pdf', OUTDIR)

    # 图 2: 超轻轴子暗物质引起的偏振角振荡。左图是观测时间序列；
    # 右图把轴子质量转换为振荡周期和相干时间。
    # 输出文件: figures/generated/chapter_15/ch15_axion_polarization_oscillation.pdf
    draw_figure('ch15_axion_polarization_oscillation.pdf', OUTDIR)

    # 图 3: 宇宙双折射。左图显示旋转角 beta 如何把 E 模泄漏到 EB；
    # 右图显示 beta 与探测器偏振角误差 alpha 的退化。
    # 输出文件: figures/generated/chapter_15/ch15_cosmic_birefringence.pdf
    draw_figure('ch15_cosmic_birefringence.pdf', OUTDIR)

    # 图 4: 黑洞轴子云。左图给出不同黑洞质量对应的超辐射轴子质量窗口；
    # 右图展示 M87* 和 Sgr A* 偏振角振荡的典型时间尺度。
    # 输出文件: figures/generated/chapter_15/ch15_black_hole_axion_cloud.pdf
    draw_figure('ch15_black_hole_axion_cloud.pdf', OUTDIR)

    # 图 5: FRB 的 Faraday 前景。左图显示高 RM 下偏振角随频率快速缠绕；
    # 右图显示有限通道宽度导致的带宽去偏振。
    # 输出文件: figures/generated/chapter_15/ch15_frb_faraday_foreground.pdf
    draw_figure('ch15_frb_faraday_foreground.pdf', OUTDIR)

    # 图 6: 脉冲星阵列中的共同窄带信号。左图是同一 Earth term 加不同 pulsar term；
    # 右图是标量势振荡模型中的简化相关矩阵。
    # 输出文件: figures/generated/chapter_15/ch15_pulsar_array_correlation.pdf
    draw_figure('ch15_pulsar_array_correlation.pdf', OUTDIR)

    # 图 7: 小尺度暗物质透镜。左图给出子晕 Einstein 角；
    # 右图把角接近程度转换为天体测量偏移量。
    # 输出文件: figures/generated/chapter_15/ch15_dark_matter_lensing.pdf
    draw_figure('ch15_dark_matter_lensing.pdf', OUTDIR)


if __name__ == "__main__":
    main()
