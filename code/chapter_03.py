#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第 03 章图像脚本

运行方式：
    python code/chapter_03.py

输出目录：
    figures/generated/chapter_03/

备注：
    本脚本只生成本章需要的公式图。每张图的注释说明它对应的公式族、
    变量含义和阅读方式。默认参数用于展示标度关系，不代表某一次真实观测。
"""

from __future__ import annotations

from pathlib import Path

from plot_recipes import draw_figure
from plot_style import ROOT


OUTDIR = ROOT / "figures" / "generated" / "chapter_03"


def main() -> None:

    # 图 1: 相干态、热态和压缩态在相空间中的示意。相干态近似圆形最小不确定度分布，热态更宽，压缩态在一个正交量上变窄但在另一个正交量上变宽。
    # 输出文件: figures/generated/chapter_03/ch03_phase_space_states.pdf
    draw_figure('ch03_phase_space_states.pdf', OUTDIR)

    # 图 2: 数态、相干态和热态的单模光子数分布。相同平均光子数下，方差和高光子数尾部不同，直接影响 g2 和计数噪声。
    # 输出文件: figures/generated/chapter_03/ch03_state_count_distributions.pdf
    draw_figure('ch03_state_count_distributions.pdf', OUTDIR)

    # 图 3: 黑体亮温对应的单模占有数 nbar_nu。它说明光学恒星光通常落在弱热光区，而长波段或高亮温 maser 可达到高占有数。
    # 输出文件: figures/generated/chapter_03/ch03_blackbody_mode_occupation.pdf
    draw_figure('ch03_blackbody_mode_occupation.pdf', OUTDIR)

    # 图 4: 有限时间分辨率会稀释热光聚束信号。当时间 bin 大于相干时间时，测得的 g2 峰值按相干时间与 bin 宽的比值下降；多模平均会进一步降低对比度。
    # 输出文件: figures/generated/chapter_03/ch03_coherence_time_dilution.pdf
    draw_figure('ch03_coherence_time_dilution.pdf', OUTDIR)

    # 图 5: 有限探测效率会降低源计数率；天空背景和暗计数会把归一化相关幅度按源光子比例平方稀释。
    # 输出文件: figures/generated/chapter_03/ch03_detection_loss_background.pdf
    draw_figure('ch03_detection_loss_background.pdf', OUTDIR)

    # 图 6: 观测到的 g2 会被背景和多源混合拉回 1。即使单个发射体反聚束，源光子比例不足或独立发射体很多时，非经典边界也很快被淹没。
    # 输出文件: figures/generated/chapter_03/ch03_nonclassical_mixing_boundary.pdf
    draw_figure('ch03_nonclassical_mixing_boundary.pdf', OUTDIR)


if __name__ == "__main__":
    main()
