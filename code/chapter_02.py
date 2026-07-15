#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第 02 章图像脚本

运行方式：
    python code/chapter_02.py

输出目录：
    figures/generated/chapter_02/

备注：
    本脚本只生成本章需要的公式图。每张图的注释说明它对应的公式族、
    变量含义和阅读方式。默认参数用于展示标度关系，不代表某一次真实观测。
"""

from __future__ import annotations

from pathlib import Path

from plot_recipes import draw_figure
from plot_style import ROOT


OUTDIR = ROOT / "figures" / "generated" / "chapter_02"


def main() -> None:

    # 图 1: 两束光可以有相同的平均强度和光变曲线，却有不同的二阶相干函数。平均强度只记录一阶统计量，光子到达时间之间的联合概率保存在 g2 中。
    # 输出文件: figures/generated/chapter_02/ch02_mean_intensity_vs_correlation.pdf
    draw_figure('ch02_mean_intensity_vs_correlation.pdf', OUTDIR)

    # 图 2: 光子事件表把时间、望远镜位置、频率通道和偏振标签放在同一个数据结构中。不同的边缘化方式分别给出光变曲线、谱线、偏振量和强度相关函数。
    # 输出文件: figures/generated/chapter_02/ch02_event_table_information.pdf
    draw_figure('ch02_event_table_information.pdf', OUTDIR)

    # 图 3: 观测到的二阶相关对比度会被有效模式数、光谱带宽和时间 bin 同时稀释。
    # 左图展示 \(M\) 个独立模式和 \(\Delta t/\tau_c\) 对 \(g^{(2)}_{\rm obs}(0)-1\) 的压低；
    # 右图把 \(\tau_c\simeq1/\Delta\nu\) 代入，显示光学带宽和电子时间分辨率的可行区域。
    # 输出文件: figures/generated/chapter_02/ch02_contrast_dilution.pdf
    draw_figure('ch02_contrast_dilution.pdf', OUTDIR)

    # 图 4: 从 HBT、Narrabri 到现代 Cherenkov 阵列的时间线。图中突出沉寂期的工程瓶颈，以及高速探测、数字相关器和 IACT 大面积镜面带来的复兴。
    # 输出文件: figures/generated/chapter_02/ch02_revival_timeline.pdf
    draw_figure('ch02_revival_timeline.pdf', OUTDIR)

    # 图 5: 第一代量子天文学科学问题的可行性和新增信息量。点的大小和颜色表示进入常规观测所需的时间尺度。
    # 输出文件: figures/generated/chapter_02/ch02_science_case_map.pdf
    draw_figure('ch02_science_case_map.pdf', OUTDIR)


if __name__ == "__main__":
    main()
