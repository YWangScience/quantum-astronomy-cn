#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第 20 章图像脚本

运行方式：
    python code/chapter_20.py

输出目录：
    figures/generated/chapter_20/

备注：
    本脚本只生成本章需要的公式图。每张图的注释说明它对应的公式族、
    变量含义和阅读方式。默认参数用于展示标度关系，不代表某一次真实观测。
"""

from __future__ import annotations

from pathlib import Path

from plot_recipes import draw_figure
from plot_style import ROOT


OUTDIR = ROOT / "figures" / "generated" / "chapter_20"


def main() -> None:

    # 图 1: HBT 桌面实验的原始符合直方图和归一化 g2。左图显示同时时间轴与 time-shift 背景，右图显示扣除仪器慢漂移后的热光聚束峰。
    # 输出文件: figures/generated/chapter_20/ch20_hbt_lab_histogram.pdf
    draw_figure('ch20_hbt_lab_histogram.pdf', OUTDIR)

    # 图 2: 非齐次 Poisson 事件表。事件保留到达时间、等效波长通道和质量标记，随后才投影成光变曲线或筛选后的计数率。
    # 输出文件: figures/generated/chapter_20/ch20_event_table_simulation.pdf
    draw_figure('ch20_event_table_simulation.pdf', OUTDIR)

    # 图 3: 均匀圆盘强度干涉拟合。基线上的 |V|^2 点给出角直径后验，第一零点附近的点对直径最敏感。
    # 输出文件: figures/generated/chapter_20/ch20_uniform_disk_fit.pdf
    draw_figure('ch20_uniform_disk_fit.pdf', OUTDIR)

    # 图 4: 双星可见度练习。通量比控制振荡深度，轨道相位通过投影分离改变固定基线上的 |V|^2。
    # 输出文件: figures/generated/chapter_20/ch20_binary_visibility.pdf
    draw_figure('ch20_binary_visibility.pdf', OUTDIR)

    # 图 5: 多望远镜相关器标度。望远镜数决定基线数，时间 bin 和光谱通道数决定单路数据流压力。
    # 输出文件: figures/generated/chapter_20/ch20_correlator_scaling.pdf
    draw_figure('ch20_correlator_scaling.pdf', OUTDIR)

    # 图 6: SPADE 计算实验。直接成像在小分离处 Fisher 信息下降，理想模式排序保持接近常数，并把信息放入高阶模式概率。
    # 输出文件: figures/generated/chapter_20/ch20_spade_exercise.pdf
    draw_figure('ch20_spade_exercise.pdf', OUTDIR)

    # 图 7: Type Ia 超新星角直径距离 toy model。速度模型给出物理半径，强度干涉给出角半径，两者合成距离后验。
    # 输出文件: figures/generated/chapter_20/ch20_typeia_distance_posterior.pdf
    draw_figure('ch20_typeia_distance_posterior.pdf', OUTDIR)


if __name__ == "__main__":
    main()
