#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第 06 章图像脚本

运行方式：
    python code/chapter_06.py

输出目录：
    figures/generated/chapter_06/

备注：
    本脚本只生成本章需要的公式图。每张图的注释说明它对应的公式族、
    变量含义和阅读方式。默认参数用于展示标度关系，不代表某一次真实观测。
"""

from __future__ import annotations

from pathlib import Path

from plot_recipes import draw_figure
from plot_style import ROOT


OUTDIR = ROOT / "figures" / "generated" / "chapter_06"


def main() -> None:

    # 图 1: 事件表从原始电子记录、标定事件到相关函数产品的三层结构。
    # 每一层都保留时间、通道和质量信息，避免在早期投影时丢失可用于校正的变量。
    # 输出文件: figures/generated/chapter_06/ch06_event_table_schema.pdf
    draw_figure('ch06_event_table_schema.pdf', OUTDIR)

    # 图 2: 不同探测器技术的典型时间抖动、暗计数和量子效率范围。
    # 横纵坐标都是数量级坐标；点的面积代表典型量子效率，不代表严格性能上限。
    # 输出文件: figures/generated/chapter_06/ch06_detector_trade_space.pdf
    draw_figure('ch06_detector_trade_space.pdf', OUTDIR)

    # 图 3: 探测器时间响应会把真实相关峰卷积变宽并降低峰值。
    # 这里保持峰面积近似不变，用来显示有限电子时间分辨率如何稀释峰高。
    # 输出文件: figures/generated/chapter_06/ch06_detector_timing_response.pdf
    draw_figure('ch06_detector_timing_response.pdf', OUTDIR)

    # 图 4: 探测器死时间会使观测计数率在高入射光子率下饱和。
    # 非延长和延长死时间模型在强光源下给出不同偏差，需要用实验标定选择模型。
    # 输出文件: figures/generated/chapter_06/ch06_deadtime_saturation.pdf
    draw_figure('ch06_deadtime_saturation.pdf', OUTDIR)

    # 图 5: 时间校正预算跨越从皮秒到数百秒的尺度。
    # 相关函数只关心相对延迟，脉冲星折叠和跨夜合并还需要绝对时间尺度和质心改正。
    # 输出文件: figures/generated/chapter_06/ch06_time_budget.pdf
    draw_figure('ch06_time_budget.pdf', OUTDIR)

    # 图 6: 光谱分辨率增加会拉长相干时间，但也会降低单个光谱通道内的光子率。
    # 这张图对应 tau_c ≈ R lambda / c 的数量级关系。
    # 输出文件: figures/generated/chapter_06/ch06_spectral_resolution_coherence.pdf
    draw_figure('ch06_spectral_resolution_coherence.pdf', OUTDIR)


if __name__ == "__main__":
    main()
