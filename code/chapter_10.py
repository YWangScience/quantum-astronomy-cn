#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第 10 章图像脚本

运行方式：
    python code/chapter_10.py

输出目录：
    figures/generated/chapter_10/

备注：
    本脚本只生成本章需要的公式图。每张图的注释说明它对应的公式族、
    变量含义和阅读方式。默认参数用于展示标度关系，不代表某一次真实观测。
"""

from __future__ import annotations

from pathlib import Path

from plot_recipes import draw_figure
from plot_style import ROOT


OUTDIR = ROOT / "figures" / "generated" / "chapter_10"


def main() -> None:

    # 图 1: 均匀圆盘恒星的平方可见度随基线下降。波长取 416 nm，
    # 灰色区域标出 VERITAS 量级的投影基线范围。
    # 输出文件: figures/generated/chapter_10/ch10_stellar_diameter_visibility.pdf
    draw_figure('ch10_stellar_diameter_visibility.pdf', OUTDIR)

    # 图 2: 双星的 |V|^2 振荡。角分离决定振荡周期，流量比决定振幅。
    # 输出文件: figures/generated/chapter_10/ch10_binary_visibility.pdf
    draw_figure('ch10_binary_visibility.pdf', OUTDIR)

    # 图 3: 线性边缘昏暗亮度分布及其由径向 Hankel 积分得到的 |V|^2。
    # 输出文件: figures/generated/chapter_10/ch10_limb_darkening.pdf
    draw_figure('ch10_limb_darkening.pdf', OUTDIR)

    # 图 4: 快速自转造成椭圆光球；不同位置角的基线看到不同的有效角直径。
    # 参数采用 gamma Cas 量级的轴比，仅用于展示标度。
    # 输出文件: figures/generated/chapter_10/ch10_rotation_oblateness.pdf
    draw_figure('ch10_rotation_oblateness.pdf', OUTDIR)

    # 图 5: 由 F_bol 和角直径推导 T_eff 时的误差传播。
    # 角直径误差进入系数为 1/2，因此常常主导有效温度误差。
    # 输出文件: figures/generated/chapter_10/ch10_teff_error_budget.pdf
    draw_figure('ch10_teff_error_budget.pdf', OUTDIR)


if __name__ == "__main__":
    main()
