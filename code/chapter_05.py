#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第 05 章图像脚本

运行方式：
    python code/chapter_05.py

输出目录：
    figures/generated/chapter_05/

备注：
    本脚本只生成本章需要的公式图。每张图的注释说明它对应的公式族、
    变量含义和阅读方式。默认参数用于展示标度关系，不代表某一次真实观测。
"""

from __future__ import annotations

from pathlib import Path

from plot_recipes import draw_figure
from plot_style import ROOT


OUTDIR = ROOT / "figures" / "generated" / "chapter_05"


def main() -> None:

    # 图 1: van Cittert-Zernike 定理把天空亮度的形状映射为 |V|^2 曲线。
    # 均匀圆盘、Gaussian、双星和薄环在空间频率上有不同零点和振荡结构。
    # 输出文件: figures/generated/chapter_05/ch05_vcz_visibility_models.pdf
    draw_figure('ch05_vcz_visibility_models.pdf', OUTDIR)

    # 图 2: 用 416 nm 观测时，均匀圆盘的第一零点基线 B0=1.22 lambda/theta。
    # 横轴是角直径，纵轴是首次把恒星圆盘分辨到零可见度所需的投影基线。
    # 输出文件: figures/generated/chapter_05/ch05_uniform_disk_resolution.pdf
    draw_figure('ch05_uniform_disk_resolution.pdf', OUTDIR)

    # 图 3: 强度干涉信号 C12=N0|V|^2 随投影基线下降。
    # 这里 N0 取 VERITAS 416 nm 系统的典型零基线相关量级，角直径越大下降越快。
    # 输出文件: figures/generated/chapter_05/ch05_sii_signal_vs_baseline.pdf
    draw_figure('ch05_sii_signal_vs_baseline.pdf', OUTDIR)

    # 图 4: SNR 标度显示亮星、长积分和更宽电子带宽对强度干涉的重要性。
    # 曲线只展示相对比例，实际归一化还要乘以收集面积、效率和 |V|^2。
    # 输出文件: figures/generated/chapter_05/ch05_snr_scaling.pdf
    draw_figure('ch05_snr_scaling.pdf', OUTDIR)

    # 图 5: 地球自转把固定望远镜基线投影到不同的 u,v 位置。
    # 对 N 台望远镜，同时可得到 N(N-1)/2 条基线，覆盖越密，模型假设越少。
    # 输出文件: figures/generated/chapter_05/ch05_uv_coverage.pdf
    draw_figure('ch05_uv_coverage.pdf', OUTDIR)

    # 图 6: 零基线相关幅度 N0 会随夜晚、带宽、电子响应和校准状态漂移。校准偏差会直接映射成 |V|^2 的幅度偏差。
    # 输出文件: figures/generated/chapter_05/ch05_zero_baseline_calibration.pdf
    draw_figure('ch05_zero_baseline_calibration.pdf', OUTDIR)

    # 图 7: 只测 |V|^2 会丢失一阶 Fourier 相位，镜像源可以有相同的功率谱。相位恢复必须依赖先验、二维覆盖或三阶相关等额外信息。
    # 输出文件: figures/generated/chapter_05/ch05_phase_ambiguity.pdf
    draw_figure('ch05_phase_ambiguity.pdf', OUTDIR)

    # 图 8: 强度干涉角直径误差由统计、零基线、背景、模型和选择函数共同组成。现代阵列不只受 photon noise 限制。
    # 输出文件: figures/generated/chapter_05/ch05_error_budget.pdf
    draw_figure('ch05_error_budget.pdf', OUTDIR)


if __name__ == "__main__":
    main()
