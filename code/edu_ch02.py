#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""教学版第 02 章（傅里叶、带宽与相干时间）图像脚本。

运行方式：
    python code/edu_ch02.py

输出目录：
    figures/generated/edu_ch02/

坐标轴用英文/数学记号，物理解释见对应 LaTeX 图注。默认参数只用于展示
"时间越短、频谱越宽"以及"相干时间 = 1/带宽"这两条标度关系。
"""

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt

from plot_style import (
    ROOT,
    apply_nature_style,
    clean_axis,
    panel_label,
    save_figure,
    COLORS,
)

OUTDIR = ROOT / "figures" / "generated" / "edu_ch02"


def fig_wave_packet_spectrum() -> None:
    """波包越短，频谱越宽：Delta t * Delta nu ~ const。"""
    apply_nature_style()
    fig, axes = plt.subplots(2, 2, figsize=(6.7, 4.3))

    t = np.linspace(-6, 6, 2400)
    nu = np.linspace(0, 6, 2400)
    nu0 = 3.0  # 载波频率（任意单位）

    rows = [(0.62, "short wave packet"), (2.1, "long wave packet")]
    for i, (sig_t, tag) in enumerate(rows):
        env = np.exp(-t ** 2 / (2 * sig_t ** 2))
        signal = env * np.cos(2 * np.pi * nu0 * t)

        axt = axes[i, 0]
        axt.plot(t, signal, color=COLORS["blue"], lw=1.05)
        axt.plot(t, env, color=COLORS["orange"], lw=1.3, ls="--")
        axt.plot(t, -env, color=COLORS["orange"], lw=1.3, ls="--")
        axt.set_xlim(-6, 6)
        axt.set_ylim(-1.28, 1.28)
        axt.set_yticks([])
        clean_axis(axt)
        # Delta t 双箭头
        axt.annotate("", xy=(sig_t, 1.12), xytext=(-sig_t, 1.12),
                     arrowprops=dict(arrowstyle="<->", color=COLORS["orange"], lw=1.1))
        axt.text(0, 1.16, r"$\Delta t$", color=COLORS["orange"],
                 fontsize=8.0, ha="center", va="bottom")

        sig_nu = 1.0 / (2 * np.pi * sig_t)  # 频域高斯宽度
        spec = np.exp(-(nu - nu0) ** 2 / (2 * sig_nu ** 2))
        axf = axes[i, 1]
        axf.plot(nu, spec, color=COLORS["green"], lw=1.6)
        axf.fill_between(nu, spec, color=COLORS["green"], alpha=0.14)
        axf.set_xlim(0, 6)
        axf.set_ylim(0, 1.2)
        axf.set_yticks([])
        clean_axis(axf)
        axf.annotate("", xy=(nu0 + sig_nu, 1.03), xytext=(nu0 - sig_nu, 1.03),
                     arrowprops=dict(arrowstyle="<->", color=COLORS["green"], lw=1.1))
        axf.text(nu0, 1.07, r"$\Delta\nu$", color=COLORS["green"],
                 fontsize=8.0, ha="center", va="bottom")

    axes[1, 0].set_xlabel(r"time $t$")
    axes[1, 1].set_xlabel(r"frequency $\nu$")
    axes[0, 0].set_title("time domain", fontsize=8.6)
    axes[0, 1].set_title("frequency domain (spectrum)", fontsize=8.6)
    fig.text(0.5, -0.01, r"short packet $\Rightarrow$ broad spectrum;"
             r"  long packet $\Rightarrow$ narrow spectrum   "
             r"($\Delta t\,\Delta\nu \sim \mathrm{const}$)",
             ha="center", fontsize=8.0, color=COLORS["black"])

    panel_label(axes[0, 0], "a")
    panel_label(axes[0, 1], "b")
    panel_label(axes[1, 0], "c")
    panel_label(axes[1, 1], "d")
    save_figure(fig, OUTDIR, "e02_wave_packet_spectrum.pdf")


def fig_coherence_bandwidth() -> None:
    """(a) |g1| 衰减快慢由带宽决定；(b) tau_c = 1/Delta_nu。"""
    apply_nature_style()
    fig, axes = plt.subplots(1, 2, figsize=(6.7, 3.0))

    # (a) 一阶相干度随延迟衰减：窄带 -> 长相干时间；宽带 -> 短相干时间
    tau = np.linspace(0, 6, 600)
    for tau_c, name, col in [(2.4, r"narrow band (small $\Delta\nu$)", COLORS["blue"]),
                             (0.8, r"broad band (large $\Delta\nu$)", COLORS["orange"])]:
        axes[0].plot(tau, np.exp(-(tau / tau_c) ** 2), color=col, lw=1.7, label=name)
        axes[0].axvline(tau_c, color=col, lw=0.9, ls=":")
    axes[0].set_xlim(0, 6)
    axes[0].set_ylim(0, 1.05)
    axes[0].set_xlabel(r"delay $\tau$")
    axes[0].set_ylabel(r"$|g^{(1)}(\tau)|$")
    axes[0].legend(frameon=False, loc="upper right")
    axes[0].text(2.5, 0.5, r"$\tau_c$", color=COLORS["blue"], fontsize=8.2)
    clean_axis(axes[0], grid=True)
    panel_label(axes[0], "a")

    # (b) tau_c = 1/Delta_nu（log-log），标出可见光例子
    dnu = np.logspace(9, 14, 200)      # Hz
    axes[1].loglog(dnu, 1.0 / dnu, color=COLORS["green"], lw=1.8)
    ex_dnu, ex_tc = 1.2e12, 1.0 / 1.2e12  # 500 nm, 1 nm 带宽 -> ~0.8 ps
    axes[1].plot(ex_dnu, ex_tc, marker="o", ms=6, color=COLORS["orange"], zorder=5)
    axes[1].annotate(r"$\lambda=500\,$nm, $\Delta\lambda=1\,$nm" "\n"
                     r"$\Delta\nu\!\approx\!1.2\,$THz, $\tau_c\!\approx\!0.8\,$ps",
                     xy=(ex_dnu, ex_tc), xytext=(2.0e9, 3e-13),
                     fontsize=6.8, color=COLORS["black"],
                     arrowprops=dict(arrowstyle="->", color=COLORS["orange"], lw=0.9))
    axes[1].set_xlabel(r"bandwidth $\Delta\nu$ (Hz)")
    axes[1].set_ylabel(r"coherence time $\tau_c$ (s)")
    axes[1].set_title(r"$\tau_c \simeq 1/\Delta\nu$", fontsize=8.8)
    clean_axis(axes[1], grid=True)
    panel_label(axes[1], "b")

    save_figure(fig, OUTDIR, "e02_coherence_bandwidth.pdf")


def main() -> None:
    fig_wave_packet_spectrum()
    fig_coherence_bandwidth()


if __name__ == "__main__":
    main()
