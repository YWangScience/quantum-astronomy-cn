#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第 11 章图像脚本

运行方式：
    python code/chapter_11.py

输出目录：
    figures/generated/chapter_11/

备注：
    本脚本只生成本章需要的公式图。每张图的注释说明它对应的公式族、
    变量含义和阅读方式。默认参数用于展示标度关系，不代表某一次真实观测。
"""

from __future__ import annotations

from pathlib import Path

from plot_recipes import draw_figure
from plot_style import ROOT


OUTDIR = ROOT / "figures" / "generated" / "chapter_11"


def main() -> None:

    # 图 1: 白矮星的质量-半径关系和引力红移标度。
    # 半径曲线采用 Nauenberg 近似，展示电子简并压导致的 R 随 M 增大而减小。
    # 右图把相同关系写成 Balmer 线可测的 v_gr=GM/(Rc)。
    # 输出文件: figures/generated/chapter_11/ch11_white_dwarf_mass_radius.pdf
    draw_figure('ch11_white_dwarf_mass_radius.pdf', OUTDIR)

    # 图 2: 磁激变变星的 P_spin/P_orb--磁矩参数图。
    # 阴影区对应盘状、流状和环状/同步吸积的近似分界，用来解释相位分辨光变。
    # 输出文件: figures/generated/chapter_11/ch11_magnetic_cv_flow_map.pdf
    draw_figure('ch11_magnetic_cv_flow_map.pdf', OUTDIR)

    # 图 3: 光柱半径 R_LC=cP/2pi 的数量级，以及 Crab 型相位折叠光变。
    # 这张图把自转周期、磁层大小和事件表中的相位窗联系起来。
    # 输出文件: figures/generated/chapter_11/ch11_light_cylinder_phase.pdf
    draw_figure('ch11_light_cylinder_phase.pdf', OUTDIR)

    # 图 4: 旋转矢量模型下的 Q/I、U/I 相位曲线和 Q-U 轨迹。
    # 读图时应把偏振度和偏振角看成同一组 Stokes 事件统计的两个投影。
    # 输出文件: figures/generated/chapter_11/ch11_stokes_qu_track.pdf
    draw_figure('ch11_stokes_qu_track.pdf', OUTDIR)

    # 图 5: 4U 0142+61 的 IXPE 量级偏振能量依赖。
    # 低能和高能的偏振角相差约 90 度，中间能段偏振度降到探测灵敏度附近。
    # 输出文件: figures/generated/chapter_11/ch11_birefringence_energy.pdf
    draw_figure('ch11_birefringence_energy.pdf', OUTDIR)

    # 图 6: 热斑光变对中子星紧致度的响应。
    # 引力光弯曲使背面区域也可能可见，紧致度越大，脉冲轮廓越平滑。
    # 输出文件: figures/generated/chapter_11/ch11_hotspot_lightcurve.pdf
    draw_figure('ch11_hotspot_lightcurve.pdf', OUTDIR)


if __name__ == "__main__":
    main()
