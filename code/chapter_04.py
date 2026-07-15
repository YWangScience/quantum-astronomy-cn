#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第 04 章图像脚本

运行方式：
    python code/chapter_04.py

输出目录：
    figures/generated/chapter_04/

备注：
    本脚本只生成本章需要的公式图。每张图的注释说明它对应的公式族、
    变量含义和阅读方式。默认参数用于展示标度关系，不代表某一次真实观测。
"""

from __future__ import annotations

from pathlib import Path

from plot_recipes import draw_figure
from plot_style import ROOT


OUTDIR = ROOT / "figures" / "generated" / "chapter_04"


def main() -> None:

    # 图 1: Mandel Q 参数展示同一平均计数下，计数方差如何改变零延迟二阶相干。
    # 横轴是一个时间门内的平均光子数 <N>，纵轴是 g2(0)=1+Q/<N>。
    # Q>0 表示热光或多模混沌光的超 Poisson 起伏，Q=0 表示相干态的 Poisson 起伏。
    # 输出文件: figures/generated/chapter_04/ch04_mandel_q_g2.pdf
    draw_figure('ch04_mandel_q_g2.pdf', OUTDIR)

    # 图 2: Siegert 关系展示热光中 |g1(tau)| 的相位记忆怎样变成 g2(tau)-1 的强度聚束峰。
    # 横轴以相干时间 tau_c 归一化，峰宽和峰高都只适用于高斯混沌场近似。
    # 输出文件: figures/generated/chapter_04/ch04_siegert_relation.pdf
    draw_figure('ch04_siegert_relation.pdf', OUTDIR)

    # 图 3: factorial moment 使用 N(N-1) 权重，去掉同一光子和自己配对的 shot-noise 项。
    # 这张图说明为什么符合计数和 g2 估计量天然使用阶乘矩，而不是普通二阶矩 N^2。
    # 输出文件: figures/generated/chapter_04/ch04_factorial_moments.pdf
    draw_figure('ch04_factorial_moments.pdf', OUTDIR)

    # 图 4: 有限时间响应把 ps 量级的真实聚束峰卷积成 ns 量级的低峰。
    # 左图比较不同响应宽度下的相关峰形，右图给出峰值随 Delta t_eff/tau_c 的稀释标度。
    # 输出文件: figures/generated/chapter_04/ch04_response_convolution.pdf
    draw_figure('ch04_response_convolution.pdf', OUTDIR)

    # 图 5: 延迟直方图估计量把真实符合直方图和移位参考直方图相减，得到 g2-1 的小 excess。
    # 横轴是探测器通道之间的时间延迟，右图的纵轴用 10^-3 标度显示聚束峰。
    # 输出文件: figures/generated/chapter_04/ch04_delay_histogram_estimator.pdf
    draw_figure('ch04_delay_histogram_estimator.pdf', OUTDIR)

    # 图 6: 单探测器自相关会被死时间挖出零延迟空洞，afterpulsing 又会在非零延迟制造假峰；分束后的交叉相关可把这些仪器效应和真实热光峰分开。
    # 输出文件: figures/generated/chapter_04/ch04_deadtime_pileup_bias.pdf
    draw_figure('ch04_deadtime_pileup_bias.pdf', OUTDIR)

    # 图 7: 三台望远镜的三阶强度相关包含 gamma12 gamma23 gamma31 的实部，因此对闭合相位敏感。
    # 输出文件: figures/generated/chapter_04/ch04_g3_closure_phase.pdf
    draw_figure('ch04_g3_closure_phase.pdf', OUTDIR)

    # 图 8: 频率和偏振分辨的 g2 可写成跨通道矩阵。谱线通道、同偏振通道和跨偏振通道有不同的 excess 幅度。
    # 输出文件: figures/generated/chapter_04/ch04_frequency_polarization_matrix.pdf
    draw_figure('ch04_frequency_polarization_matrix.pdf', OUTDIR)


if __name__ == "__main__":
    main()
