#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第 18 章图像脚本

运行方式：
    python code/chapter_18.py

输出目录：
    figures/generated/chapter_18/

备注：
    本脚本只生成本章需要的公式图。每张图的注释说明它对应的公式族、
    变量含义和阅读方式。默认参数用于展示标度关系，不代表某一次真实观测。
"""

from __future__ import annotations

from pathlib import Path

from plot_recipes import draw_figure
from plot_style import ROOT


OUTDIR = ROOT / "figures" / "generated" / "chapter_18"


def main() -> None:

    # 图 1: 把 AB 星等转换为窄带光子率，显示口径、效率和星等如何决定事件表的原始计数。
    # 输出文件: figures/generated/chapter_18/ch18_photon_rate_magnitude.pdf
    draw_figure('ch18_photon_rate_magnitude.pdf', OUTDIR)

    # 图 2: 由光学相干时间和电子时间分辨率估算零基线相关 contrast，被滤光片带宽和采样时间共同稀释。
    # 输出文件: figures/generated/chapter_18/ch18_coherence_dilution.pdf
    draw_figure('ch18_coherence_dilution.pdf', OUTDIR)

    # 图 3: 使用 Hanbury Brown 的强度干涉 SNR 标度，把目标星等和积分时间转成是否可检出的等值线。
    # 输出文件: figures/generated/chapter_18/ch18_snr_heatmap.pdf
    draw_figure('ch18_snr_heatmap.pdf', OUTDIR)

    # 图 4: 对均匀圆盘模型画出 |V|^2 与基线的关系，并用导数显示哪些基线最能约束角直径。
    # 输出文件: figures/generated/chapter_18/ch18_visibility_fisher.pdf
    draw_figure('ch18_visibility_fisher.pdf', OUTDIR)

    # 图 5: 用简化阵列几何比较 4 台望远镜和多台 CTA 型望远镜的 uv 覆盖密度。
    # 输出文件: figures/generated/chapter_18/ch18_uv_coverage.pdf
    draw_figure('ch18_uv_coverage.pdf', OUTDIR)

    # 图 6: 背景光和暗电流按比例稀释相关峰，off-source 观测用于估计修正因子和系统误差。
    # 输出文件: figures/generated/chapter_18/ch18_background_dilution.pdf
    draw_figure('ch18_background_dilution.pdf', OUTDIR)

    # 图 7: 统计误差随时间下降，但背景、时间、校准和模型项形成系统误差平台。
    # 输出文件: figures/generated/chapter_18/ch18_error_budget.pdf
    draw_figure('ch18_error_budget.pdf', OUTDIR)


if __name__ == "__main__":
    main()
