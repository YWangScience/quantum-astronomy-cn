#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第 14 章图像脚本

运行方式：
    python code/chapter_14.py

输出目录：
    figures/generated/chapter_14/

备注：
    本脚本只生成本章需要的公式图。每张图的注释说明它对应的公式族、
    变量含义和阅读方式。默认参数用于展示标度关系，不代表某一次真实观测。
"""

from __future__ import annotations

from pathlib import Path

from plot_recipes import draw_figure
from plot_style import ROOT


OUTDIR = ROOT / "figures" / "generated" / "chapter_14"


def main() -> None:

    # 图 1: 冷等离子体色散。左图展示同一参考频率下的到达时间延迟；
    # 右图把银河系盘、银晕、宿主星系和宇宙学等离子体的 DM 贡献拆开。
    # 输出文件: figures/generated/chapter_14/ch14_dispersion_delay.pdf
    draw_figure('ch14_dispersion_delay.pdf', OUTDIR)

    # 图 2: Faraday 旋转。偏振角对 lambda^2 的斜率给出 RM；
    # 若 RM 与 DM 来自同一区域，二者的比值可估计视线平均磁场。
    # 输出文件: figures/generated/chapter_14/ch14_faraday_rotation.pdf
    draw_figure('ch14_faraday_rotation.pdf', OUTDIR)

    # 图 3: 多径散射。左图显示指数尾如何展宽短脉冲；
    # 右图显示经验散射时间随 DM 和频率的强烈变化。
    # 输出文件: figures/generated/chapter_14/ch14_scattering_broadening.pdf
    draw_figure('ch14_scattering_broadening.pdf', OUTDIR)

    # 图 4: 尘埃消光和偏振。左图比较不同 R_V 的平均银河系消光曲线；
    # 右图展示 Serkowski 定律下偏振效率峰值随波长移动。
    # 输出文件: figures/generated/chapter_14/ch14_dust_extinction_polarization.pdf
    draw_figure('ch14_dust_extinction_polarization.pdf', OUTDIR)

    # 图 5: 强引力透镜。左图给出 Fermat 到达时间面和点质量双像；
    # 右图用 4GM/c^3 展示透镜质量对应的基本延迟尺度。
    # 输出文件: figures/generated/chapter_14/ch14_lensing_time_delay.pdf
    draw_figure('ch14_lensing_time_delay.pdf', OUTDIR)

    # 图 6: 波动光学透镜。左图显示多像干涉在频域形成的条纹；
    # 右图给出 w=8*pi*GM*f/c^3 的几何光学与波动光学分界。
    # 输出文件: figures/generated/chapter_14/ch14_wave_lensing_interference.pdf
    draw_figure('ch14_wave_lensing_interference.pdf', OUTDIR)

    # 图 7: Cosmic Bell 实验的因果结构。远处恒星或类星体光子决定测量设置，
    # 将可能共同原因的时空区域推向更早宇宙。
    # 输出文件: figures/generated/chapter_14/ch14_cosmic_bell_lightcones.pdf
    draw_figure('ch14_cosmic_bell_lightcones.pdf', OUTDIR)


if __name__ == "__main__":
    main()
