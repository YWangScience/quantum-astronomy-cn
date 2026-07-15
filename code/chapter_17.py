#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第 17 章图像脚本

运行方式：
    python code/chapter_17.py

输出目录：
    figures/generated/chapter_17/

备注：
    本脚本只生成本章需要的公式图。每张图的注释说明它对应的公式族、
    变量含义和阅读方式。默认参数用于展示标度关系，不代表某一次真实观测。
"""

from __future__ import annotations

from pathlib import Path

from plot_recipes import draw_figure
from plot_style import ROOT


OUTDIR = ROOT / "figures" / "generated" / "chapter_17"


def main() -> None:

    # 图 1: 三种长基线路线的核心限制。左图比较直接传输星光时的链路损耗；
    # 右图把基线转换成光学角分辨率，说明为什么 km 以上基线有科学吸引力。
    # 输出文件: figures/generated/chapter_17/ch17_architecture_loss.pdf
    draw_figure('ch17_architecture_loss.pdf', OUTDIR)

    # 图 2: 纠缠资源率和存储时间。左图把可接受的天体事件率转换成 Bell pair 需求；
    # 右图把基线长度转换成最小通信/存储时间。
    # 输出文件: figures/generated/chapter_17/ch17_entanglement_resources.pdf
    draw_figure('ch17_entanglement_resources.pdf', OUTDIR)

    # 图 3: time-bin 编码的资源缩放。对弱光源，二进制时间编码把 Bell pair 和 memory qubit
    # 需求从 N 个时间 bin 降到 log2(N+1) 个。
    # 输出文件: figures/generated/chapter_17/ch17_timebin_scaling.pdf
    draw_figure('ch17_timebin_scaling.pdf', OUTDIR)

    # 图 4: 链路和存储共同决定有效量子资源质量。左图是通道损耗；
    # 右图是不同 T2 下的存储相干因子。
    # 输出文件: figures/generated/chapter_17/ch17_fidelity_distance.pdf
    draw_figure('ch17_fidelity_distance.pdf', OUTDIR)

    # 图 5: 非局域相位测量的 Fisher 信息。Stas 等实验中的核心标度是
    # FI 正比于 herald 成功概率乘以 visibility 的平方。
    # 输出文件: figures/generated/chapter_17/ch17_fisher_visibility.pdf
    draw_figure('ch17_fisher_visibility.pdf', OUTDIR)

    # 图 6: 总体资源空间。横轴是纠缠率，纵轴是存储时间；
    # 白线标出不同基线的 B/c 时间，散点标出实验和远期目标量级。
    # 输出文件: figures/generated/chapter_17/ch17_network_parameter_space.pdf
    draw_figure('ch17_network_parameter_space.pdf', OUTDIR)


if __name__ == "__main__":
    main()
