#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第 21 章图像脚本

运行方式：
    python code/chapter_21.py

输出目录：
    figures/generated/chapter_21/

备注：
    本脚本只生成本章需要的公式图。每张图的注释说明它对应的公式族、
    变量含义和阅读方式。默认参数用于展示标度关系，不代表某一次真实观测。
"""

from __future__ import annotations

from pathlib import Path

from plot_recipes import draw_figure
from plot_style import ROOT


OUTDIR = ROOT / "figures" / "generated" / "chapter_21"


def main() -> None:

    # 图 1: 时间 bin 和有效模式数会稀释热光聚束。右图把滤光片带宽换成相干时间，显示窄带滤光和快速电子学的共同作用。
    # 输出文件: figures/generated/chapter_21/ch21_g2_scaling_mistake.pdf
    draw_figure('ch21_g2_scaling_mistake.pdf', OUTDIR)

    # 图 2: 单个 Poisson 尾部事件在大量搜索 bin 中会变常见。右图把单次 p 值转换成全局 false-alarm 概率。
    # 输出文件: figures/generated/chapter_21/ch21_poisson_false_alarm.pdf
    draw_figure('ch21_poisson_false_alarm.pdf', OUTDIR)

    # 图 3: 电子串扰和校准残差可以比天体聚束峰更大。积分时间只能压低统计误差，不能自动消除系统误差地板。
    # 输出文件: figures/generated/chapter_21/ch21_calibration_artifacts.pdf
    draw_figure('ch21_calibration_artifacts.pdf', OUTDIR)

    # 图 4: 只保留 |V|^2 会丢掉镜像方向的相位信息。相位恢复需要先验、多基线或高阶相关，而不是自动完成。
    # 输出文件: figures/generated/chapter_21/ch21_phase_loss.pdf
    draw_figure('ch21_phase_loss.pdf', OUTDIR)

    # 图 5: 量子超分辨仍然受光子数和模式误差限制。理想模式排序降低统计误差，但系统误差地板会终止继续改进。
    # 输出文件: figures/generated/chapter_21/ch21_superresolution_budget.pdf
    draw_figure('ch21_superresolution_budget.pdf', OUTDIR)

    # 图 6: 非 Poisson 统计有多种普通来源。变源、死时间和 afterpulsing 在 Fano 因子和短延迟相关中留下不同形状。
    # 输出文件: figures/generated/chapter_21/ch21_nonpoisson_diagnostics.pdf
    draw_figure('ch21_nonpoisson_diagnostics.pdf', OUTDIR)

    # 图 7: 天体 maser/laser 的统计由线、连续谱和谱宽共同决定。理想相干线、未饱和强度噪声和热背景会给出不同 g2。
    # 输出文件: figures/generated/chapter_21/ch21_maser_mixed_statistics.pdf
    draw_figure('ch21_maser_mixed_statistics.pdf', OUTDIR)


if __name__ == "__main__":
    main()
