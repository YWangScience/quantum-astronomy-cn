#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第 13 章图像脚本

运行方式：
    python code/chapter_13.py

输出目录：
    figures/generated/chapter_13/

备注：
    本脚本只生成本章需要的公式图。每张图的注释说明它对应的公式族、
    变量含义和阅读方式。默认参数用于展示标度关系，不代表某一次真实观测。
"""

from __future__ import annotations

from pathlib import Path

from plot_recipes import draw_figure
from plot_style import ROOT


OUTDIR = ROOT / "figures" / "generated" / "chapter_13"


def main() -> None:

    # 图 1: 非齐次 Poisson 事件表。上半部分画真实光子率和单光子到达时刻，
    # 右半部分画触发时间 t0 与衰减时标 tau 的相对似然，说明背景和少量光子怎样共同限制模型。
    # 输出文件: figures/generated/chapter_13/ch13_transient_event_likelihood.pdf
    draw_figure('ch13_transient_event_likelihood.pdf', OUTDIR)

    # 图 2: 膨胀火球角半径 theta=v(t-t0)/D。三条曲线分别代表银河系新星、
    # 低红移 Type Ia 超新星和 GW170817 类千新星；虚线给出不同光学基线的角分辨标度。
    # 输出文件: figures/generated/chapter_13/ch13_expanding_fireball_resolution.pdf
    draw_figure('ch13_expanding_fireball_resolution.pdf', OUTDIR)

    # 图 3: 多信使延迟。左图用对数时间轴比较 GW、gamma、光学和后期 X/radio 信号；
    # 右图把同一延迟换算成 40 Mpc 距离上的传播速度差上限。
    # 输出文件: figures/generated/chapter_13/ch13_multimessenger_delay.pdf
    draw_figure('ch13_multimessenger_delay.pdf', OUTDIR)

    # 图 4: 千新星的颜色演化和扩散时标。左图用黑体光谱展示从蓝到红的快速演化；
    # 右图展示 opacity、ejecta mass 和 velocity 怎样决定峰值时间。
    # 输出文件: figures/generated/chapter_13/ch13_kilonova_color_evolution.pdf
    draw_figure('ch13_kilonova_color_evolution.pdf', OUTDIR)

    # 图 5: GRB 余辉同步辐射。左图标出 nu_m 与 nu_c 两个 break；
    # 右图展示光学和 X-ray 光变及 jet break 后的变陡。
    # 输出文件: figures/generated/chapter_13/ch13_afterglow_synchrotron_breaks.pdf
    draw_figure('ch13_afterglow_synchrotron_breaks.pdf', OUTDIR)

    # 图 6: TDE 回落和再处理。左图画 t^{-5/3} fallback 与 Eddington 标度；
    # 右图画光学/UV 黑体半径收缩和温度升高的典型演化。
    # 输出文件: figures/generated/chapter_13/ch13_tde_fallback_reprocessing.pdf
    draw_figure('ch13_tde_fallback_reprocessing.pdf', OUTDIR)


if __name__ == "__main__":
    main()
