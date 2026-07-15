#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""教学版第 04 章（量子力学与谐振子：阶梯算符）图像脚本。

运行方式：
    python code/edu_ch04.py

输出目录：
    figures/generated/edu_ch04/

坐标轴用英文/数学记号，物理解释见对应 LaTeX 图注。默认参数只用于展示
结构关系（等间距能级、零点能、相空间形状），不代表某一次真实测量。
"""

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

from plot_style import (
    ROOT,
    apply_nature_style,
    clean_axis,
    panel_label,
    save_figure,
    COLORS,
)

OUTDIR = ROOT / "figures" / "generated" / "edu_ch04"


def fig_energy_ladder() -> None:
    """谐振子势阱 + 等间距能级 E_n = (n+1/2) hbar omega。"""
    apply_nature_style()
    fig, ax = plt.subplots(figsize=(4.6, 3.7))

    x = np.linspace(-3.7, 3.7, 500)
    ax.plot(x, 0.5 * x ** 2, color=COLORS["black"], lw=1.7, zorder=3)

    nmax = 5
    for n in range(nmax + 1):
        E = n + 0.5
        xt = np.sqrt(2.0 * E)  # 经典转折点 V(x)=E
        ax.hlines(E, -xt, xt, color=COLORS["blue"], lw=1.35, zorder=4)
        ax.text(-xt - 0.18, E, rf"$E_{{{n}}}$", va="center", ha="right",
                fontsize=7.6, color=COLORS["blue"])

    # 零点能标注
    ax.annotate(r"$E_0=\frac{1}{2}\hbar\omega$ (zero point)",
                xy=(0.0, 0.5), xytext=(0.55, 1.55),
                fontsize=7.4, color=COLORS["orange"],
                arrowprops=dict(arrowstyle="->", color=COLORS["orange"], lw=1.0))

    # 相邻能级间隔 hbar omega（取 E_3 与 E_4 之间，转折点足够宽）
    xa = 2.35
    ax.annotate("", xy=(xa, 4.5), xytext=(xa, 3.5),
                arrowprops=dict(arrowstyle="<->", color=COLORS["green"], lw=1.2))
    ax.text(xa + 0.12, 4.0, r"$\hbar\omega$", color=COLORS["green"],
            fontsize=8.4, va="center", ha="left")

    # 阶梯算符：a^dagger 上一格，a 下一格
    ax.annotate("", xy=(-0.55, 2.5), xytext=(-0.55, 1.5),
                arrowprops=dict(arrowstyle="->", color=COLORS["purple"], lw=1.3))
    ax.text(-0.72, 2.0, r"$\hat a^{\dagger}$", color=COLORS["purple"],
            fontsize=8.6, va="center", ha="right")
    ax.annotate("", xy=(0.55, 1.5), xytext=(0.55, 2.5),
                arrowprops=dict(arrowstyle="->", color=COLORS["orange"], lw=1.3))
    ax.text(0.72, 2.0, r"$\hat a$", color=COLORS["orange"],
            fontsize=8.6, va="center", ha="left")

    ax.set_xlim(-4.9, 4.2)
    ax.set_ylim(0, 6.5)
    ax.set_xlabel(r"position $x$")
    ax.set_ylabel(r"energy $E\,/\,\hbar\omega$")
    ax.set_yticks(range(0, 7))
    clean_axis(ax)
    save_figure(fig, OUTDIR, "e04_energy_ladder.pdf")


def _annulus(ax, R, width, color, alpha):
    th = np.linspace(0, 2 * np.pi, 240)
    r_out, r_in = R + width / 2.0, R - width / 2.0
    xs = np.concatenate([r_out * np.cos(th), r_in * np.cos(th[::-1])])
    ys = np.concatenate([r_out * np.sin(th), r_in * np.sin(th[::-1])])
    ax.fill(xs, ys, color=color, alpha=alpha, lw=0.0)


def fig_phase_space_states() -> None:
    """相空间：数态是均匀的环，相干态是绕圈平移的紧凑光斑。"""
    apply_nature_style()
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 3.4))

    lim = 4.2
    for ax in axes:
        ax.axhline(0, color=COLORS["grey"], lw=0.7, zorder=1)
        ax.axvline(0, color=COLORS["grey"], lw=0.7, zorder=1)
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_aspect("equal")
        ax.set_xlabel(r"$x \;\propto\; \hat a+\hat a^{\dagger}$")
        ax.set_ylabel(r"$p \;\propto\; \hat a-\hat a^{\dagger}$")
        clean_axis(ax)

    # (a) 数态 |n>：均匀模糊的整圈环，圆心在原点
    R = np.sqrt(2 * 3 + 1)  # n=3
    _annulus(axes[0], R, 0.9, COLORS["blue"], 0.30)
    th = np.linspace(0, 2 * np.pi, 200)
    axes[0].plot(R * np.cos(th), R * np.sin(th), color=COLORS["blue"], lw=1.0, alpha=0.8)
    axes[0].plot(0, 0, marker="+", color=COLORS["black"], ms=7, mew=1.3)
    axes[0].set_title(r"number state $|n\rangle$  ($\langle x\rangle=\langle p\rangle=0$)",
                      fontsize=8.2)

    # (b) 相干态 |alpha>：钉在圆周上的紧凑光斑，沿圆周旋转
    alpha_mag, alpha_ang = 2.7, np.deg2rad(38)
    x0, y0 = alpha_mag * np.cos(alpha_ang), alpha_mag * np.sin(alpha_ang)
    axes[1].plot(alpha_mag * np.cos(th), alpha_mag * np.sin(th),
                 color=COLORS["grey"], lw=0.9, ls="--")
    for r, a in [(0.85, 0.18), (0.6, 0.30), (0.38, 0.5)]:
        axes[1].add_patch(Circle((x0, y0), r, color=COLORS["orange"], alpha=a, lw=0))
    # 旋转箭头
    ang = np.linspace(alpha_ang + 0.15, alpha_ang + 0.95, 40)
    axes[1].plot(alpha_mag * np.cos(ang), alpha_mag * np.sin(ang),
                 color=COLORS["black"], lw=1.1)
    axes[1].annotate("", xy=(alpha_mag * np.cos(ang[-1]), alpha_mag * np.sin(ang[-1])),
                     xytext=(alpha_mag * np.cos(ang[-4]), alpha_mag * np.sin(ang[-4])),
                     arrowprops=dict(arrowstyle="->", color=COLORS["black"], lw=1.1))
    # |alpha| 半径线与相位角
    axes[1].plot([0, x0], [0, y0], color=COLORS["black"], lw=0.9, ls=":")
    axes[1].text(x0 * 0.5 - 0.15, y0 * 0.5 + 0.28, r"$|\alpha|$",
                 fontsize=8.0, color=COLORS["black"])
    axes[1].text(1.15, 0.32, r"$\arg\alpha$", fontsize=7.6, color=COLORS["black"])
    axes[1].set_title(r"coherent state $|\alpha\rangle$ (rotates along the circle)",
                      fontsize=8.2)

    panel_label(axes[0], "a")
    panel_label(axes[1], "b")
    save_figure(fig, OUTDIR, "e04_phase_space_states.pdf")


def main() -> None:
    fig_energy_ladder()
    fig_phase_space_states()


if __name__ == "__main__":
    main()
