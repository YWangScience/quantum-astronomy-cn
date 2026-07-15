#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第 07 章图像脚本

运行方式：
    python code/chapter_07.py

输出目录：
    figures/generated/chapter_07/

备注：
    本脚本只生成本章需要的公式图。每张图的注释说明它对应的公式族、
    变量含义和阅读方式。默认参数用于展示标度关系，不代表某一次真实观测。
"""

from __future__ import annotations

from pathlib import Path

from plot_recipes import draw_figure
from plot_style import ROOT


OUTDIR = ROOT / "figures" / "generated" / "chapter_07"


def main() -> None:

    # 图 1: 非齐次 Poisson 过程把瞬时光子率映射为事件到达时间。
    # 似然函数由事件所在位置的 rate 项和整段观测的积分 rate 项共同决定。
    # 输出文件: figures/generated/chapter_07/ch07_poisson_likelihood.pdf
    draw_figure('ch07_poisson_likelihood.pdf', OUTDIR)

    # 图 2: 时移背景估计把一个通道平移到非物理延迟，得到 accidental pairs 的形状。
    # 中央峰和时移背景之差才是用于估计相关超额的信号。
    # 输出文件: figures/generated/chapter_07/ch07_time_shift_background.pdf
    draw_figure('ch07_time_shift_background.pdf', OUTDIR)

    # 图 3: 事件对相关不能直接用全量双循环；排序窗口和 FFT 相关对应不同数据表示。
    # 这张图只展示复杂度标度，不代表某台机器的实际 wall time。
    # 输出文件: figures/generated/chapter_07/ch07_correlator_scaling.pdf
    draw_figure('ch07_correlator_scaling.pdf', OUTDIR)

    # 图 4: 多基线、多延迟 bin 或多波段结果需要协方差矩阵。
    # 对角项是单个数据点方差，非对角项来自共享通道、共同背景估计和系统串扰。
    # 输出文件: figures/generated/chapter_07/ch07_covariance_matrix.pdf
    draw_figure('ch07_covariance_matrix.pdf', OUTDIR)

    # 图 5: 参数误差随 Fisher 信息增加而下降，但系统误差地板会终止根号光子数标度。
    # 对观测设计而言，统计误差曲线和系统地板的交点给出继续积分的收益边界。
    # 输出文件: figures/generated/chapter_07/ch07_fisher_scaling.pdf
    draw_figure('ch07_fisher_scaling.pdf', OUTDIR)


if __name__ == "__main__":
    main()
