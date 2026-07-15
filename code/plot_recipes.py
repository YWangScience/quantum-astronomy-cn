#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Plot recipes for Nature-style textbook figures."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from plot_style import (
    COLORS,
    PALETTE,
    apply_nature_style,
    clean_axis,
    disk_visibility,
    gaussian_visibility,
    j0_numeric,
    panel_label,
    poisson_pmf,
    save_figure,
)

import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Ellipse, FancyArrowPatch, Rectangle


def draw_figure(filename: str, outdir: Path) -> None:
    apply_nature_style()
    recipe = RECIPES.get(filename)
    if recipe is None:
        raise KeyError(f"No plotting recipe registered for {filename}")
    recipe(outdir, filename)


def ch01_fourier_visibility(outdir: Path, filename: str) -> None:
    u = np.linspace(0.0, 9.0, 700)
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.25))
    for sigma in [0.08, 0.16, 0.30]:
        axes[0].plot(u, gaussian_visibility(u, sigma), label=fr"$\sigma={sigma}$")
    axes[0].set(xlabel=r"$u=B/\lambda$", ylabel=r"$|V(u)|$", title="Gaussian source")
    axes[0].legend(frameon=False)
    panel_label(axes[0], "a")

    for sep in [0.45, 0.75, 1.10]:
        axes[1].plot(u, np.abs(np.cos(np.pi * sep * u)), label=fr"$d={sep}$")
    axes[1].set(xlabel=r"$u=B/\lambda$", ylabel=r"$|V(u)|$", title="Equal binary")
    axes[1].legend(frameon=False)
    panel_label(axes[1], "b")

    x = np.linspace(0.0, 18.0, 700)
    axes[2].plot(x, np.abs(disk_visibility(x)), color=COLORS["green"])
    axes[2].set(xlabel=r"$\pi\theta B/\lambda$", ylabel=r"$|V|$", title="Uniform disk")
    panel_label(axes[2], "c")
    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch01_event_table_map(outdir: Path, filename: str) -> None:
    fig, ax = plt.subplots(figsize=(7.1, 3.15))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    table_x, table_y = 0.08, 0.55
    table_w, table_h = 0.36, 0.30
    ax.add_patch(Rectangle((table_x, table_y), table_w, table_h, fc="#F8FBFD", ec=COLORS["black"], lw=0.9))
    headers = [r"$t_j$", r"$\mathbf{r}_j$", r"$\nu_j$", r"$p_j$", r"$w_j$"]
    values = ["time", "recv.", "freq.", "pol.", "weight"]
    for i, (header, value) in enumerate(zip(headers, values)):
        x0 = table_x + table_w * i / 5.0
        ax.plot([x0, x0], [table_y, table_y + table_h], color=COLORS["light_grey"], lw=0.8)
        ax.text(x0 + table_w / 10.0, table_y + 0.21, header, ha="center", va="center", fontsize=9.2)
        ax.text(x0 + table_w / 10.0, table_y + 0.10, value, ha="center", va="center", fontsize=6.8, color=COLORS["grey"])
    ax.plot([table_x + table_w, table_x + table_w], [table_y, table_y + table_h], color=COLORS["light_grey"], lw=0.8)
    ax.text(table_x + table_w / 2, table_y + table_h + 0.06, "one photon event", ha="center", va="center", fontsize=8.5)
    ax.text(table_x + table_w / 2, table_y - 0.06, r"$e_j=(t_j,\mathbf{r}_j,\nu_j,p_j,w_j)$", ha="center", va="center", fontsize=8.5)

    products = [
        ((0.66, 0.82), "image", r"bin by sky position", COLORS["blue"]),
        ((0.82, 0.62), "spectrum", r"bin by $\nu$", COLORS["green"]),
        ((0.66, 0.40), "light curve", r"bin by $t$", COLORS["orange"]),
        ((0.82, 0.20), "correlations", r"keep pairs/groups", COLORS["purple"]),
    ]
    for (x, y), title, subtitle, color in products:
        ax.add_patch(Rectangle((x - 0.105, y - 0.055), 0.21, 0.11, fc="white", ec=color, lw=1.1))
        ax.text(x, y + 0.017, title, ha="center", va="center", fontsize=8.0)
        ax.text(x, y - 0.023, subtitle, ha="center", va="center", fontsize=6.5, color=COLORS["grey"])
        ax.add_patch(FancyArrowPatch((table_x + table_w + 0.02, table_y + table_h / 2), (x - 0.12, y),
                                     arrowstyle="-|>", mutation_scale=10, lw=0.9, color=color))

    ax.text(
        0.50,
        0.50,
        "projection = choose columns,\nbin or average, then lose\nthe discarded coordinates",
        ha="center",
        va="center",
        fontsize=7.1,
        color=COLORS["black"],
        bbox=dict(facecolor="white", edgecolor="none", alpha=0.86, pad=1.6),
    )
    save_figure(fig, outdir, filename)


def ch01_phase_interference(outdir: Path, filename: str) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.65), gridspec_kw={"wspace": 0.35})

    ax = axes[0]
    ax.set_aspect("equal")
    ax.set_xlim(-0.25, 1.75)
    ax.set_ylim(-0.45, 1.35)
    ax.axhline(0, color=COLORS["grey"], lw=0.8)
    ax.axvline(0, color=COLORS["grey"], lw=0.8)
    e1 = np.array([0.92, 0.0])
    angle = np.deg2rad(52)
    e2 = np.array([0.72 * np.cos(angle), 0.72 * np.sin(angle)])
    esum = e1 + e2
    arrows = [
        ((0, 0), e1, COLORS["blue"], r"$\mathcal{E}_1$"),
        ((0, 0), e2, COLORS["orange"], r"$\mathcal{E}_2$"),
        ((0, 0), esum, COLORS["green"], r"$\mathcal{E}_1+\mathcal{E}_2$"),
    ]
    for start, end, color, label in arrows:
        ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=11, lw=1.35, color=color))
        ax.text(end[0] + 0.04, end[1] + 0.035, label, fontsize=8.0, color=color)
    ax.add_patch(Arc((0, 0), 0.42, 0.42, theta1=0, theta2=52, color=COLORS["black"], lw=0.9))
    ax.text(0.28, 0.13, r"$\Delta\phi$", fontsize=8.0)
    ax.set(xlabel="real part", ylabel="imaginary part", title="phasors add as vectors")
    clean_axis(ax, grid=False)
    panel_label(ax, "a")

    ax = axes[1]
    dphi = np.linspace(-np.pi, np.pi, 500)
    intensity = 1.0 + np.cos(dphi)
    ax.plot(dphi, intensity, color=COLORS["blue"])
    ax.axvline(0, color=COLORS["green"], lw=1.0, ls="--")
    ax.axvline(np.pi, color=COLORS["orange"], lw=1.0, ls="--")
    ax.axvline(-np.pi, color=COLORS["orange"], lw=1.0, ls="--")
    ax.text(0.12, 1.78, "constructive", fontsize=7.2, color=COLORS["green"])
    ax.text(-2.95, 0.20, "destructive", fontsize=7.2, color=COLORS["orange"])
    ax.set_xticks([-np.pi, 0, np.pi])
    ax.set_xticklabels([r"$-\pi$", "0", r"$\pi$"])
    ax.set(xlabel=r"phase difference $\Delta\phi$", ylabel=r"interference term scale", ylim=(-0.05, 2.08), title=r"$I\propto |\mathcal{E}_1+\mathcal{E}_2|^2$")
    clean_axis(ax, grid=True)
    panel_label(ax, "b")

    save_figure(fig, outdir, filename)


def ch01_projected_baseline(outdir: Path, filename: str) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(7.3, 3.0), gridspec_kw={"wspace": 0.45})

    ax = axes[0]
    ax.set_aspect("equal")
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, 0.92)
    ax.axis("off")
    t1 = np.array([0.24, 0.20])
    t2 = np.array([0.78, 0.34])
    bvec = t2 - t1
    sdir = np.array([-0.25, -0.97])
    sdir = sdir / np.linalg.norm(sdir)
    wave_normal = -sdir
    for offset in [-0.10, 0.08, 0.26]:
        center = np.array([0.54, 0.76]) + offset * np.array([wave_normal[1], -wave_normal[0]])
        p0 = center - 0.52 * np.array([wave_normal[1], -wave_normal[0]])
        p1 = center + 0.52 * np.array([wave_normal[1], -wave_normal[0]])
        ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=COLORS["light_grey"], lw=1.0)
    ax.add_patch(FancyArrowPatch((0.92, 0.86), (0.70, 0.26), arrowstyle="-|>", mutation_scale=12, lw=1.1, color=COLORS["orange"]))
    ax.text(0.88, 0.75, r"source direction $\mathbf{s}$", ha="right", va="center", fontsize=7.2, color=COLORS["orange"])
    ax.scatter([t1[0], t2[0]], [t1[1], t2[1]], s=35, color=COLORS["blue"], zorder=4)
    ax.text(t1[0], t1[1] - 0.06, r"$T_1$", ha="center", fontsize=8.0)
    ax.text(t2[0], t2[1] - 0.06, r"$T_2$", ha="center", fontsize=8.0)
    ax.add_patch(FancyArrowPatch(t1, t2, arrowstyle="-|>", mutation_scale=11, lw=1.25, color=COLORS["black"]))
    ax.text(0.50, 0.31, r"physical baseline $\mathbf{b}$", fontsize=7.2, rotation=14)
    delay_len = float(np.dot(bvec, sdir))
    foot = t2 - delay_len * sdir
    ax.plot([t2[0], foot[0]], [t2[1], foot[1]], color=COLORS["green"], lw=1.0, ls="--")
    ax.text(0.77, 0.47, r"$\mathbf{b}\cdot\mathbf{s}$", fontsize=7.4, color=COLORS["green"])
    ax.set_title("geometric delay", fontsize=9.5)
    panel_label(ax, "a")

    ax = axes[1]
    ax.set_aspect("equal")
    ax.set_xlim(-0.18, 1.02)
    ax.set_ylim(-0.15, 0.92)
    ax.axhline(0, color=COLORS["grey"], lw=0.8)
    ax.axvline(0, color=COLORS["grey"], lw=0.8)
    ax.add_patch(FancyArrowPatch((0, 0), (0.72, 0.44), arrowstyle="-|>", mutation_scale=12, lw=1.35, color=COLORS["blue"]))
    ax.plot([0.72, 0.72], [0, 0.44], color=COLORS["blue"], lw=0.9, ls="--")
    ax.plot([0, 0.72], [0.44, 0.44], color=COLORS["blue"], lw=0.9, ls="--")
    ax.text(0.36, -0.055, r"$B_x$", ha="center", fontsize=8.0)
    ax.text(0.76, 0.22, r"$B_y$", va="center", fontsize=8.0)
    ax.text(0.37, 0.28, r"$\mathbf{B}_\perp$", fontsize=8.0, color=COLORS["blue"])
    theta = np.linspace(-0.25, 1.1, 100)
    track1 = np.column_stack((0.42 * np.cos(theta) + 0.18, 0.27 * np.sin(theta) + 0.34))
    track2 = np.column_stack((0.30 * np.cos(theta + 0.45) + 0.22, 0.46 * np.sin(theta + 0.45) + 0.18))
    ax.plot(track1[:, 0], track1[:, 1], color=COLORS["orange"], lw=1.0)
    ax.plot(track2[:, 0], track2[:, 1], color=COLORS["green"], lw=1.0)
    ax.text(0.18, 0.78, "Earth rotation\nmoves the point", fontsize=7.0, color=COLORS["grey"])
    ax.set(xlabel=r"east-west projection $B_x$", ylabel=r"north-south projection $B_y$", title=r"projected baseline on sky")
    clean_axis(ax, grid=True)
    panel_label(ax, "b")

    save_figure(fig, outdir, filename)


def ch01_thermal_fluctuation_hbt(outdir: Path, filename: str) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(8.35, 2.85), gridspec_kw={"wspace": 0.56})

    ax = axes[0]
    ax.set_aspect("equal")
    ax.set_xlim(-1.45, 1.45)
    ax.set_ylim(-1.20, 1.23)
    ax.axis("off")
    rng = np.random.default_rng(31)
    cases = [
        ((-0.10, 0.47), rng.normal(loc=0.08, scale=0.23, size=9), "large sum", COLORS["green"]),
        ((-0.10, -0.53), rng.uniform(0.0, 2.0 * np.pi, size=9), "small sum", COLORS["orange"]),
    ]
    for center, angles, label, color in cases:
        center = np.array(center)
        vectors = 0.18 * np.column_stack((np.cos(angles), np.sin(angles)))
        total = vectors.sum(axis=0)
        for vec in vectors:
            ax.add_patch(FancyArrowPatch(center, center + vec, arrowstyle="-|>", mutation_scale=8, lw=0.85, color=COLORS["grey"], alpha=0.88))
        total_scale = 0.34 / max(np.linalg.norm(total), 0.18)
        total_vec = total * total_scale
        ax.add_patch(FancyArrowPatch(center, center + total_vec, arrowstyle="-|>", mutation_scale=11, lw=1.45, color=color))
        ax.text(center[0] + 0.45, center[1] + 0.02, label, ha="left", va="center", fontsize=7.4, color=color)
        ax.text(center[0] - 0.54, center[1] + 0.02, r"$I=|\mathcal{E}|^2$", ha="right", va="center", fontsize=7.4)
    ax.text(0.12, 1.08, "thermal phasor sum", ha="center", va="center", fontsize=9.0)
    panel_label(ax, "a")

    ax = axes[1]
    t = np.linspace(0.0, 1.0, 360)
    rng = np.random.default_rng(7)
    common = (
        0.10 * np.exp(-0.5 * ((t - 0.25) / 0.045) ** 2)
        + 0.07 * np.exp(-0.5 * ((t - 0.55) / 0.070) ** 2)
        + 0.06 * np.exp(-0.5 * ((t - 0.80) / 0.050) ** 2)
    )
    near_1 = 1.00 + common + 0.012 * rng.normal(size=t.size)
    near_2 = 0.92 + 0.92 * common + 0.012 * rng.normal(size=t.size)
    far_1 = 0.72 + 0.035 * rng.normal(size=t.size)
    far_2 = 0.61 + 0.035 * rng.normal(size=t.size)
    ax.plot(t, near_1, color=COLORS["blue"], lw=1.05)
    ax.plot(t, near_2, color=COLORS["orange"], lw=1.05)
    ax.plot(t, far_1, color=COLORS["purple"], lw=0.95, alpha=0.95)
    ax.plot(t, far_2, color=COLORS["green"], lw=0.95, alpha=0.95)
    label_box = dict(facecolor="white", edgecolor="none", alpha=0.78, pad=0.8)
    ax.text(0.03, 1.14, "short baseline: shared peaks", fontsize=7.0, color=COLORS["black"], bbox=label_box)
    ax.text(0.03, 0.54, "long baseline: mostly independent", fontsize=7.0, color=COLORS["black"], bbox=label_box)
    ax.set(xlabel="time", ylabel="intensity", title="intensity fluctuations", ylim=(0.42, 1.23))
    ax.set_yticks([])
    clean_axis(ax, grid=True)
    panel_label(ax, "b")

    ax = axes[2]
    x = np.linspace(0.0, 8.4, 700)
    v2 = disk_visibility(x) ** 2
    ax.plot(x, v2, color=COLORS["purple"], lw=1.25)
    for xpos, text in [(0.85, "small $B\\theta/\\lambda$"), (3.4, "resolved"), (6.7, "weak excess")]:
        ypos = float(np.interp(xpos, x, v2))
        ax.scatter([xpos], [ypos], s=22, color=COLORS["black"], zorder=4)
        ax.text(xpos + 0.15, ypos + 0.055, text, fontsize=6.8, va="center")
    ax.set(
        xlabel=r"$x=\pi B\theta/\lambda$",
        ylabel=r"$g^{(2)}(0)-1\propto |V|^2$",
        ylim=(-0.03, 1.08),
        title="baseline probes angular size",
    )
    clean_axis(ax, grid=True)
    panel_label(ax, "c")

    save_figure(fig, outdir, filename)


def ch01_hbt_schematic(outdir: Path, filename: str) -> None:
    fig, axes = plt.subplots(
        2,
        2,
        figsize=(7.35, 4.65),
        gridspec_kw={"wspace": 0.34, "hspace": 0.44},
    )

    ax = axes[0, 0]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.add_patch(Ellipse((0.13, 0.58), 0.13, 0.22, fc=COLORS["yellow"], ec=COLORS["orange"], lw=1.0))
    ax.text(0.13, 0.78, "thermal\nstar", ha="center", va="center", fontsize=7.4)
    telescope_y = [0.72, 0.34]
    for idx, y in enumerate(telescope_y, start=1):
        ax.add_patch(Rectangle((0.48, y - 0.035), 0.14, 0.07, fc=COLORS["light_grey"], ec=COLORS["black"], lw=0.8))
        ax.add_patch(Rectangle((0.61, y - 0.015), 0.05, 0.03, fc=COLORS["blue"], ec="none", alpha=0.75))
        ax.text(0.55, y + 0.095, fr"$T_{idx}$", ha="center", va="center", fontsize=8.0)
        ax.add_patch(FancyArrowPatch((0.20, 0.58), (0.48, y), arrowstyle="-|>", mutation_scale=9, lw=1.0, color=COLORS["grey"]))
        ax.add_patch(FancyArrowPatch((0.66, y), (0.86, y), arrowstyle="-|>", mutation_scale=9, lw=1.0, color=COLORS["blue"]))
        ax.add_patch(Rectangle((0.86, y - 0.05), 0.09, 0.10, fc="white", ec=COLORS["blue"], lw=0.9))
        ax.text(0.905, y, fr"$N_{idx}(t)$", ha="center", va="center", fontsize=7.5)
    ax.plot([0.55, 0.55], [0.34, 0.72], color=COLORS["black"], lw=0.8)
    ax.text(0.535, 0.53, r"$B$", ha="right", va="center", fontsize=8.0)
    ax.text(0.78, 0.52, "no optical\nbeam combiner", ha="center", va="center", fontsize=7.0, color=COLORS["grey"])
    panel_label(ax, "a")

    rng = np.random.default_rng(12)
    t = np.linspace(0.0, 1.0, 260)
    common = 0.07 * np.exp(-0.5 * ((t - 0.34) / 0.055) ** 2) + 0.05 * np.exp(-0.5 * ((t - 0.72) / 0.065) ** 2)
    n1 = 1.0 + common + 0.018 * rng.normal(size=t.size)
    n2 = 0.78 + 0.90 * common + 0.018 * rng.normal(size=t.size)
    ax = axes[0, 1]
    ax.plot(t, n1, color=COLORS["blue"], label=r"$N_1(t)$")
    ax.plot(t, n2, color=COLORS["orange"], label=r"$N_2(t)$")
    for x0 in [0.34, 0.72]:
        ax.axvspan(x0 - 0.045, x0 + 0.045, color=COLORS["light_grey"], alpha=0.75, lw=0)
    ax.set(xlabel="time", ylabel="counts per bin", ylim=(0.70, 1.13), title="shared intensity fluctuations")
    ax.legend(frameon=False, loc="upper right")
    clean_axis(ax, grid=True)
    panel_label(ax, "b")

    tau = np.linspace(-2.2, 2.2, 500)
    g2 = 1.0 + 0.115 * np.exp(-0.5 * (tau / 0.34) ** 2)
    ax = axes[1, 0]
    ax.plot(tau, g2, color=COLORS["green"], label=r"$\widehat g^{(2)}_{12}(\tau)$")
    ax.axhline(1.0, color=COLORS["grey"], lw=0.9, ls="--", label="random coincidences")
    ax.axvline(0.0, color=COLORS["black"], lw=0.8)
    ax.annotate(
        "excess\ncoincidences",
        xy=(0.0, 1.112),
        xytext=(0.72, 1.09),
        arrowprops=dict(arrowstyle="-|>", lw=0.7, color=COLORS["black"]),
        ha="left",
        va="center",
        fontsize=7.2,
    )
    ax.set(xlabel=r"delay after $\tau_g$", ylabel=r"$H_{12}/(R_1R_2T\Delta\tau)$", ylim=(0.975, 1.135), title="delay histogram")
    ax.legend(frameon=False, loc="upper left")
    clean_axis(ax, grid=True)
    panel_label(ax, "c")

    x = np.linspace(0.0, 8.0, 700)
    v2 = disk_visibility(x) ** 2
    ax = axes[1, 1]
    ax.plot(x, v2, color=COLORS["purple"])
    ax.axhline(1.0, color=COLORS["grey"], lw=0.8, ls="--")
    ax.text(0.35, 0.88, "unresolved", fontsize=7.3, color=COLORS["black"])
    ax.text(4.0, 0.16, "resolved:\ncorrelation falls", fontsize=7.3, color=COLORS["black"])
    ax.set(xlabel=r"$x=\pi B\theta/\lambda$", ylabel=r"$g^{(2)}(0)-1\propto |V|^2$", ylim=(-0.02, 1.06), title="angular information")
    clean_axis(ax, grid=True)
    panel_label(ax, "d")

    save_figure(fig, outdir, filename)


def ch01_photon_count_statistics(outdir: Path, filename: str) -> None:
    n = np.arange(0, 18)
    mu = 5.0
    poisson = poisson_pmf(n, mu)
    fig, ax = plt.subplots(figsize=(3.5, 2.45))
    sigma = np.sqrt(mu)
    ax.bar(n, poisson, width=0.72, color=COLORS["blue"], alpha=0.88)
    ax.axvline(mu, color=COLORS["black"], lw=1.0, label=r"mean $\mu$")
    ax.axvspan(mu - sigma, mu + sigma, color=COLORS["sky"], alpha=0.22, label=r"$\mu\pm\sqrt{\mu}$")
    ax.annotate(
        r"shot noise scale $\sqrt{\mu}$",
        xy=(mu + sigma, poisson_pmf(np.array([int(round(mu + sigma))]), mu)[0]),
        xytext=(9.1, 0.12),
        arrowprops=dict(arrowstyle="-|>", lw=0.8, color=COLORS["black"]),
        fontsize=7.4,
        ha="left",
    )
    ax.set(xlabel="photon count N", ylabel="P(N)", title="Poisson count distribution")
    ax.legend(frameon=False, loc="upper right")
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch01_resolution_baseline(outdir: Path, filename: str) -> None:
    baseline = np.logspace(0, 6, 500)
    wavelengths = {"350 nm": 350e-9, "500 nm": 500e-9, "1.6 um": 1.6e-6}
    rad_to_uas = 180.0 / np.pi * 3600.0 * 1e6
    fig, ax = plt.subplots(figsize=(3.55, 2.45))
    for label, lam in wavelengths.items():
        theta = 1.22 * lam / baseline * rad_to_uas
        ax.loglog(baseline, theta, label=label)
    ax.set(xlabel="baseline B [m]", ylabel="Rayleigh scale [uas]")
    ax.legend(frameon=False)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch01_correlation_dilution_budget(outdir: Path, filename: str) -> None:
    fig, axes = plt.subplots(
        1,
        2,
        figsize=(8.1, 2.5),
        gridspec_kw={"width_ratios": [1.08, 1.0], "wspace": 0.76},
    )

    bandwidth = np.logspace(8, 13, 320)
    time_bin = np.logspace(-12, -7, 280)
    bb, tt = np.meshgrid(bandwidth, time_bin)
    tau_c = 1.0 / bb
    contrast = np.minimum(1.0, tau_c / tt)
    im = axes[0].pcolormesh(
        bandwidth,
        time_bin,
        np.log10(contrast),
        shading="auto",
        cmap="viridis",
        vmin=-5,
        vmax=0,
    )
    axes[0].set_xscale("log")
    axes[0].set_yscale("log")
    axes[0].set(xlabel=r"bandwidth $\Delta\nu$ [Hz]", ylabel=r"time bin $\Delta t$ [s]")
    axes[0].scatter([1.2e12, 2.5e11], [1e-10, 5e-10], s=26, color="white", edgecolor=COLORS["black"], linewidth=0.5)
    axes[0].text(9.0e11, 1.25e-10, "1 nm,\n100 ps", fontsize=6.8, color="white", ha="right", va="center")
    axes[0].text(2.1e11, 7.0e-10, "narrow band,\nslow APD", fontsize=6.8, color="white")
    cbar = fig.colorbar(im, ax=axes[0], pad=0.045, fraction=0.044)
    cbar.set_label(r"$\log_{10}(\tau_c/\Delta t)$", labelpad=3)
    panel_label(axes[0], "a")

    source_fraction = np.linspace(0.05, 1.0, 400)
    axes[1].plot(source_fraction, source_fraction ** 2, color=COLORS["orange"], label=r"$f_1=f_2=f$")
    axes[1].plot(source_fraction, source_fraction * 0.7, color=COLORS["blue"], label=r"$f_2=0.7$")
    axes[1].axhline(0.5, color=COLORS["grey"], lw=0.8, ls="--")
    axes[1].set(xlabel=r"source fraction $S/(S+B)$", ylabel="remaining correlation amplitude", ylim=(0, 1.04))
    axes[1].legend(frameon=False, loc="upper left")
    panel_label(axes[1], "b")

    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch01_polarization_mueller_matrix(outdir: Path, filename: str) -> None:
    matrix = np.array(
        [
            [1.000, 0.015, -0.006, 0.002],
            [0.004, 0.965, 0.018, -0.010],
            [-0.003, -0.021, 0.952, 0.016],
            [0.001, 0.006, -0.012, 0.905],
        ]
    )
    labels = ["I", "Q", "U", "V"]
    fig, axes = plt.subplots(
        1,
        2,
        figsize=(8.35, 2.82),
        gridspec_kw={"width_ratios": [1.10, 1.0], "wspace": 0.96},
    )
    im = axes[0].imshow(matrix, cmap="coolwarm", vmin=-0.06, vmax=1.0)
    axes[0].set_xticks(range(4), labels=[r"$S_{\rm sky," + x + "}$" for x in labels])
    axes[0].set_yticks(range(4), labels=[r"$S_{\rm obs," + x + "}$" for x in labels])
    axes[0].tick_params(axis="x", rotation=32, labelsize=7.0)
    for i in range(4):
        for j in range(4):
            color = "white" if matrix[i, j] > 0.55 else COLORS["black"]
            axes[0].text(j, i, f"{matrix[i,j]:.3f}", ha="center", va="center", fontsize=6.7, color=color)
    cbar = fig.colorbar(im, ax=axes[0], pad=0.050, fraction=0.044)
    cbar.set_label("Mueller element", labelpad=3)
    panel_label(axes[0], "a")

    true_angle = np.linspace(0, 180, 300)
    p = 0.02
    q = p * np.cos(np.deg2rad(2 * true_angle))
    u = p * np.sin(np.deg2rad(2 * true_angle))
    q_obs = matrix[1, 0] + matrix[1, 1] * q + matrix[1, 2] * u
    u_obs = matrix[2, 0] + matrix[2, 1] * q + matrix[2, 2] * u
    axes[1].plot(q, u, color=COLORS["grey"], lw=1.2, label="sky")
    axes[1].plot(q_obs, u_obs, color=COLORS["purple"], label="after leakage")
    axes[1].scatter([q[0], q_obs[0]], [u[0], u_obs[0]], color=[COLORS["grey"], COLORS["purple"]], s=22)
    axes[1].axhline(0, color=COLORS["light_grey"], lw=0.8)
    axes[1].axvline(0, color=COLORS["light_grey"], lw=0.8)
    axes[1].set(xlabel=r"$Q/I$", ylabel=r"$U/I$", aspect="equal")
    axes[1].legend(frameon=False, loc="upper right")
    panel_label(axes[1], "b")
    for ax in axes:
        clean_axis(ax)
    save_figure(fig, outdir, filename)


def ch01_quantum_detection_map(outdir: Path, filename: str) -> None:
    fig, ax = plt.subplots(figsize=(7.25, 3.45))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    boxes = [
        (0.08, 0.63, 0.18, 0.18, "field state", r"$\rho_{AB}$", COLORS["blue"]),
        (0.38, 0.63, 0.18, 0.18, "ignore mode B", r"$\rho_A=\mathrm{Tr}_B\rho_{AB}$", COLORS["green"]),
        (0.68, 0.69, 0.21, 0.16, "single counts", r"$\langle \hat E^{(-)}\hat E^{(+)}\rangle$", COLORS["orange"]),
        (0.68, 0.39, 0.21, 0.16, "coincidences", r"$\langle \hat E_1^{(-)}\hat E_2^{(-)}\hat E_2^{(+)}\hat E_1^{(+)}\rangle$", COLORS["purple"]),
    ]
    for x, y, w, h, title, formula, color in boxes:
        ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=color, lw=1.2))
        ax.text(x + w / 2, y + h * 0.68, title, ha="center", va="center", fontsize=7.8)
        ax.text(x + w / 2, y + h * 0.35, formula, ha="center", va="center", fontsize=7.0, color=color)

    ax.add_patch(FancyArrowPatch((0.26, 0.72), (0.38, 0.72), arrowstyle="-|>", mutation_scale=10, lw=1.0, color=COLORS["black"]))
    ax.add_patch(FancyArrowPatch((0.56, 0.72), (0.68, 0.77), arrowstyle="-|>", mutation_scale=10, lw=1.0, color=COLORS["black"]))
    ax.add_patch(FancyArrowPatch((0.56, 0.72), (0.68, 0.47), arrowstyle="-|>", mutation_scale=10, lw=1.0, color=COLORS["black"]))

    ax.text(
        0.32,
        0.87,
        "unobserved\nfreedom is averaged",
        ha="center",
        va="bottom",
        fontsize=6.8,
        color=COLORS["grey"],
        bbox=dict(facecolor="white", edgecolor="none", alpha=0.85, pad=1.2),
    )
    ax.text(0.62, 0.91, "normal-ordered\nfield products", ha="center", va="center", fontsize=6.8, color=COLORS["grey"])

    ax.add_patch(Rectangle((0.10, 0.23), 0.14, 0.12, fc="#F8FBFD", ec=COLORS["blue"], lw=0.9))
    ax.add_patch(Rectangle((0.12, 0.25), 0.10, 0.08, fc=COLORS["light_grey"], ec="none"))
    ax.text(0.17, 0.18, "mode A", ha="center", fontsize=7.0, color=COLORS["blue"])
    ax.add_patch(Rectangle((0.20, 0.12), 0.14, 0.12, fc="#F8FBFD", ec=COLORS["grey"], lw=0.9, alpha=0.85))
    ax.add_patch(Rectangle((0.22, 0.14), 0.10, 0.08, fc=COLORS["light_grey"], ec="none"))
    ax.text(0.27, 0.07, "mode B\nnot recorded", ha="center", fontsize=7.0, color=COLORS["grey"])
    ax.add_patch(FancyArrowPatch((0.20, 0.35), (0.16, 0.63), arrowstyle="-|>", mutation_scale=9, lw=0.8, color=COLORS["blue"]))
    ax.add_patch(FancyArrowPatch((0.29, 0.24), (0.19, 0.63), arrowstyle="-|>", mutation_scale=9, lw=0.8, color=COLORS["grey"]))

    ax.text(
        0.58,
        0.17,
        "diagonal: photon-number probabilities\n"
        "off-diagonal: phase coherence between basis states",
        ha="center",
        va="center",
        fontsize=7.3,
        bbox=dict(facecolor="white", edgecolor=COLORS["light_grey"], pad=3.0),
    )

    save_figure(fig, outdir, filename)


def ch01_fisher_visibility_design(outdir: Path, filename: str) -> None:
    wavelength = 500e-9
    mas_to_rad = np.pi / (180 * 3600 * 1000)
    baseline = np.linspace(1.0, 500.0, 700)
    theta0 = 0.7 * mas_to_rad
    theta_step = 0.005 * mas_to_rad
    vis0 = disk_visibility(np.pi * theta0 * baseline / wavelength) ** 2
    visp = disk_visibility(np.pi * (theta0 + theta_step) * baseline / wavelength) ** 2
    vism = disk_visibility(np.pi * (theta0 - theta_step) * baseline / wavelength) ** 2
    deriv = (visp - vism) / (2 * theta_step / mas_to_rad)
    sigma_floor = 0.03
    fisher_density = deriv ** 2 / (sigma_floor ** 2 + np.maximum(vis0, 0.02))
    fisher_density /= np.nanmax(fisher_density)

    photons = np.logspace(4, 10, 400)
    stat_error = 1.0 / np.sqrt(photons)
    sys_floor = 3e-4
    total = np.sqrt(stat_error ** 2 + sys_floor ** 2)

    fig, axes = plt.subplots(1, 2, figsize=(7.1, 2.45))
    axes[0].plot(baseline, vis0, color=COLORS["blue"], label=r"$|V|^2$")
    axes[0].plot(baseline, fisher_density, color=COLORS["orange"], label="relative Fisher density")
    axes[0].set(xlabel="baseline B [m]", ylabel="normalized value", ylim=(-0.04, 1.08))
    axes[0].legend(frameon=False)
    panel_label(axes[0], "a")

    axes[1].loglog(photons, stat_error, color=COLORS["grey"], ls="--", label="shot noise")
    axes[1].loglog(photons, total, color=COLORS["green"], label="with systematic floor")
    axes[1].axhline(sys_floor, color=COLORS["black"], lw=0.8, ls=":")
    axes[1].set(xlabel="effective photon pairs", ylabel="fractional error")
    axes[1].legend(frameon=False)
    panel_label(axes[1], "b")

    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch02_mean_intensity_vs_correlation(outdir: Path, filename: str) -> None:
    t = np.linspace(-5.0, 5.0, 700)
    fig, axes = plt.subplots(1, 2, figsize=(6.2, 2.35))
    axes[0].plot(t, np.ones_like(t), color=COLORS["black"], label="same mean")
    axes[0].fill_between(t, 0.96, 1.04, color=COLORS["light_grey"])
    axes[0].set(xlabel="time", ylabel="mean intensity", ylim=(0.88, 1.12))
    panel_label(axes[0], "a")
    axes[1].plot(t, np.ones_like(t), color=COLORS["blue"], label="Poisson")
    axes[1].plot(t, 1.0 + np.exp(-np.abs(t) / 0.9), color=COLORS["orange"], label="thermal")
    axes[1].set(xlabel=r"delay $\tau/\tau_c$", ylabel=r"$g^{(2)}(\tau)$")
    axes[1].legend(frameon=False)
    panel_label(axes[1], "b")
    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch02_event_table_information(outdir: Path, filename: str) -> None:
    rng = np.random.default_rng(2)
    time = rng.normal(0.0, 1.0, 2200)
    freq = 1.4 + 0.15 * rng.normal(size=2200) + 0.04 * time
    pol = rng.choice([0, 1], size=2200, p=[0.62, 0.38])
    fig, axes = plt.subplots(
        1,
        3,
        figsize=(7.8, 2.42),
        gridspec_kw={"width_ratios": [1.0, 1.18, 0.70], "wspace": 0.55},
    )
    axes[0].hist(time, bins=42, color=COLORS["blue"], alpha=0.9)
    axes[0].set(xlabel="arrival time", ylabel="events")
    panel_label(axes[0], "a")
    axes[1].hist2d(time, freq, bins=45, cmap="magma")
    axes[1].set(xlabel="time", ylabel="frequency")
    panel_label(axes[1], "b")
    axes[2].bar(["H", "V"], [np.sum(pol == 0), np.sum(pol == 1)], color=[COLORS["green"], COLORS["purple"]])
    axes[2].set(ylabel="events")
    panel_label(axes[2], "c")
    for ax in axes:
        clean_axis(ax)
    save_figure(fig, outdir, filename)


def ch02_contrast_dilution(outdir: Path, filename: str) -> None:
    ratio = np.logspace(-1, 5, 700)
    fig, axes = plt.subplots(1, 2, figsize=(7.1, 2.45))
    for modes in [1, 10, 100, 1000]:
        contrast = (1.0 / modes) * np.minimum(1.0, 1.0 / ratio)
        axes[0].loglog(ratio, contrast, label=fr"$M={modes}$")
    axes[0].axvline(1.0, color=COLORS["black"], lw=0.85, ls="--")
    axes[0].set(xlabel=r"time bin $\Delta t/\tau_c$", ylabel=r"$g^{(2)}_{\rm obs}(0)-1$")
    axes[0].legend(frameon=False, ncol=2)
    panel_label(axes[0], "a")

    bandwidth = np.logspace(8, 13, 260)
    time_bin = np.logspace(-12, -7, 240)
    bb, tt = np.meshgrid(bandwidth, time_bin)
    tau_c = 1.0 / bb
    contrast = np.minimum(1.0, tau_c / tt)
    im = axes[1].pcolormesh(
        bandwidth,
        time_bin,
        np.log10(contrast),
        shading="auto",
        cmap="viridis",
        vmin=-5,
        vmax=0,
    )
    axes[1].set_xscale("log")
    axes[1].set_yscale("log")
    axes[1].set(xlabel=r"optical bandwidth $\Delta\nu$ [Hz]", ylabel=r"time bin $\Delta t$ [s]")
    cbar = fig.colorbar(im, ax=axes[1], pad=0.02)
    cbar.set_label(r"$\log_{10}(\tau_c/\Delta t)$")
    panel_label(axes[1], "b")

    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch02_revival_timeline(outdir: Path, filename: str) -> None:
    events = [
        (1956, "HBT\nSirius", COLORS["blue"], 0.28, 0.0),
        (1974, "Narrabri\n32 stars", COLORS["blue"], 0.28, 0.0),
        (2006, "IACT arrays\nproposal", COLORS["orange"], 0.28, 0.0),
        (2017, "stellar\nbunching", COLORS["green"], -0.30, -1.4),
        (2020, "VERITAS\n4 telescopes", COLORS["purple"], 0.36, -0.9),
        (2024, "MAGIC / VSII\nscience", COLORS["purple"], -0.36, 1.4),
        (2030, "CTAO\nroutine SII", COLORS["black"], 0.36, 0.5),
    ]
    fig, ax = plt.subplots(figsize=(7.35, 2.18))
    ax.hlines(0, 1950, 2034, color=COLORS["light_grey"], lw=4)
    for year, label, color, y, dx in events:
        ax.scatter(year, 0, s=95, color=color, edgecolor="white", linewidth=0.7, zorder=3)
        ax.vlines(year, 0, y * 0.72, color=color, lw=1.0)
        ax.text(year + dx, y, label, ha="center", va="center", fontsize=6.6, color=color)
    ax.axvspan(1975, 2005, color=COLORS["light_grey"], alpha=0.35, lw=0)
    ax.text(1990, -0.50, "hardware and data-rate bottleneck", ha="center", fontsize=6.9, color=COLORS["grey"])
    ax.set(xlim=(1950, 2035), ylim=(-0.62, 0.54), xlabel="year")
    ax.set_yticks([])
    clean_axis(ax)
    save_figure(fig, outdir, filename)


def ch02_science_case_map(outdir: Path, filename: str) -> None:
    labels = ["bright stellar radii", "Be disks", "fast rotators", "photon bunching", "microlensing", "Type Ia SNe", "natural lasers", "quantum networks"]
    feasibility = np.array([0.92, 0.72, 0.68, 0.82, 0.38, 0.28, 0.43, 0.18])
    novelty = np.array([0.58, 0.72, 0.76, 0.55, 0.82, 0.92, 0.70, 0.95])
    timescale = np.array([2026, 2028, 2028, 2026, 2032, 2035, 2031, 2045])
    fig, ax = plt.subplots(figsize=(4.55, 3.05))
    sizes = 45 + (timescale - 2025) * 8
    ax.scatter(feasibility, novelty, s=sizes, c=timescale, cmap="viridis", edgecolor="white", linewidth=0.6)
    label_pos = {
        "bright stellar radii": (0.84, 0.61, "right", "bright stellar\nradii"),
        "photon bunching": (0.79, 0.51, "right", "photon\nbunching"),
        "quantum networks": (0.18, 0.99, "left", "quantum\nnetworks"),
        "Type Ia SNe": (0.15, 0.94, "left", "Type Ia SNe"),
        "microlensing": (0.40, 0.84, "left", "microlensing"),
        "natural lasers": (0.45, 0.72, "left", "natural lasers"),
        "fast rotators": (0.72, 0.79, "left", "fast rotators"),
        "Be disks": (0.74, 0.75, "left", "Be disks"),
    }
    for label in labels:
        x, y, ha, text = label_pos[label]
        ax.text(x, y, text, fontsize=6.5, ha=ha, va="center")
    ax.axvline(0.6, color=COLORS["grey"], lw=0.8, ls="--")
    ax.axhline(0.7, color=COLORS["grey"], lw=0.8, ls="--")
    ax.set(xlabel="near-term feasibility", ylabel="new information", xlim=(0.08, 1.02), ylim=(0.45, 1.02))
    cbar = fig.colorbar(ax.collections[0], ax=ax, pad=0.05)
    cbar.set_label("plausible decade")
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch03_phase_space_states(outdir: Path, filename: str) -> None:
    fig, ax = plt.subplots(figsize=(3.45, 3.0))
    ellipses = [
        ((0.2, 0.3), 0.85, 0.85, 0, COLORS["blue"], "coherent"),
        ((-1.2, -0.9), 1.4, 1.4, 0, COLORS["orange"], "thermal"),
        ((1.25, -0.9), 1.6, 0.42, 28, COLORS["green"], "squeezed"),
    ]
    for xy, w, h, angle, color, label in ellipses:
        ax.add_patch(Ellipse(xy, w, h, angle=angle, fc=color, ec="none", alpha=0.28))
        ax.scatter([xy[0]], [xy[1]], color=color, s=18)
        ax.text(xy[0], xy[1] + 0.68, label, ha="center", va="center", fontsize=8)
    ax.axhline(0, color=COLORS["grey"], lw=0.8)
    ax.axvline(0, color=COLORS["grey"], lw=0.8)
    ax.set(xlabel="field quadrature X", ylabel="field quadrature P", xlim=(-2.3, 2.3), ylim=(-2.0, 1.8))
    clean_axis(ax)
    save_figure(fig, outdir, filename)


def ch03_state_count_distributions(outdir: Path, filename: str) -> None:
    n = np.arange(0, 18)
    mu = 4.0
    fock = np.zeros_like(n, dtype=float)
    fock[4] = 1.0
    coherent = poisson_pmf(n, mu)
    thermal = mu ** n / (1.0 + mu) ** (n + 1.0)
    fig, ax = plt.subplots(figsize=(3.75, 2.55))
    ax.vlines(n - 0.16, 0, fock, color=COLORS["blue"], lw=1.4, label=r"Fock $|4\rangle$")
    ax.plot(n - 0.16, fock, "o", color=COLORS["blue"], ms=3.0)
    ax.vlines(n, 0, coherent, color=COLORS["green"], lw=1.25, label=r"coherent $\bar n=4$")
    ax.plot(n, coherent, "o", color=COLORS["green"], ms=3.0)
    ax.vlines(n + 0.16, 0, thermal, color=COLORS["orange"], lw=1.25, label=r"thermal $\bar n=4$")
    ax.plot(n + 0.16, thermal, "o", color=COLORS["orange"], ms=3.0)
    ax.set(xlabel="photon number N in one mode", ylabel=r"$P(N)$", xlim=(-0.8, 17.8), ylim=(0, 1.08))
    ax.legend(frameon=False, loc="upper right")
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch03_blackbody_mode_occupation(outdir: Path, filename: str) -> None:
    h = 6.62607015e-34
    k_b = 1.380649e-23
    c = 299792458.0
    wavelength_um = np.logspace(-1, 4, 800)
    wavelength_m = wavelength_um * 1e-6
    frequency = c / wavelength_m
    fig, ax = plt.subplots(figsize=(3.75, 2.55))
    for temp, color in [(3000.0, COLORS["orange"]), (5800.0, COLORS["green"]), (10000.0, COLORS["blue"])]:
        x = h * frequency / (k_b * temp)
        nbar = 1.0 / np.expm1(x)
        ax.loglog(wavelength_um, nbar, color=color, label=fr"$T_b={temp:.0f}$ K")
    ax.axvspan(0.4, 0.7, color=COLORS["light_grey"], alpha=0.7, lw=0)
    ax.text(0.47, 2e-3, "visible", fontsize=7.2, color=COLORS["black"])
    ax.axhline(1.0, color=COLORS["black"], lw=0.8, ls="--")
    ax.set(xlabel=r"wavelength $\lambda$ [$\mu$m]", ylabel=r"single-mode occupation $\bar n_\nu$", xlim=(0.1, 1e4), ylim=(1e-8, 1e5))
    ax.legend(frameon=False, loc="upper left")
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch03_coherence_time_dilution(outdir: Path, filename: str) -> None:
    x = np.logspace(-1, 4, 500)
    fig, ax = plt.subplots(figsize=(3.55, 2.45))
    for m in [1, 3, 10, 100]:
        contrast = np.minimum(1.0 / m, 1.0 / (m * x))
        ax.loglog(x, contrast, label=fr"$M={m}$")
    ax.axvline(1.0, color=COLORS["black"], lw=0.9, ls="--")
    ax.set(xlabel=r"time bin $\Delta t/\tau_c$", ylabel=r"$g^{(2)}(0)-1$")
    ax.legend(frameon=False)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch03_detection_loss_background(outdir: Path, filename: str) -> None:
    eta = np.linspace(0.02, 1.0, 400)
    source_rate = 1.0e6
    dark = 80.0
    sky = 2.0e5
    detected_source = eta * source_rate
    total = detected_source + dark + sky
    source_fraction = detected_source / total

    fig, axes = plt.subplots(1, 2, figsize=(7.1, 2.45))
    axes[0].plot(eta, detected_source, color=COLORS["blue"], label="source")
    axes[0].plot(eta, total, color=COLORS["orange"], label="source + sky + dark")
    axes[0].set(xlabel=r"efficiency $\eta$", ylabel=r"rate [s$^{-1}$]")
    axes[0].ticklabel_format(axis="y", style="sci", scilimits=(-2, 2))
    axes[0].legend(frameon=False)
    panel_label(axes[0], "a")

    axes[1].plot(eta, source_fraction, color=COLORS["green"], label=r"$f=S/(S+B)$")
    axes[1].plot(eta, source_fraction ** 2, color=COLORS["purple"], label=r"$g^{(2)}$ excess factor")
    axes[1].set(xlabel=r"efficiency $\eta$", ylabel="fraction", ylim=(0, 1.03))
    axes[1].legend(frameon=False, loc="lower right")
    panel_label(axes[1], "b")

    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch03_nonclassical_mixing_boundary(outdir: Path, filename: str) -> None:
    f = np.linspace(0.0, 1.0, 500)
    fig, ax = plt.subplots(figsize=(3.75, 2.55))
    cases = [
        (0.0, COLORS["blue"], "single emitter"),
        (0.5, COLORS["green"], "partly antibunched"),
        (1.0, COLORS["grey"], "Poisson"),
        (2.0, COLORS["orange"], "single-mode thermal"),
    ]
    for g2_src, color, label in cases:
        measured = 1.0 + f ** 2 * (g2_src - 1.0)
        ax.plot(f, measured, color=color, label=label)
    for modes in [2, 10, 100]:
        measured = 1.0 + f ** 2 / modes
        ax.plot(f, measured, color=COLORS["purple"], lw=1.0, alpha=0.45, ls="--")
        ax.text(0.82, measured[int(0.82 * (len(f) - 1))] + 0.015, fr"$M={modes}$", fontsize=6.6, color=COLORS["purple"])
    ax.axhline(1.0, color=COLORS["black"], lw=0.85, ls=":")
    ax.set(xlabel=r"source fraction $f$", ylabel=r"measured $g^{(2)}(0)$", ylim=(0.0, 2.05))
    ax.legend(frameon=False, loc="upper left")
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch04_mandel_q_g2(outdir: Path, filename: str) -> None:
    mean_n = np.linspace(0.6, 50.0, 500)
    fig, ax = plt.subplots(figsize=(3.55, 2.45))
    for q in [-0.5, 0.0, 4.0, 15.0]:
        ax.plot(mean_n, 1.0 + q / mean_n, label=fr"$Q={q}$")
    ax.axhline(1.0, color=COLORS["black"], lw=0.8, ls="--")
    ax.set(xlabel=r"$\langle N\rangle$", ylabel=r"$g^{(2)}(0)$", ylim=(0.0, 4.2))
    ax.legend(frameon=False)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch04_siegert_relation(outdir: Path, filename: str) -> None:
    tau = np.linspace(-5, 5, 700)
    g1 = np.exp(-np.abs(tau) / 1.1)
    fig, ax = plt.subplots(figsize=(3.55, 2.45))
    ax.plot(tau, g1, label=r"$|g^{(1)}|$")
    ax.plot(tau, 1 + g1 ** 2, label=r"$g^{(2)}=1+|g^{(1)}|^2$")
    ax.set(xlabel=r"delay $\tau/\tau_c$", ylabel="correlation")
    ax.legend(frameon=False)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch04_factorial_moments(outdir: Path, filename: str) -> None:
    n = np.arange(0, 26)
    p = poisson_pmf(n, 6.0)
    ordinary = n ** 2 * p
    factorial = n * np.maximum(n - 1, 0) * p
    fig, ax = plt.subplots(figsize=(3.55, 2.45))
    ax.plot(n, ordinary / ordinary.sum(), "o-", label=r"$N^2$ weight")
    ax.plot(n, factorial / factorial.sum(), "s-", label=r"$N(N-1)$ weight")
    ax.set(xlabel="count N", ylabel="normalized contribution")
    ax.legend(frameon=False)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch04_response_convolution(outdir: Path, filename: str) -> None:
    tau = np.linspace(-12.0, 12.0, 1400)
    intrinsic_width = 0.32
    intrinsic = np.exp(-0.5 * (tau / intrinsic_width) ** 2)
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.45))

    for response in [0.35, 1.0, 3.0]:
        kernel = np.exp(-0.5 * (tau / response) ** 2)
        kernel = kernel / np.trapezoid(kernel, tau)
        observed = np.convolve(intrinsic, kernel, mode="same") * (tau[1] - tau[0])
        axes[0].plot(tau, observed, label=fr"$\sigma_t/\tau_c={response / intrinsic_width:.1f}$")
    axes[0].plot(tau, intrinsic, color=COLORS["black"], lw=1.0, ls="--", label="intrinsic")
    axes[0].set(xlabel=r"delay $\tau/\tau_c$", ylabel=r"$g^{(2)}-1$")
    axes[0].legend(frameon=False)
    panel_label(axes[0], "a")

    ratio = np.logspace(-1, 2.2, 500)
    dilution = 1.0 / np.sqrt(1.0 + ratio ** 2)
    axes[1].loglog(ratio, dilution, color=COLORS["purple"])
    axes[1].axvline(1.0, color=COLORS["black"], lw=0.85, ls="--")
    axes[1].set(xlabel=r"response width $\Delta t_{\rm eff}/\tau_c$", ylabel="peak contrast fraction")
    panel_label(axes[1], "b")

    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch04_delay_histogram_estimator(outdir: Path, filename: str) -> None:
    rng = np.random.default_rng(14)
    tau = np.linspace(-9.0, 9.0, 181)
    baseline = 1.0e5 * np.ones_like(tau)
    peak = 230.0 * np.exp(-0.5 * (tau / 0.75) ** 2)
    raw = rng.poisson(baseline + peak)
    reference = rng.poisson(baseline)
    excess = (raw - reference) / baseline

    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.45))
    axes[0].step(tau, raw / 1.0e5, where="mid", label="same-source")
    axes[0].step(tau, reference / 1.0e5, where="mid", label="shifted reference", color=COLORS["grey"])
    axes[0].set(xlabel=r"delay $\tau$ [ns]", ylabel=r"coincidences / $10^5$")
    axes[0].legend(frameon=False)
    panel_label(axes[0], "a")

    axes[1].plot(tau, excess * 1.0e3, "o", ms=2.8, color=COLORS["blue"])
    axes[1].plot(tau, peak / baseline * 1.0e3, color=COLORS["orange"], label="bunching model")
    axes[1].axhline(0.0, color=COLORS["black"], lw=0.85)
    axes[1].set(xlabel=r"delay $\tau$ [ns]", ylabel=r"$g^{(2)}-1$ [$10^{-3}$]")
    axes[1].legend(frameon=False)
    panel_label(axes[1], "b")

    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch04_deadtime_pileup_bias(outdir: Path, filename: str) -> None:
    tau = np.linspace(-80, 80, 900)
    thermal = 1.0 + 0.0022 * np.exp(-0.5 * (tau / 9.0) ** 2)
    deadtime_hole = 1.0 - 0.75 * np.exp(-0.5 * (tau / 18.0) ** 2)
    afterpulse = 1.0 + 0.10 * np.exp(-0.5 * ((np.abs(tau) - 42.0) / 7.0) ** 2)
    measured_single = thermal * deadtime_hole * afterpulse
    cross = thermal

    fig, axes = plt.subplots(1, 2, figsize=(7.1, 2.45))
    axes[0].plot(tau, measured_single, color=COLORS["orange"], label="one detector auto-correlation")
    axes[0].plot(tau, cross, color=COLORS["blue"], label="split-beam cross-correlation")
    axes[0].axhline(1.0, color=COLORS["black"], lw=0.8, ls=":")
    axes[0].set(xlabel=r"delay $\tau$ [ns]", ylabel=r"apparent $g^{(2)}$")
    axes[0].legend(frameon=False)
    panel_label(axes[0], "a")

    rates = np.logspace(4, 8, 500)
    tau_d = 25e-9
    nonpar = rates / (1 + rates * tau_d)
    par = rates * np.exp(-rates * tau_d)
    axes[1].loglog(rates, rates, color=COLORS["grey"], ls="--", label="ideal")
    axes[1].loglog(rates, nonpar, color=COLORS["green"], label="non-paralyzable")
    axes[1].loglog(rates, par, color=COLORS["purple"], label="paralyzable")
    axes[1].set(xlabel=r"incident rate [s$^{-1}$]", ylabel=r"recorded rate [s$^{-1}$]")
    axes[1].legend(frameon=False)
    panel_label(axes[1], "b")

    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch04_g3_closure_phase(outdir: Path, filename: str) -> None:
    closure = np.linspace(-np.pi, np.pi, 500)
    amp = 0.45
    g3 = 1 + 3 * amp ** 2 + 2 * amp ** 3 * np.cos(closure)

    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.55))
    pts = np.array([[0.0, 1.0], [-0.9, -0.55], [0.9, -0.55]])
    axes[0].scatter(pts[:, 0], pts[:, 1], s=72, color=[COLORS["blue"], COLORS["orange"], COLORS["green"]], zorder=3)
    for i, j, label in [(0, 1, r"$\gamma_{12}$"), (1, 2, r"$\gamma_{23}$"), (2, 0, r"$\gamma_{31}$")]:
        axes[0].add_patch(FancyArrowPatch(pts[i], pts[j], arrowstyle="-|>", mutation_scale=12, lw=1.2, color=COLORS["black"]))
        mid = 0.5 * (pts[i] + pts[j])
        axes[0].text(mid[0], mid[1], label, fontsize=8.0, ha="center", va="center", bbox=dict(fc="white", ec="none", alpha=0.85, pad=0.5))
    axes[0].set(xlim=(-1.25, 1.25), ylim=(-0.85, 1.25), aspect="equal")
    axes[0].set_xticks([])
    axes[0].set_yticks([])
    axes[0].set_title("three-telescope product")
    panel_label(axes[0], "a")

    axes[1].plot(closure, g3, color=COLORS["purple"])
    axes[1].axhline(1 + 3 * amp ** 2, color=COLORS["grey"], lw=0.85, ls="--", label="pair terms")
    axes[1].set(xlabel=r"closure phase $\phi_{12}+\phi_{23}+\phi_{31}$", ylabel=r"$g^{(3)}_{123}$")
    axes[1].set_xticks([-np.pi, 0, np.pi], labels=[r"$-\pi$", "0", r"$\pi$"])
    axes[1].legend(frameon=False)
    panel_label(axes[1], "b")
    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch04_frequency_polarization_matrix(outdir: Path, filename: str) -> None:
    channels = ["H blue", "V blue", "H line", "V line", "H red", "V red"]
    n = len(channels)
    mat = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            same_band = 1.0 if i // 2 == j // 2 else 0.25 * np.exp(-abs(i // 2 - j // 2))
            same_pol = 1.0 if i % 2 == j % 2 else 0.45
            line_boost = 1.8 if (i // 2 == 1 and j // 2 == 1) else 1.0
            mat[i, j] = 1e-3 * same_band * same_pol * line_boost
    fig, ax = plt.subplots(figsize=(3.75, 3.0))
    im = ax.imshow(mat * 1e3, cmap="magma", vmin=0, vmax=1.8)
    ax.set_xticks(range(n), labels=channels, rotation=35, ha="right")
    ax.set_yticks(range(n), labels=channels)
    for i in range(n):
        for j in range(n):
            ax.text(j, i, f"{mat[i,j]*1e3:.1f}", ha="center", va="center", color="white" if mat[i,j]*1e3 > 0.7 else COLORS["black"], fontsize=6.4)
    cbar = fig.colorbar(im, ax=ax, pad=0.02)
    cbar.set_label(r"$g^{(2)}-1$ [$10^{-3}$]")
    clean_axis(ax)
    save_figure(fig, outdir, filename)


def ch05_vcz_visibility_models(outdir: Path, filename: str) -> None:
    u = np.linspace(0.0, 12.0, 700)
    fig, ax = plt.subplots(figsize=(3.55, 2.45))
    ax.plot(u, disk_visibility(np.pi * 0.34 * u) ** 2, label="uniform disk")
    ax.plot(u, gaussian_visibility(u, 0.12) ** 2, label="Gaussian")
    ax.plot(u, np.cos(np.pi * 0.65 * u) ** 2, label="equal binary")
    ax.plot(u, j0_numeric(2 * np.pi * 0.17 * u) ** 2, label="thin ring")
    ax.set(xlabel=r"spatial frequency $u=B/\lambda$", ylabel=r"$|V|^2$")
    ax.legend(frameon=False)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch05_sii_signal_vs_baseline(outdir: Path, filename: str) -> None:
    baseline = np.linspace(0.0, 500.0, 650)
    wavelength = 416e-9
    c_inst = 1.25e-6
    mas_to_rad = np.pi / (180 * 3600 * 1000)
    fig, ax = plt.subplots(figsize=(3.55, 2.45))
    for theta_mas in [0.3, 0.5, 0.8]:
        theta = theta_mas * mas_to_rad
        x = np.pi * theta * baseline / wavelength
        ax.plot(baseline, c_inst * disk_visibility(x) ** 2, label=fr"{theta_mas} mas")
    ax.set(xlabel="projected baseline B [m]", ylabel=r"$g^{(2)}_{12}(0)-1$")
    ax.ticklabel_format(axis="y", style="sci", scilimits=(-2, 2))
    ax.legend(frameon=False)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch05_uniform_disk_resolution(outdir: Path, filename: str) -> None:
    wavelength = 416e-9
    mas_to_rad = np.pi / (180 * 3600 * 1000)
    theta = np.linspace(0.08, 2.0, 500)
    first_null = 1.22 * wavelength / (theta * mas_to_rad)
    fig, ax = plt.subplots(figsize=(3.55, 2.45))
    ax.loglog(theta, first_null, color=COLORS["blue"])
    for baseline, label in [(80, "80 m"), (170, "170 m"), (500, "500 m"), (2000, "2 km")]:
        ax.axhline(baseline, lw=0.85, ls="--", label=label)
    ax.set(xlabel=r"uniform-disk diameter $\theta$ [mas]", ylabel="first-null baseline [m]")
    ax.legend(frameon=False, ncol=2)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch05_snr_scaling(outdir: Path, filename: str) -> None:
    mag = np.linspace(0.0, 9.0, 500)
    rel_flux = 10.0 ** (-0.4 * (mag - 5.0))
    fig, ax = plt.subplots(figsize=(3.55, 2.45))
    for hours, bandwidth, color in [(1, 100e6, COLORS["blue"]), (5, 100e6, COLORS["orange"]), (5, 1e9, COLORS["green"])]:
        rel_snr = rel_flux * np.sqrt(hours / 5.0) * np.sqrt(bandwidth / 100e6)
        ax.semilogy(mag, rel_snr, color=color, label=fr"{hours} h, $\Delta f={bandwidth/1e6:.0f}$ MHz")
    ax.axhline(1.0, color=COLORS["black"], lw=0.85, ls="--")
    ax.set(xlabel="visual magnitude", ylabel="relative SNR")
    ax.legend(frameon=False)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch05_uv_coverage(outdir: Path, filename: str) -> None:
    hour_angle = np.linspace(-4, 4, 13) * np.pi / 12
    baselines = [(60, 0.1), (110, 0.8), (180, 1.5)]
    fig, ax = plt.subplots(figsize=(3.2, 3.0))
    for length, angle in baselines:
        u = length * np.cos(hour_angle + angle)
        v = 0.55 * length * np.sin(hour_angle + angle)
        ax.plot(u, v, "o-", ms=3)
        ax.plot(-u, -v, "o-", ms=3, alpha=0.55)
    ax.set(xlabel="u [m]", ylabel="v [m]", aspect="equal")
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch05_zero_baseline_calibration(outdir: Path, filename: str) -> None:
    rng = np.random.default_rng(5)
    night = np.arange(1, 16)
    true_n0 = 1.25e-6 * (1 + 0.05 * np.sin(night / 2.1))
    measured = true_n0 + rng.normal(0, 0.035e-6, size=night.size)
    baseline = np.linspace(0, 380, 420)
    wavelength = 416e-9
    mas_to_rad = np.pi / (180 * 3600 * 1000)
    theta = 0.62 * mas_to_rad
    model = disk_visibility(np.pi * theta * baseline / wavelength) ** 2

    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.45))
    axes[0].plot(night, true_n0 * 1e6, color=COLORS["grey"], lw=1.0, label="smooth drift")
    axes[0].errorbar(night, measured * 1e6, yerr=0.035, fmt="o", color=COLORS["blue"], ms=3.4, label="calibrator")
    axes[0].set(xlabel="night", ylabel=r"$N_0$ [$10^{-6}$]")
    axes[0].legend(frameon=False)
    panel_label(axes[0], "a")

    axes[1].plot(baseline, model, color=COLORS["black"], label="true")
    axes[1].plot(baseline, 1.08 * model, color=COLORS["orange"], ls="--", label=r"$N_0$ high by 8%")
    axes[1].plot(baseline, 0.92 * model, color=COLORS["purple"], ls="--", label=r"$N_0$ low by 8%")
    axes[1].set(xlabel="baseline B [m]", ylabel=r"calibrated $|V|^2$")
    axes[1].legend(frameon=False)
    panel_label(axes[1], "b")
    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch05_phase_ambiguity(outdir: Path, filename: str) -> None:
    x = np.linspace(-4.0, 4.0, 900)
    source_a = np.exp(-0.5 * ((x + 0.85) / 0.22) ** 2) + 0.55 * np.exp(-0.5 * ((x - 0.65) / 0.28) ** 2)
    source_b = source_a[::-1]
    source_a /= np.trapezoid(source_a, x)
    source_b /= np.trapezoid(source_b, x)
    freq = np.fft.fftshift(np.fft.fftfreq(x.size, d=x[1] - x[0]))
    va = np.abs(np.fft.fftshift(np.fft.fft(source_a))) ** 2
    vb = np.abs(np.fft.fftshift(np.fft.fft(source_b))) ** 2
    va /= va.max()
    vb /= vb.max()

    fig, axes = plt.subplots(1, 2, figsize=(7.1, 2.45))
    axes[0].plot(x, source_a, color=COLORS["blue"], label="source")
    axes[0].plot(x, source_b, color=COLORS["orange"], ls="--", label="mirror")
    axes[0].set(xlabel="angle", ylabel="brightness")
    axes[0].legend(frameon=False)
    panel_label(axes[0], "a")

    sel = np.abs(freq) < 4.5
    axes[1].plot(freq[sel], va[sel], color=COLORS["blue"], label=r"$|V|^2$ source")
    axes[1].plot(freq[sel], vb[sel], color=COLORS["orange"], ls="--", label=r"$|V|^2$ mirror")
    axes[1].set(xlabel="spatial frequency", ylabel=r"normalized $|V|^2$")
    axes[1].legend(frameon=False)
    panel_label(axes[1], "b")
    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch05_error_budget(outdir: Path, filename: str) -> None:
    labels = ["Narrabri-like", "VERITAS", "MAGIC", "CTA pathfinder"]
    stat = np.array([0.10, 0.035, 0.045, 0.020])
    n0 = np.array([0.035, 0.025, 0.030, 0.015])
    bg = np.array([0.020, 0.018, 0.026, 0.018])
    model = np.array([0.025, 0.020, 0.024, 0.018])
    weather = np.array([0.018, 0.015, 0.019, 0.012])
    x = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(4.4, 2.85))
    bottom = np.zeros(len(labels))
    for vals, color, lab in [
        (stat, COLORS["blue"], "statistics"),
        (n0, COLORS["orange"], "zero baseline"),
        (bg, COLORS["green"], "background"),
        (model, COLORS["purple"], "model"),
        (weather, COLORS["grey"], "selection"),
    ]:
        ax.bar(x, vals, bottom=bottom, color=color, label=lab)
        bottom += vals
    ax.set_xticks(x, labels=labels, rotation=18, ha="right")
    ax.set(ylabel="diameter error contribution", ylim=(0, 0.22))
    ax.legend(frameon=False, ncol=2, loc="upper right")
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch06_detector_timing_response(outdir: Path, filename: str) -> None:
    tau = np.linspace(-8, 8, 900)
    intrinsic = 0.35
    fig, ax = plt.subplots(figsize=(3.55, 2.45))
    for sigma_t in [0.0, 0.5, 1.5, 4.0]:
        sigma = np.sqrt(intrinsic ** 2 + sigma_t ** 2)
        ax.plot(tau, intrinsic / sigma * np.exp(-0.5 * (tau / sigma) ** 2), label=fr"$\sigma_t={sigma_t}$ ns")
    ax.set(xlabel=r"delay $\tau$ [ns]", ylabel=r"measured excess")
    ax.legend(frameon=False)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch06_deadtime_saturation(outdir: Path, filename: str) -> None:
    rin = np.logspace(2, 8, 500)
    tau = 20e-9
    nonpar = rin / (1 + rin * tau)
    par = rin * np.exp(-rin * tau)
    fig, ax = plt.subplots(figsize=(3.55, 2.45))
    ax.loglog(rin, rin, color=COLORS["grey"], ls="--", label="ideal")
    ax.loglog(rin, nonpar, label="non-paralyzable")
    ax.loglog(rin, par, label="paralyzable")
    ax.set(xlabel="incident rate [s$^{-1}$]", ylabel="recorded rate [s$^{-1}$]")
    ax.legend(frameon=False)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch06_event_table_schema(outdir: Path, filename: str) -> None:
    fig, ax = plt.subplots(figsize=(7.0, 2.55))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis("off")
    stages = [
        (0.25, "raw event", ["time counter", "channel id", "ADC/TDC word", "overflow flag"]),
        (3.45, "calibrated event", ["UTC/TAI/TDB time", "telescope + detector", "wavelength bin", "polarization + weight"]),
        (6.85, "correlation product", ["baseline", "delay bin", r"$g^{(2)}(\tau)-1$", "noise + quality mask"]),
    ]
    colors = [COLORS["blue"], COLORS["green"], COLORS["orange"]]
    for i, (x0, title, rows) in enumerate(stages):
        ax.add_patch(Rectangle((x0, 0.42), 2.55, 3.05, facecolor="white", edgecolor=colors[i], lw=1.4))
        ax.add_patch(Rectangle((x0, 2.95), 2.55, 0.52, facecolor=colors[i], edgecolor=colors[i], lw=1.4))
        ax.text(x0 + 1.275, 3.21, title, ha="center", va="center", color="white", fontweight="bold")
        for j, row in enumerate(rows):
            ax.text(x0 + 0.18, 2.55 - 0.53 * j, row, ha="left", va="center")
            ax.plot([x0 + 0.15, x0 + 2.40], [2.28 - 0.53 * j, 2.28 - 0.53 * j], color=COLORS["light_grey"], lw=0.65)
    for x in [2.85, 6.1]:
        ax.add_patch(FancyArrowPatch((x, 1.95), (x + 0.45, 1.95), arrowstyle="-|>", mutation_scale=12, lw=1.2, color=COLORS["black"]))
    ax.text(3.08, 2.3, "calibration", ha="center", va="bottom", fontsize=7.5)
    ax.text(6.36, 2.3, "estimation", ha="center", va="bottom", fontsize=7.5)
    save_figure(fig, outdir, filename)


def ch06_detector_trade_space(outdir: Path, filename: str) -> None:
    names = ["PMT", "SPAD", "SNSPD", "MKID"]
    jitter_ps = np.array([900.0, 45.0, 4.0, 2.0e6])
    dark = np.array([500.0, 50.0, 1.0, 0.02])
    qe = np.array([0.30, 0.58, 0.90, 0.55])
    fig, ax = plt.subplots(figsize=(3.7, 2.75))
    sizes = 80 + 420 * qe
    ax.scatter(jitter_ps, dark, s=sizes, c=[COLORS["blue"], COLORS["green"], COLORS["purple"], COLORS["orange"]],
               alpha=0.82, edgecolor="white", linewidth=0.8)
    for x, y, n in zip(jitter_ps, dark, names):
        dx = 1.12 if n != "MKID" else 0.75
        ax.text(x * dx, y * (1.25 if n != "SNSPD" else 1.8), n, fontsize=8)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set(xlabel="single-event timing jitter [ps]", ylabel="dark/background count [s$^{-1}$ pix$^{-1}$]")
    ax.text(0.04, 0.06, "marker area: representative quantum efficiency", transform=ax.transAxes, fontsize=7.0)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch06_time_budget(outdir: Path, filename: str) -> None:
    labels = [
        "SNSPD jitter",
        "SPAD jitter",
        "WR link residual",
        "PMT/electronics width",
        "100 m geometric delay",
        "1 km geometric delay",
        "Earth-orbit barycentric term",
    ]
    seconds = np.array([4e-12, 45e-12, 40e-12, 4e-9, 3.33e-7, 3.33e-6, 500.0])
    colors = [COLORS["purple"], COLORS["green"], COLORS["sky"], COLORS["blue"], COLORS["orange"], COLORS["orange"], COLORS["black"]]
    fig, ax = plt.subplots(figsize=(5.1, 2.95))
    y = np.arange(len(labels))
    ax.barh(y, seconds, color=colors, alpha=0.88)
    ax.set_xscale("log")
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set(xlabel="characteristic time scale [s]")
    for yi, val in zip(y, seconds):
        if val < 1e-9:
            txt = f"{val*1e12:.0f} ps"
        elif val < 1e-6:
            txt = f"{val*1e9:.1f} ns"
        elif val < 1e-3:
            txt = f"{val*1e6:.1f} us"
        else:
            txt = f"{val:.0f} s"
        ax.text(val * 1.4, yi, txt, va="center", fontsize=7.2)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch06_spectral_resolution_coherence(outdir: Path, filename: str) -> None:
    resolving_power = np.logspace(1, 5, 400)
    lam = 500e-9
    tau_c = resolving_power * lam / 299792458.0
    rel_rate = resolving_power[0] / resolving_power
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 2.55))
    axes[0].loglog(resolving_power, tau_c * 1e12, color=COLORS["blue"])
    axes[0].set(xlabel=r"resolving power $R=\lambda/\Delta\lambda$", ylabel=r"coherence time $\tau_c$ [ps]")
    axes[0].axhline(4.0, color=COLORS["grey"], ls="--", lw=0.9)
    axes[0].text(14, 4.8, "few-ps timing jitter", fontsize=7.1, color=COLORS["grey"])
    panel_label(axes[0], "a")
    axes[1].loglog(resolving_power, rel_rate, color=COLORS["orange"], label="photons per channel")
    axes[1].loglog(resolving_power, tau_c / tau_c[0], color=COLORS["green"], label="coherence time")
    axes[1].set(xlabel=r"resolving power $R$", ylabel="relative scaling")
    axes[1].legend(frameon=False)
    panel_label(axes[1], "b")
    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch07_poisson_likelihood(outdir: Path, filename: str) -> None:
    rng = np.random.default_rng(7)
    t = np.linspace(0, 30, 1200)
    rate = 1.4 + 12 * np.exp(-0.5 * ((t - 10) / 2.8) ** 2) + 5 * np.exp(-0.5 * ((t - 21) / 4.0) ** 2)
    dt = t[1] - t[0]
    events = np.repeat(t, rng.poisson(rate * dt))
    fig, axes = plt.subplots(2, 1, figsize=(4.2, 3.15), sharex=True, gridspec_kw={"height_ratios": [2.0, 1.0]})
    axes[0].plot(t, rate)
    axes[0].fill_between(t, 0, rate, color=COLORS["blue"], alpha=0.16)
    axes[0].set(ylabel=r"rate $\lambda(t)$ [s$^{-1}$]")
    axes[1].eventplot(events, lineoffsets=0, linelengths=0.8, colors=COLORS["black"])
    axes[1].set(xlabel="time [s]", yticks=[], ylabel="events")
    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch07_time_shift_background(outdir: Path, filename: str) -> None:
    tau = np.linspace(-60, 60, 241)
    baseline = 1.0e6 * (1 + 0.04 * np.sin(2 * np.pi * tau / 120))
    signal = 5.5e3 * np.exp(-0.5 * (tau / 4.0) ** 2)
    shifted = baseline * (1 + 0.015 * np.cos(2 * np.pi * tau / 45))
    fig, ax = plt.subplots(figsize=(4.05, 2.65))
    ax.plot(tau, baseline + signal, color=COLORS["blue"], label="zero-delay histogram")
    ax.plot(tau, shifted, color=COLORS["orange"], label="time-shift background")
    ax.fill_between(tau, shifted, baseline + signal, where=(np.abs(tau) < 14), color=COLORS["green"], alpha=0.18)
    ax.set(xlabel=r"delay $\tau$ [ns]", ylabel="event pairs per bin")
    ax.legend(frameon=False)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch07_correlator_scaling(outdir: Path, filename: str) -> None:
    n = np.logspace(3, 9, 400)
    window_pairs = 80 * n
    fft_bins = 15 * n * np.log2(n)
    naive = n ** 2
    fig, ax = plt.subplots(figsize=(3.9, 2.65))
    ax.loglog(n, naive, color=COLORS["grey"], ls="--", label=r"all pairs $N^2$")
    ax.loglog(n, window_pairs, color=COLORS["blue"], label=r"sorted window $Nk$")
    ax.loglog(n, fft_bins, color=COLORS["green"], label=r"binned FFT $M\log M$")
    ax.set(xlabel="events or time bins", ylabel="relative operations")
    ax.legend(frameon=False)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch07_covariance_matrix(outdir: Path, filename: str) -> None:
    rng = np.random.default_rng(71)
    n_tel = 9
    cov = 0.035 * rng.normal(size=(n_tel, n_tel))
    cov = (cov + cov.T) / 2
    for i in range(n_tel):
        cov[i, i] = 1.0
    for i in range(0, n_tel - 1, 3):
        cov[i:i + 3, i:i + 3] += 0.10
    cov[1, 6] = cov[6, 1] = 0.28
    cov[3, 7] = cov[7, 3] = -0.16
    fig, ax = plt.subplots(figsize=(3.2, 2.9))
    im = ax.imshow(cov, cmap="viridis", vmin=-0.1, vmax=1.0)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03, label="correlation")
    ax.set(xlabel="baseline/channel index", ylabel="baseline/channel index")
    clean_axis(ax)
    save_figure(fig, outdir, filename)


def ch07_fisher_scaling(outdir: Path, filename: str) -> None:
    n = np.logspace(2, 8, 500)
    fig, ax = plt.subplots(figsize=(3.55, 2.45))
    ax.loglog(n, 1 / np.sqrt(n), label="statistics only")
    ax.loglog(n, np.sqrt(1 / n + 2e-4 ** 2), label=r"floor $2\times10^{-4}$")
    ax.loglog(n, np.sqrt(1 / n + 1e-3 ** 2), label=r"floor $10^{-3}$")
    ax.set(xlabel="effective photon number", ylabel="parameter uncertainty")
    ax.legend(frameon=False)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch08_rayleigh_information(outdir: Path, filename: str) -> None:
    d = np.linspace(0.002, 3.0, 360)
    x = np.linspace(-8.0, 8.0, 4001)
    dx = x[1] - x[0]
    direct = []
    for sep in d:
        g1 = np.exp(-0.5 * (x - sep / 2) ** 2) / np.sqrt(2 * np.pi)
        g2 = np.exp(-0.5 * (x + sep / 2) ** 2) / np.sqrt(2 * np.pi)
        p = 0.5 * (g1 + g2)
        dp = ((x - sep / 2) * g1 - (x + sep / 2) * g2) / 4.0
        direct.append(np.sum(dp ** 2 / np.maximum(p, 1e-300)) * dx)
    direct = np.array(direct) / 0.25
    qfi = np.ones_like(d)
    fig, ax = plt.subplots(figsize=(3.9, 2.7))
    ax.plot(d, direct, color=COLORS["blue"], label="direct image pixels")
    ax.plot(d, qfi, color=COLORS["orange"], label="quantum limit / ideal SPADE")
    ax.axvline(1.22, color=COLORS["black"], lw=0.8, ls="--", label=r"$1.22\,\lambda/D$ scale")
    ax.set(xlabel=r"source separation $s/\sigma$", ylabel=r"$F_{ss}/F_Q$ per photon", ylim=(-0.02, 1.08))
    ax.legend(frameon=False)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch08_spade_probabilities(outdir: Path, filename: str) -> None:
    import math

    d = np.linspace(0, 4.0, 600)
    q = d ** 2 / 16.0
    fig, ax = plt.subplots(figsize=(3.85, 2.65))
    for n, color in zip(range(5), PALETTE):
        ax.plot(d, np.exp(-q) * q ** n / math.factorial(n), color=color, label=fr"$n={n}$")
    ax.set(xlabel=r"separation $s/\sigma$", ylabel=r"Hermite-Gaussian probability $p_n$")
    ax.legend(frameon=False)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch08_cramer_rao_bound(outdir: Path, filename: str) -> None:
    n_ph = np.logspace(2, 10, 500)
    sep = 0.25
    x = np.linspace(-8.0, 8.0, 4001)
    dx = x[1] - x[0]
    g1 = np.exp(-0.5 * (x - sep / 2) ** 2) / np.sqrt(2 * np.pi)
    g2 = np.exp(-0.5 * (x + sep / 2) ** 2) / np.sqrt(2 * np.pi)
    p = 0.5 * (g1 + g2)
    dp = ((x - sep / 2) * g1 - (x + sep / 2) * g2) / 4.0
    f_direct = np.sum(dp ** 2 / np.maximum(p, 1e-300)) * dx
    f_q = 0.25
    floor = 0.004
    fig, ax = plt.subplots(figsize=(3.9, 2.65))
    ax.loglog(n_ph, np.sqrt(1.0 / (n_ph * f_direct)), color=COLORS["blue"], label=r"direct, $s=0.25\sigma$")
    ax.loglog(n_ph, np.sqrt(1.0 / (n_ph * f_q)), color=COLORS["orange"], label="ideal mode measurement")
    ax.loglog(n_ph, np.sqrt(1.0 / (n_ph * f_q) + floor ** 2), color=COLORS["green"], label=r"mode + $0.004\sigma$ floor")
    ax.set(xlabel=r"detected source photons $N_\gamma$", ylabel=r"separation error $\Delta s/\sigma$")
    ax.legend(frameon=False)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch08_direct_image_vs_modes(outdir: Path, filename: str) -> None:
    x = np.linspace(-4.0, 4.0, 700)
    seps = [0.0, 0.35, 1.2]
    colors = [COLORS["black"], COLORS["blue"], COLORS["orange"]]
    fig, axes = plt.subplots(1, 2, figsize=(6.25, 2.55), gridspec_kw={"width_ratios": [1.25, 1.0]})
    for sep, color in zip(seps, colors):
        profile = 0.5 * (
            np.exp(-0.5 * (x - sep / 2) ** 2)
            + np.exp(-0.5 * (x + sep / 2) ** 2)
        ) / np.sqrt(2 * np.pi)
        axes[0].plot(x, profile, color=color, label=fr"$s={sep:g}\sigma$")
    axes[0].set(xlabel=r"focal-plane coordinate $x/\sigma$", ylabel="normalized intensity")
    axes[0].legend(frameon=False)
    panel_label(axes[0], "a")

    modes = np.arange(4)
    width = 0.26
    import math
    for offset, sep, color in [(-width / 2, 0.35, COLORS["blue"]), (width / 2, 1.2, COLORS["orange"])]:
        q = sep ** 2 / 16.0
        p = np.array([np.exp(-q) * q ** n / math.factorial(int(n)) for n in modes])
        axes[1].bar(modes + offset, p, width=width, color=color, label=fr"$s={sep:g}\sigma$")
    axes[1].set(xlabel="HG mode index", ylabel="probability", yscale="log", ylim=(1e-6, 1.2))
    axes[1].legend(frameon=False)
    panel_label(axes[1], "b")
    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch08_visibility_fisher_design(outdir: Path, filename: str) -> None:
    baseline = np.linspace(1.0, 700.0, 900)
    wavelength = 450e-9
    theta_mas = 0.55
    theta_rad = theta_mas * 1e-3 / 3600.0 * np.pi / 180.0
    x = np.pi * baseline * theta_rad / wavelength
    vis2 = disk_visibility(x) ** 2
    dvis2_dlogtheta = x * np.gradient(vis2, x)
    sigma_vis2 = 0.035
    fisher = (dvis2_dlogtheta / sigma_vis2) ** 2
    fisher = fisher / np.nanmax(fisher)
    fig, ax1 = plt.subplots(figsize=(4.1, 2.7))
    ax2 = ax1.twinx()
    ax1.plot(baseline, vis2, color=COLORS["blue"], label=r"$|V|^2$")
    ax2.plot(baseline, fisher, color=COLORS["orange"], label=r"relative Fisher density")
    best = baseline[np.argmax(fisher)]
    ax1.axvline(best, color=COLORS["black"], ls="--", lw=0.8)
    ax1.set(xlabel="baseline B [m]", ylabel=r"squared visibility $|V|^2$")
    ax2.set(ylabel=r"information on $\ln\theta_\star$")
    ax1.set_ylim(-0.04, 1.05)
    ax2.set_ylim(-0.04, 1.12)
    lines = ax1.get_lines()[:1] + ax2.get_lines()[:1]
    ax1.legend(lines, [line.get_label() for line in lines], frameon=False, loc="upper right")
    clean_axis(ax1, grid=True)
    ax2.spines["top"].set_visible(False)
    save_figure(fig, outdir, filename)


def ch09_radiation_g2_diagnostics(outdir: Path, filename: str) -> None:
    tau = np.linspace(-6, 6, 900)
    thermal_single = 1.0 + np.exp(-np.abs(tau))
    thermal_multimode = 1.0 + 0.12 * np.exp(-np.abs(tau))
    coherent = np.ones_like(tau)
    noisy_maser = 1.0 + 0.05 * np.cos(6.0 * tau) * np.exp(-np.abs(tau) / 1.8)
    fig, ax = plt.subplots(figsize=(4.05, 2.65))
    ax.plot(tau, thermal_single, color=COLORS["blue"], label=r"thermal, $M=1$")
    ax.plot(tau, thermal_multimode, color=COLORS["sky"], label=r"thermal, $M\simeq8$")
    ax.plot(tau, coherent, color=COLORS["black"], label="coherent state")
    ax.plot(tau, noisy_maser, color=COLORS["orange"], label="narrow coherent component")
    ax.set(xlabel=r"delay $\tau/\tau_c$", ylabel=r"$g^{(2)}(\tau)$", ylim=(0.9, 2.08))
    ax.legend(frameon=False)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch09_diagnostic_plane(outdir: Path, filename: str) -> None:
    labels = ["thermal dust", "HII free-free", "synchrotron", "ECM", "H2O maser", "FRB"]
    log_tb = np.array([2.0, 4.0, 8.5, 13.0, 15.0, 35.0])
    pol = np.array([0.03, 0.02, 0.45, 0.85, 0.35, 0.75])
    bunch = np.array([0.55, 0.25, 0.15, 0.05, 0.04, 0.02])
    fig, ax = plt.subplots(figsize=(4.3, 2.9))
    ax.scatter(log_tb, pol, s=1200 * bunch + 70, c=PALETTE[:6], alpha=0.82)
    label_pos = {
        "thermal dust": (1.10, 0.060, "left"),
        "HII free-free": (4.45, 0.025, "left"),
        "synchrotron": (9.05, 0.480, "left"),
        "ECM": (13.55, 0.890, "left"),
        "H2O maser": (15.45, 0.385, "left"),
        "FRB": (35.45, 0.780, "left"),
    }
    for label in labels:
        x, y, ha = label_pos[label]
        ax.text(
            x,
            y,
            label,
            fontsize=7.2,
            ha=ha,
            va="center",
            bbox=dict(fc="white", ec="none", alpha=0.72, pad=0.2),
        )
    ax.axvspan(10, 38, color=COLORS["orange"], alpha=0.08)
    ax.text(10.8, 0.075, "coherent required", color=COLORS["orange"], fontsize=7.2)
    ax.set(xlabel=r"$\log_{10} T_b$ [K]", ylabel="polarization fraction", xlim=(0, 38), ylim=(0, 1.02))
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch09_brightness_temperature_scale(outdir: Path, filename: str) -> None:
    labels = ["stellar photosphere", "HII region", "solar burst limit", "pulsar giant pulse", "FRB"]
    values = np.array([3.8, 4.2, 10.0, 28.0, 35.0])
    colors = [COLORS["blue"], COLORS["green"], COLORS["yellow"], COLORS["purple"], COLORS["orange"]]
    y = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(4.2, 2.65))
    ax.barh(y, values, color=colors, alpha=0.88)
    ax.axvline(10.0, color=COLORS["black"], lw=0.85, ls="--")
    ax.text(10.35, 0.2, "incoherent radio ceiling", fontsize=7.2, rotation=90, va="bottom")
    ax.set(yticks=y, yticklabels=labels, xlabel=r"$\log_{10} T_b$ [K]", xlim=(0, 37))
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch09_thermal_mode_dilution(outdir: Path, filename: str) -> None:
    dt = np.logspace(-2, 5, 600)
    fig, ax = plt.subplots(figsize=(3.9, 2.65))
    for modes, color in zip([1, 2, 20, 200], PALETTE[:4]):
        contrast = 1.0 / (modes * (1.0 + dt))
        ax.loglog(dt, contrast, color=color, label=fr"$M_0={modes}$")
    ax.set(xlabel=r"time bin $\Delta t/\tau_c$", ylabel=r"measured $g^{(2)}(0)-1$")
    ax.legend(frameon=False, title="spatial/pol modes")
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch09_spectral_mechanisms(outdir: Path, filename: str) -> None:
    nu = np.logspace(-3, 3, 800)
    blackbody = nu ** 3 / np.expm1(np.clip(nu, 1e-6, 80))
    freefree = nu ** (-0.1) * np.exp(-nu / 120)
    synch = nu ** (-0.7) * np.exp(-nu / 250) / (1 + (0.03 / nu) ** 2.2)
    compton = np.exp(-0.5 * (np.log10(nu / 25.0) / 0.42) ** 2)
    curves = {
        "blackbody": blackbody,
        "free-free": freefree,
        "synchrotron": synch,
        "Compton bump": compton,
    }
    fig, ax = plt.subplots(figsize=(4.25, 2.75))
    for (label, y), color in zip(curves.items(), PALETTE[:4]):
        ax.loglog(nu, y / np.nanmax(y), color=color, label=label)
    ax.set(xlabel=r"frequency $\nu/\nu_0$", ylabel=r"normalized $\nu I_\nu$")
    ax.legend(frameon=False)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch10_stellar_diameter_visibility(outdir: Path, filename: str) -> None:
    baseline = np.linspace(0, 700, 800)
    wavelength = 416e-9
    mas_to_rad = np.pi / (180 * 3600 * 1000)
    fig, ax = plt.subplots(figsize=(4.0, 2.65))
    for diameter, color in zip([0.2, 0.5, 1.0, 1.5], PALETTE[:4]):
        theta = diameter * mas_to_rad
        x = np.pi * baseline * theta / wavelength
        ax.plot(baseline, disk_visibility(x) ** 2, color=color, label=fr"{diameter} mas")
    ax.axvspan(35, 170, color=COLORS["light_grey"], alpha=0.55, label="VERITAS-like")
    ax.set(xlabel="baseline B [m]", ylabel=r"$|V|^2$")
    ax.legend(frameon=False)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch10_binary_visibility(outdir: Path, filename: str) -> None:
    baseline = np.linspace(0, 550, 900)
    wavelength = 450e-9
    mas_to_rad = np.pi / (180 * 3600 * 1000)
    fig, ax = plt.subplots(figsize=(4.0, 2.65))
    cases = [(0.5, 1.0), (0.5, 0.3), (1.2, 0.3)]
    for (sep_mas, ratio), color in zip(cases, PALETTE[:3]):
        phase = 2 * np.pi * baseline * sep_mas * mas_to_rad / wavelength
        vis2 = (1 + ratio ** 2 + 2 * ratio * np.cos(phase)) / (1 + ratio) ** 2
        ax.plot(baseline, vis2, color=color, label=fr"$d={sep_mas}$ mas, $f={ratio}$")
    ax.set(xlabel="projected baseline B [m]", ylabel=r"binary $|V|^2$")
    ax.legend(frameon=False)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch10_limb_darkening(outdir: Path, filename: str) -> None:
    from scipy.special import j0

    r = np.linspace(0, 1, 500)
    x = np.linspace(0, 16, 360)
    fig, axes = plt.subplots(1, 2, figsize=(6.35, 2.45))
    for u_ld, color in zip([0.0, 0.4, 0.8], PALETTE[:3]):
        intensity = 1 - u_ld * (1 - np.sqrt(1 - r ** 2))
        norm = np.trapezoid(intensity * r, r)
        kernel = j0(np.outer(x, r))
        visibility = np.trapezoid(kernel * intensity[None, :] * r[None, :], r, axis=1) / norm
        axes[0].plot(r, intensity, color=color, label=fr"$u={u_ld}$")
        axes[1].plot(x, visibility ** 2, color=color, label=fr"$u={u_ld}$")
    axes[0].set(xlabel="normalized radius", ylabel="surface brightness")
    axes[1].set(xlabel=r"$\pi\theta B/\lambda$", ylabel=r"$|V|^2$")
    for i, ax in enumerate(axes):
        panel_label(ax, "ab"[i])
        ax.legend(frameon=False)
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch10_rotation_oblateness(outdir: Path, filename: str) -> None:
    baseline = np.linspace(0, 250, 700)
    wavelength = 416e-9
    mas_to_rad = np.pi / (180 * 3600 * 1000)
    theta_minor = 0.43 * mas_to_rad
    theta_major = 1.28 * theta_minor
    fig, ax = plt.subplots(figsize=(4.0, 2.65))
    for label, theta, color in [
        ("minor-axis baseline", theta_major, COLORS["blue"]),
        ("major-axis baseline", theta_minor, COLORS["orange"]),
        ("45 deg baseline", np.sqrt((theta_major ** 2 + theta_minor ** 2) / 2), COLORS["green"]),
    ]:
        x = np.pi * baseline * theta / wavelength
        ax.plot(baseline, disk_visibility(x) ** 2, color=color, label=label)
    ax.set(xlabel="projected baseline B [m]", ylabel=r"elliptical photosphere $|V|^2$")
    ax.legend(frameon=False)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch10_teff_error_budget(outdir: Path, filename: str) -> None:
    theta_err = np.linspace(0, 0.12, 240)
    f_err = np.linspace(0, 0.12, 240)
    th, ff = np.meshgrid(theta_err, f_err)
    teff = 0.25 * np.sqrt(ff ** 2 + (2 * th) ** 2)
    fig, ax = plt.subplots(figsize=(3.75, 2.85))
    im = ax.contourf(theta_err * 100, f_err * 100, teff * 100, levels=np.linspace(0, 7, 15), cmap="viridis")
    cs = ax.contour(theta_err * 100, f_err * 100, teff * 100, colors="white", linewidths=0.7, levels=[1, 2, 3, 5])
    ax.clabel(cs, inline=True, fontsize=7, fmt="%g%%")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03, label=r"$\sigma(T_{\rm eff})/T_{\rm eff}$ [%]")
    ax.set(xlabel=r"angular-diameter error $\sigma_\theta/\theta$ [%]", ylabel=r"bolometric-flux error $\sigma_F/F$ [%]")
    clean_axis(ax)
    save_figure(fig, outdir, filename)


def ch11_white_dwarf_mass_radius(outdir: Path, filename: str) -> None:
    mass = np.linspace(0.2, 1.38, 700)
    m_ch = 1.44
    radius_rsun = 0.0112 * np.sqrt((m_ch / mass) ** (2.0 / 3.0) - (mass / m_ch) ** (2.0 / 3.0))
    radius_rearth = radius_rsun * 109.1
    v_gr = 0.636 * mass / radius_rsun
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 2.55))
    axes[0].plot(mass, radius_rearth, color=COLORS["blue"])
    axes[0].scatter([0.6], [np.interp(0.6, mass, radius_rearth)], color=COLORS["orange"], zorder=3)
    axes[0].annotate(r"typical DA", (0.6, np.interp(0.6, mass, radius_rearth)), xytext=(0.72, 1.62),
                     arrowprops={"arrowstyle": "-", "lw": 0.7, "color": COLORS["grey"]}, fontsize=7.2)
    axes[0].set(xlabel=r"white-dwarf mass $M/M_\odot$", ylabel=r"radius $R/R_\oplus$")
    panel_label(axes[0], "a")
    axes[1].plot(mass, v_gr, color=COLORS["green"])
    axes[1].axhspan(20, 80, color=COLORS["light_grey"], alpha=0.8)
    axes[1].text(0.24, 62, "Balmer-line\nredshift scale", fontsize=7.2, color=COLORS["grey"])
    axes[1].set(xlabel=r"white-dwarf mass $M/M_\odot$", ylabel=r"$v_{\rm gr}=GM/(Rc)$ [km s$^{-1}$]")
    panel_label(axes[1], "b")
    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch11_magnetic_cv_flow_map(outdir: Path, filename: str) -> None:
    fig, ax = plt.subplots(figsize=(3.75, 2.75))
    ax.set_xscale("log")
    ax.set_yscale("log")
    mu = np.logspace(32, 36, 10)
    ax.fill_between(mu, 0.006, 0.1, color=COLORS["blue"], alpha=0.12)
    ax.fill_between(mu, 0.1, 0.6, color=COLORS["orange"], alpha=0.13)
    ax.fill_between(mu, 0.6, 1.0, color=COLORS["green"], alpha=0.14)
    ax.axhline(0.1, color=COLORS["grey"], lw=0.8, ls="--")
    ax.axhline(0.6, color=COLORS["grey"], lw=0.8, ls="--")
    samples = {
        "DQ Her": (2.5e32, 0.011),
        "FO Aqr": (1.8e33, 0.07),
        "EX Hya": (8.0e33, 0.68),
        "AE Aqr": (3.0e34, 0.004),
        "AM Her": (2.0e35, 1.0),
    }
    for label, (x, y) in samples.items():
        ax.scatter(x, y, s=22, color=COLORS["black"], zorder=3)
        ax.text(x * 1.08, y * 1.08, label, fontsize=6.9)
    ax.text(1.3e32, 0.025, "disc-like", color=COLORS["blue"], fontsize=8)
    ax.text(1.3e32, 0.23, "stream-like", color=COLORS["orange"], fontsize=8)
    ax.text(1.3e32, 0.76, "ring or synchronous", color=COLORS["green"], fontsize=8)
    ax.set(xlim=(1e32, 1e36), ylim=(0.006, 1.2), xlabel=r"white-dwarf magnetic moment $\mu$ [G cm$^3$]",
           ylabel=r"$P_{\rm spin}/P_{\rm orb}$")
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch11_light_cylinder_phase(outdir: Path, filename: str) -> None:
    period = np.logspace(-3, 4, 700)
    r_lc = 2.99792458e5 * period / (2.0 * np.pi)
    fig, axes = plt.subplots(1, 2, figsize=(6.65, 2.55))
    axes[0].loglog(period, r_lc, color=COLORS["blue"])
    axes[0].axhline(12, color=COLORS["black"], lw=0.85, ls=":", label=r"$R_{\rm NS}=12$ km")
    axes[0].axhline(8500, color=COLORS["grey"], lw=0.85, ls="--", label=r"$R_{\rm WD}\simeq8500$ km")
    markers = {"MSP": 0.004, "Crab": 0.033, "4U 0142": 8.69, "WD spin": 1000.0}
    for label, p in markers.items():
        axes[0].scatter([p], [2.99792458e5 * p / (2.0 * np.pi)], color=COLORS["orange"], zorder=3)
        axes[0].text(p * 1.25, 2.99792458e5 * p / (2.0 * np.pi) * 0.8, label, fontsize=6.9)
    axes[0].set(xlabel="spin period P [s]", ylabel=r"light-cylinder radius $R_{\rm LC}$ [km]")
    axes[0].legend(frameon=False, loc="lower right")
    panel_label(axes[0], "a")

    phase = np.linspace(0, 1, 700)
    profile = 0.18 + 1.0 * np.exp(-0.5 * ((phase - 0.02) / 0.018) ** 2)
    profile += 0.46 * np.exp(-0.5 * ((phase - 0.40) / 0.030) ** 2)
    axes[1].plot(phase, profile / profile.max(), color=COLORS["purple"])
    axes[1].fill_between(phase, 0, profile / profile.max(), where=(phase < 0.08), color=COLORS["purple"], alpha=0.18)
    axes[1].fill_between(phase, 0, profile / profile.max(), where=((phase > 0.34) & (phase < 0.48)), color=COLORS["orange"], alpha=0.18)
    axes[1].set(xlabel=r"rotational phase $\phi$", ylabel="normalized counts")
    axes[1].text(0.015, 0.88, "main pulse", fontsize=7.2)
    axes[1].text(0.36, 0.48, "interpulse", fontsize=7.2)
    panel_label(axes[1], "b")
    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch11_stokes_qu_track(outdir: Path, filename: str) -> None:
    phase = np.linspace(0.0, 1.0, 700)
    alpha = np.deg2rad(45.0)
    zeta = np.deg2rad(70.0)
    phi = 2.0 * np.pi * (phase - 0.5)
    psi = 0.5 * np.arctan2(np.sin(alpha) * np.sin(phi),
                           np.sin(zeta) * np.cos(alpha) - np.cos(zeta) * np.sin(alpha) * np.cos(phi))
    pd = 0.10 + 0.30 * np.exp(-0.5 * ((phase - 0.50) / 0.18) ** 2)
    q = pd * np.cos(2.0 * psi)
    u = pd * np.sin(2.0 * psi)
    fig, axes = plt.subplots(1, 2, figsize=(6.45, 2.55))
    axes[0].plot(phase, q, color=COLORS["blue"], label=r"$Q/I$")
    axes[0].plot(phase, u, color=COLORS["orange"], label=r"$U/I$")
    axes[0].axhline(0.0, color=COLORS["grey"], lw=0.7)
    axes[0].set(xlabel=r"rotational phase $\phi$", ylabel="normalized Stokes")
    axes[0].legend(frameon=False)
    panel_label(axes[0], "a")
    axes[1].plot(q, u, color=COLORS["purple"])
    axes[1].scatter(q[::120], u[::120], color=COLORS["black"], s=10, zorder=3)
    axes[1].set(xlabel=r"$Q/I$", ylabel=r"$U/I$", aspect="equal")
    panel_label(axes[1], "b")
    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch11_birefringence_energy(outdir: Path, filename: str) -> None:
    energy = np.array([2.4, 3.3, 4.5, 6.6])
    pd = np.array([0.14, 0.14, 0.00, 0.41])
    pd_err = np.array([0.01, 0.01, 0.09, 0.07])
    pa = np.array([48.0, 50.0, 5.0, -44.0])
    pa_err = np.array([3.0, 4.0, 35.0, 5.0])
    fig, axes = plt.subplots(1, 2, figsize=(6.4, 2.55), sharex=True)
    axes[0].errorbar(energy, pd * 100.0, yerr=pd_err * 100.0, fmt="o", color=COLORS["blue"], capsize=2.5)
    axes[0].axvspan(4.0, 5.0, color=COLORS["light_grey"], alpha=0.85)
    axes[0].text(4.08, 28, "mode\nmixing", fontsize=7.0, color=COLORS["grey"])
    axes[0].set(xlabel="photon energy [keV]", ylabel="linear polarization [%]", ylim=(-3, 55))
    panel_label(axes[0], "a")
    axes[1].errorbar(energy, pa, yerr=pa_err, fmt="o", color=COLORS["orange"], capsize=2.5)
    axes[1].axhline(48, color=COLORS["grey"], lw=0.75, ls="--")
    axes[1].axhline(-44, color=COLORS["grey"], lw=0.75, ls="--")
    axes[1].axvspan(4.0, 5.0, color=COLORS["light_grey"], alpha=0.85)
    axes[1].set(xlabel="photon energy [keV]", ylabel="polarization angle [deg]", ylim=(-90, 90))
    panel_label(axes[1], "b")
    for ax in axes:
        ax.set_xlim(2.0, 8.0)
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch11_hotspot_lightcurve(outdir: Path, filename: str) -> None:
    phase = np.linspace(0.0, 1.0, 900)
    inc = np.deg2rad(62.0)
    colat = np.deg2rad(42.0)
    cospsi = np.sin(inc) * np.sin(colat) * np.cos(2.0 * np.pi * phase) + np.cos(inc) * np.cos(colat)
    fig, ax = plt.subplots(figsize=(3.75, 2.55))
    for u, color in [(0.20, COLORS["blue"]), (0.32, COLORS["orange"]), (0.44, COLORS["green"])]:
        cos_alpha = u + (1.0 - u) * cospsi
        flux = np.clip(cos_alpha, 0.0, None)
        flux = flux / flux.mean()
        ax.plot(phase, flux, color=color, label=fr"$u=2GM/Rc^2={u:.2f}$")
    ax.set(xlabel=r"rotational phase $\phi$", ylabel="relative hotspot flux")
    ax.legend(frameon=False)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch12_black_hole_scales(outdir: Path, filename: str) -> None:
    mass = np.logspace(1, 10, 700)
    tg = 4.9255e-6 * mass
    rg_km = 1.4766 * mass
    fig, axes = plt.subplots(1, 2, figsize=(6.55, 2.55))
    axes[0].loglog(mass, tg, color=COLORS["blue"])
    axes[0].scatter([4.0e6, 6.5e9], [4.9255e-6 * 4.0e6, 4.9255e-6 * 6.5e9],
                    color=COLORS["orange"], zorder=3)
    axes[0].text(4.4e6, 14, "Sgr A*", fontsize=7.2)
    axes[0].text(2.2e9, 5.5e4, "M87*", fontsize=7.2)
    axes[0].set(xlabel=r"black-hole mass $M/M_\odot$", ylabel=r"$t_g=GM/c^3$ [s]")
    panel_label(axes[0], "a")

    distances_pc = {"Sgr A*": 8.2e3, "M87*": 16.8e6, "AGN at 100 Mpc": 1.0e8}
    masses = np.logspace(5, 10, 400)
    pc_km = 3.085677581e13
    rad_to_uas = 180.0 / np.pi * 3600.0 * 1e6
    for label, dpc in distances_pc.items():
        theta = 1.4766 * masses / (dpc * pc_km) * rad_to_uas
        axes[1].loglog(masses, 10.4 * theta, label=label)
    axes[1].axhspan(20, 60, color=COLORS["light_grey"], alpha=0.65)
    axes[1].set(xlabel=r"black-hole mass $M/M_\odot$", ylabel=r"shadow diameter [${\mu}$as]")
    axes[1].legend(frameon=False, fontsize=6.7)
    panel_label(axes[1], "b")
    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch12_accretion_disk_radii(outdir: Path, filename: str) -> None:
    wavelength = np.linspace(1200, 9000, 500)
    radius_ld = 0.46 * (wavelength / 2500.0) ** (4.0 / 3.0)
    t_orb = 18.0 * (radius_ld / 0.46) ** 1.5
    t_th = t_orb / 0.1
    fig, axes = plt.subplots(1, 2, figsize=(6.55, 2.55))
    axes[0].plot(wavelength, radius_ld, color=COLORS["blue"], label=r"$R_\lambda \propto \lambda^{4/3}$")
    axes[0].fill_between(wavelength, radius_ld, 4.0 * radius_ld, color=COLORS["orange"], alpha=0.16,
                         label="microlensing larger")
    axes[0].set(xlabel=r"rest wavelength $\lambda$ [Angstrom]", ylabel=r"half-light scale [light days]")
    axes[0].legend(frameon=False)
    panel_label(axes[0], "a")
    axes[1].loglog(radius_ld, t_orb, color=COLORS["green"], label="orbital")
    axes[1].loglog(radius_ld, t_th, color=COLORS["purple"], label=r"thermal, $\alpha=0.1$")
    axes[1].set(xlabel="disk radius [light days]", ylabel="rest-frame timescale [days]")
    axes[1].legend(frameon=False)
    panel_label(axes[1], "b")
    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch12_blr_reverberation_interferometry(outdir: Path, filename: str) -> None:
    lum = np.logspace(42, 47, 500)
    rblr = 33.7 * (lum / 1e44) ** 0.533
    velocity = np.linspace(-4500, 4500, 500)
    phase_major = 0.55 * np.tanh(velocity / 1600.0) * np.exp(-(velocity / 5200.0) ** 2)
    phase_minor = 0.12 * np.tanh(velocity / 1600.0) * np.exp(-(velocity / 5200.0) ** 2)
    fig, axes = plt.subplots(1, 2, figsize=(6.55, 2.55))
    axes[0].loglog(lum, rblr, color=COLORS["blue"])
    axes[0].scatter([3e46], [145], color=COLORS["orange"], zorder=3)
    axes[0].text(1.3e46, 190, "3C 273\nPa alpha", fontsize=7.0)
    axes[0].set(xlabel=r"$\lambda L_\lambda(5100{\rm A})$ [erg s$^{-1}$]",
                ylabel=r"$R_{\rm BLR}$ [light days]")
    panel_label(axes[0], "a")
    axes[1].plot(velocity, phase_major, color=COLORS["purple"], label="baseline along rotation")
    axes[1].plot(velocity, phase_minor, color=COLORS["grey"], label="misaligned baseline")
    axes[1].axhline(0, color=COLORS["black"], lw=0.75)
    axes[1].set(xlabel=r"line-of-sight velocity [km s$^{-1}$]", ylabel="differential phase [deg]")
    axes[1].legend(frameon=False)
    panel_label(axes[1], "b")
    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch12_photon_ring_visibility(outdir: Path, filename: str) -> None:
    baseline = np.linspace(0.05, 100, 1000)
    uas_to_rad = np.pi / (180.0 * 3600.0 * 1e6)
    diameter = 42.0 * uas_to_rad
    u = baseline * 1e9
    thin = np.abs(j0_numeric(np.pi * diameter * u))
    fig, axes = plt.subplots(1, 2, figsize=(6.55, 2.55))
    for width_uas, color, label in [(3, COLORS["blue"], "narrow ring"), (10, COLORS["orange"], "thick flow"), (20, COLORS["green"], "broad crescent")]:
        sigma = (width_uas * uas_to_rad) / 2.355
        envelope = np.exp(-2.0 * (np.pi * sigma * u) ** 2)
        axes[0].plot(baseline, thin * envelope, color=color, label=label)
    axes[0].set(xlabel=r"projected baseline [$G\lambda$]", ylabel=r"visibility amplitude $|V|$")
    axes[0].legend(frameon=False)
    panel_label(axes[0], "a")

    n = np.arange(0, 5)
    width = 20.0 * np.exp(-1.7 * n)
    flux = 1.0 * np.exp(-1.3 * n)
    axes[1].semilogy(n, width / width[0], "o-", color=COLORS["purple"], label="relative width")
    axes[1].semilogy(n, flux / flux[0], "s-", color=COLORS["grey"], label="relative flux")
    axes[1].set(xlabel="subring index n", ylabel="relative scale")
    axes[1].legend(frameon=False)
    panel_label(axes[1], "b")
    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch12_variability_autocorrelation(outdir: Path, filename: str) -> None:
    tau = np.linspace(0, 900, 700)
    freq = np.logspace(-3, 1, 700)
    fig, axes = plt.subplots(1, 2, figsize=(6.55, 2.55))
    for tc, color in [(30, COLORS["blue"]), (100, COLORS["orange"]), (300, COLORS["green"])]:
        axes[0].plot(tau, np.exp(-tau / tc), color=color, label=fr"$\tau_d={tc}$ d")
        psd = 1.0 / (1.0 + (2.0 * np.pi * freq * tc) ** 2)
        axes[1].loglog(freq, psd / psd.max(), color=color)
    axes[0].set(xlabel="rest-frame lag [days]", ylabel="DRW autocorrelation")
    axes[1].set(xlabel=r"frequency [day$^{-1}$]", ylabel="normalized PSD")
    axes[0].legend(frameon=False)
    panel_label(axes[0], "a")
    panel_label(axes[1], "b")
    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch12_hawking_temperature_scale(outdir: Path, filename: str) -> None:
    mass = np.logspace(-18, 10, 900)
    temp = 6.17e-8 / mass
    lifetime = 2.1e67 * mass ** 3
    fig, axes = plt.subplots(1, 2, figsize=(6.55, 2.55))
    axes[0].loglog(mass, temp, color=COLORS["blue"])
    axes[0].axhline(2.725, color=COLORS["grey"], lw=0.85, ls="--", label="CMB")
    axes[0].scatter([1.0, 4e6, 6.5e9], [6.17e-8, 6.17e-8 / 4e6, 6.17e-8 / 6.5e9],
                    color=COLORS["orange"], s=18, zorder=3)
    axes[0].set(xlabel=r"black-hole mass $M/M_\odot$", ylabel=r"$T_H$ [K]")
    axes[0].legend(frameon=False)
    panel_label(axes[0], "a")
    axes[1].loglog(mass, lifetime, color=COLORS["purple"])
    axes[1].axhline(1.38e10, color=COLORS["grey"], lw=0.85, ls="--", label="Universe age")
    axes[1].set(xlabel=r"black-hole mass $M/M_\odot$", ylabel="evaporation time [yr]")
    axes[1].legend(frameon=False)
    panel_label(axes[1], "b")
    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch13_transient_event_likelihood(outdir: Path, filename: str) -> None:
    rng = np.random.default_rng(13)
    t = np.linspace(0.0, 36.0, 1800)
    dt = t[1] - t[0]
    bg, amp, t0_true, tau_true = 0.22, 7.2, 9.0, 7.0
    true_rate = bg + amp * np.exp(-(t - t0_true) / tau_true) * (t >= t0_true)
    events = np.repeat(t, rng.poisson(true_rate * dt))

    t0_grid = np.linspace(6.5, 11.5, 90)
    tau_grid = np.linspace(3.0, 14.5, 95)
    log_like = np.empty((tau_grid.size, t0_grid.size))
    for i, tau in enumerate(tau_grid):
        for j, t0 in enumerate(t0_grid):
            model_t = bg + amp * np.exp(-(t - t0) / tau) * (t >= t0)
            model_e = bg + amp * np.exp(-(events - t0) / tau) * (events >= t0)
            log_like[i, j] = np.sum(np.log(model_e)) - np.trapezoid(model_t, t)
    like = np.exp(log_like - np.max(log_like))

    fig, axes = plt.subplots(1, 2, figsize=(6.55, 2.75))
    axes[0].plot(t, true_rate, color=COLORS["blue"], lw=1.5, label="true rate")
    axes[0].eventplot(events, lineoffsets=-0.75, linelengths=0.42, colors=COLORS["black"], linewidths=0.55)
    axes[0].axvline(t0_true, color=COLORS["orange"], lw=0.9, ls="--", label=r"$t_0$")
    axes[0].set(xlabel="time after alert [h]", ylabel=r"rate [ph h$^{-1}$]", ylim=(-1.15, 8.2))
    axes[0].legend(frameon=False, loc="upper right")
    panel_label(axes[0], "a")

    levels = [0.05, 0.16, 0.5, 0.85]
    im = axes[1].contourf(t0_grid, tau_grid, like, levels=np.r_[0.0, levels, 1.0], cmap="viridis")
    axes[1].contour(t0_grid, tau_grid, like, levels=levels, colors="white", linewidths=0.55)
    axes[1].plot(t0_true, tau_true, "o", ms=4, color=COLORS["orange"])
    axes[1].set(xlabel=r"trigger time $t_0$ [h]", ylabel=r"decay time $\tau$ [h]")
    fig.colorbar(im, ax=axes[1], pad=0.02, label="relative likelihood")
    panel_label(axes[1], "b")
    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch13_expanding_fireball_resolution(outdir: Path, filename: str) -> None:
    days = np.logspace(-1.0, 3.0, 600)
    sec = days * 86400.0
    rad_to_uas = 180.0 / np.pi * 3600.0 * 1e6
    cases = [
        ("nova: 1000 km/s, 2 kpc", 1.0e6, 2.0e3 * 3.086e16, COLORS["blue"]),
        ("SN Ia: 10000 km/s, 20 Mpc", 1.0e7, 20.0e6 * 3.086e16, COLORS["orange"]),
        ("kilonova: 0.2c, 40 Mpc", 0.2 * 2.998e8, 40.0e6 * 3.086e16, COLORS["green"]),
    ]
    fig, ax = plt.subplots(figsize=(4.35, 2.85))
    for label, velocity, distance, color in cases:
        theta = velocity * sec / distance * rad_to_uas
        ax.loglog(days, theta, color=color, label=label)
    for baseline, y in [(1, 126.0), (10, 12.6), (100, 1.26)]:
        ax.axhline(y, color=COLORS["grey"], lw=0.75, ls="--")
        ax.text(0.12, y * 1.07, fr"$B={baseline}$ km", fontsize=7.2, color=COLORS["grey"])
    ax.set(xlabel="time after explosion [d]", ylabel=r"angular radius $\theta$ [$\mu$as]", ylim=(1e-3, 4e3))
    ax.legend(frameon=False, fontsize=7.2)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch13_multimessenger_delay(outdir: Path, filename: str) -> None:
    channels = ["GW", "gamma", "optical", "X/radio"]
    delay_s = np.array([0.03, 1.74, 11.0 * 3600.0, 9.0 * 86400.0])
    err_s = np.array([0.03, 0.05, 3600.0, 2.0 * 86400.0])
    fig, axes = plt.subplots(1, 2, figsize=(6.55, 2.75))
    axes[0].errorbar(delay_s, np.arange(len(channels)), xerr=err_s, fmt="o", color=COLORS["blue"], ecolor=COLORS["grey"], capsize=2)
    axes[0].set_xscale("log")
    axes[0].set(yticks=np.arange(len(channels)), yticklabels=channels, xlabel="delay from merger [s]")
    axes[0].axvline(1.74, color=COLORS["orange"], lw=0.85, ls="--")
    panel_label(axes[0], "a")

    delay = np.logspace(-3, 5, 500)
    distance_c = 40.0e6 * 3.086e16 / 2.998e8
    frac = delay / distance_c
    axes[1].loglog(delay, frac, color=COLORS["purple"])
    axes[1].scatter([1.74], [1.74 / distance_c], color=COLORS["orange"], s=20, zorder=4)
    axes[1].set(xlabel="allowed propagation delay [s]", ylabel=r"$|\Delta v|/c$ at 40 Mpc")
    panel_label(axes[1], "b")
    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch13_kilonova_color_evolution(outdir: Path, filename: str) -> None:
    h = 6.62607015e-34
    c = 2.99792458e8
    k_b = 1.380649e-23
    sigma = 5.670374419e-8
    lam_um = np.linspace(0.32, 2.4, 650)
    lam = lam_um * 1e-6
    epochs = [
        ("0.6 d, 8300 K", 8300.0, 4.5e12, COLORS["blue"]),
        ("2 d, 5000 K", 5000.0, 7.2e12, COLORS["orange"]),
        ("7 d, 2800 K", 2800.0, 9.0e12, COLORS["green"]),
    ]
    fig, axes = plt.subplots(1, 2, figsize=(6.55, 2.75))
    for label, temp, radius_m, color in epochs:
        bb = (2.0 * h * c ** 2 / lam ** 5) / np.expm1(h * c / (lam * k_b * temp))
        lam_lam = 4.0 * np.pi ** 2 * radius_m ** 2 * lam * bb
        axes[0].plot(lam_um, lam_lam / lam_lam.max(), color=color, label=label)
    axes[0].set(xlabel=r"wavelength [$\mu$m]", ylabel=r"normalized $\lambda L_\lambda$")
    axes[0].legend(frameon=False, fontsize=7.2)
    panel_label(axes[0], "a")

    kappa = np.logspace(-1, 1.2, 500)
    comps = [
        ("blue", 0.01, 0.27, COLORS["blue"]),
        ("purple", 0.04, 0.15, COLORS["purple"]),
        ("red", 0.04, 0.10, COLORS["orange"]),
    ]
    msun = 1.98847e30
    for label, mass_msun, velocity_c, color in comps:
        mass = mass_msun * msun
        velocity = velocity_c * c
        tdiff = np.sqrt(kappa * 0.1 * mass / (4.0 * np.pi * velocity * c)) / 86400.0
        axes[1].loglog(kappa, tdiff, color=color, label=label)
    axes[1].set(xlabel=r"opacity $\kappa$ [cm$^2$ g$^{-1}$]", ylabel=r"diffusion time [d]")
    axes[1].legend(frameon=False, fontsize=7.2)
    panel_label(axes[1], "b")
    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch13_afterglow_synchrotron_breaks(outdir: Path, filename: str) -> None:
    p = 2.3
    nu = np.logspace(8, 19, 700)
    nu_m, nu_c = 8.0e13, 2.0e16
    spectrum = np.where(nu < nu_m, (nu / nu_m) ** (1.0 / 3.0), (nu / nu_m) ** (-(p - 1.0) / 2.0))
    spectrum *= np.where(nu > nu_c, (nu / nu_c) ** -0.5, 1.0)
    fig, axes = plt.subplots(1, 2, figsize=(6.55, 2.75))
    axes[0].loglog(nu, spectrum, color=COLORS["blue"])
    for x, label in [(nu_m, r"$\nu_m$"), (nu_c, r"$\nu_c$")]:
        axes[0].axvline(x, color=COLORS["grey"], lw=0.8, ls="--")
        axes[0].text(x * 1.07, 0.035, label, fontsize=8, color=COLORS["grey"])
    axes[0].set(xlabel=r"frequency $\nu$ [Hz]", ylabel=r"relative $F_\nu$")
    panel_label(axes[0], "a")

    time = np.logspace(-2, 2, 600)
    tb = 2.2
    alpha1, alpha2 = 1.15, 2.15
    optical = (time / 0.1) ** -alpha1 * (1.0 + (time / tb) ** 4) ** (-(alpha2 - alpha1) / 4.0)
    xray = 0.55 * (time / 0.1) ** -1.40
    axes[1].loglog(time, optical / optical.max(), color=COLORS["orange"], label="optical")
    axes[1].loglog(time, xray / optical.max(), color=COLORS["purple"], label="X-ray")
    axes[1].axvline(tb, color=COLORS["grey"], lw=0.8, ls="--", label="jet break")
    axes[1].set(xlabel="time after burst [d]", ylabel="relative flux")
    axes[1].legend(frameon=False, fontsize=7.2)
    panel_label(axes[1], "b")
    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch13_tde_fallback_reprocessing(outdir: Path, filename: str) -> None:
    time = np.logspace(0, 3, 650)
    tmin = 38.0
    mdot_peak = 2.5
    mdot = np.where(time < tmin, mdot_peak * (time / tmin) ** 0.8, mdot_peak * (time / tmin) ** (-5.0 / 3.0))
    edd = np.ones_like(time) * 0.025
    fig, axes = plt.subplots(1, 2, figsize=(6.55, 2.75))
    axes[0].loglog(time, mdot, color=COLORS["blue"], label=r"fallback $\dot M$")
    axes[0].loglog(time, edd, color=COLORS["grey"], ls="--", label=r"$\dot M_{\rm Edd}$")
    axes[0].axvline(tmin, color=COLORS["orange"], lw=0.85, ls=":")
    axes[0].set(xlabel="time after disruption [d]", ylabel=r"$\dot M$ [$M_\odot$ yr$^{-1}$]")
    axes[0].legend(frameon=False, fontsize=7.2)
    panel_label(axes[0], "a")

    t = np.linspace(0, 260, 500)
    radius = 10 ** (15.1 - 1.1 * (1.0 - np.exp(-t / 110.0)))
    temp = 1.4e4 + (5.0e4 - 1.4e4) * (1.0 - np.exp(-t / 95.0))
    axes[1].semilogy(t, radius, color=COLORS["green"], label=r"$R_{\rm BB}$")
    ax2 = axes[1].twinx()
    ax2.plot(t, temp / 1e4, color=COLORS["orange"], label=r"$T_{\rm BB}$")
    axes[1].set(xlabel="time after optical peak [d]", ylabel=r"$R_{\rm BB}$ [cm]")
    ax2.set_ylabel(r"$T_{\rm BB}$ [$10^4$ K]")
    axes[1].legend(frameon=False, fontsize=7.2, loc="upper right")
    ax2.legend(frameon=False, fontsize=7.2, loc="center right")
    panel_label(axes[1], "b")
    clean_axis(axes[1], grid=True)
    clean_axis(ax2)
    save_figure(fig, outdir, filename)


def ch14_dispersion_delay(outdir: Path, filename: str) -> None:
    nu = np.linspace(0.35, 2.0, 600)
    fig, axes = plt.subplots(1, 2, figsize=(6.95, 2.55))
    for dm in [50, 300, 1000]:
        delay = 4.148808 * dm * (nu ** -2 - 2.0 ** -2)
        axes[0].plot(nu, delay, label=fr"DM={dm}")
    axes[0].set(xlabel=r"frequency $\nu$ [GHz]", ylabel="delay to 2 GHz [ms]")
    axes[0].legend(frameon=False)
    panel_label(axes[0], "a")

    z = np.linspace(0.01, 1.6, 400)
    dm_mw_disk = np.full_like(z, 60.0)
    dm_mw_halo = np.full_like(z, 50.0)
    dm_host = 80.0 / (1.0 + z)
    dm_cosmic = 900.0 * z
    bottom = np.zeros_like(z)
    for values, label, color in [
        (dm_mw_disk, "MW disk", COLORS["grey"]),
        (dm_mw_halo, "MW halo", COLORS["sky"]),
        (dm_host, "host", COLORS["orange"]),
        (dm_cosmic, "cosmic", COLORS["blue"]),
    ]:
        axes[1].fill_between(z, bottom, bottom + values, color=color, alpha=0.8, label=label)
        bottom = bottom + values
    axes[1].set(xlabel="redshift z", ylabel=r"observed DM [pc cm$^{-3}$]")
    axes[1].legend(frameon=False, fontsize=6.7, loc="upper left")
    panel_label(axes[1], "b")
    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch14_faraday_rotation(outdir: Path, filename: str) -> None:
    lam2 = np.linspace(0.0, 0.22, 500)
    fig, axes = plt.subplots(1, 2, figsize=(6.85, 2.55))
    for rm in [10, 50, 150]:
        psi = np.degrees(rm * lam2)
        axes[0].plot(lam2, psi, label=fr"RM={rm}")
    wrapped = np.degrees(np.mod(80.0 * lam2, np.pi))
    axes[0].scatter(lam2[::28], wrapped[::28], s=8, color=COLORS["black"], alpha=0.7, label="wrapped")
    axes[0].set(xlabel=r"$\lambda^2$ [m$^2$]", ylabel=r"polarization angle $\psi$ [deg]")
    axes[0].legend(frameon=False, fontsize=6.8, ncol=2)
    panel_label(axes[0], "a")

    rm_grid = np.logspace(0, 4, 500)
    for dm, color in [(30, COLORS["green"]), (300, COLORS["blue"]), (1200, COLORS["orange"])]:
        axes[1].loglog(rm_grid, 1.232 * rm_grid / dm, color=color, label=fr"DM={dm}")
    axes[1].set(xlabel=r"$|{\rm RM}|$ [rad m$^{-2}$]", ylabel=r"$|\langle B_\parallel\rangle|$ [$\mu$G]")
    axes[1].legend(frameon=False)
    panel_label(axes[1], "b")
    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch14_scattering_broadening(outdir: Path, filename: str) -> None:
    t = np.linspace(-8.0, 42.0, 1500)
    dt = t[1] - t[0]
    intrinsic = np.exp(-0.5 * (t / 0.9) ** 2)
    intrinsic /= np.trapezoid(intrinsic, t)
    fig, axes = plt.subplots(1, 2, figsize=(6.95, 2.55))
    axes[0].plot(t, intrinsic / intrinsic.max(), color=COLORS["black"], lw=1.0, label="intrinsic")
    for nu, color in [(0.6, COLORS["orange"]), (1.0, COLORS["blue"]), (1.8, COLORS["green"])]:
        tau = 2.5 * nu ** (-4.0)
        kernel = np.where(t >= 0.0, np.exp(-t / tau) / tau, 0.0)
        kernel /= np.trapezoid(kernel, t)
        observed = np.convolve(intrinsic, kernel, mode="same") * dt
        observed /= observed.max()
        axes[0].plot(t, observed, color=color, label=fr"{nu:.1f} GHz")
    axes[0].set(xlabel="arrival time [ms]", ylabel="normalized pulse")
    axes[0].legend(frameon=False, fontsize=6.8)
    panel_label(axes[0], "a")

    dm = np.logspace(1.0, 3.35, 450)
    log_dm = np.log10(dm)
    for nu, color in [(0.6, COLORS["orange"]), (1.4, COLORS["blue"]), (3.0, COLORS["green"])]:
        log_tau = -6.46 + 0.154 * log_dm + 1.07 * log_dm ** 2 - 3.86 * np.log10(nu)
        tau = 10 ** log_tau
        axes[1].loglog(dm, tau, color=color, label=fr"{nu:.1f} GHz")
    mid = 10 ** (-6.46 + 0.154 * log_dm + 1.07 * log_dm ** 2 - 3.86 * np.log10(1.4))
    axes[1].fill_between(dm, mid / 10.0, mid * 10.0, color=COLORS["light_grey"], zorder=0, label="1 dex scatter")
    axes[1].set(xlabel=r"DM [pc cm$^{-3}$]", ylabel=r"$\tau_{\rm sc}$ [ms]")
    axes[1].legend(frameon=False, fontsize=6.8, loc="upper left")
    panel_label(axes[1], "b")
    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch14_dust_extinction_polarization(outdir: Path, filename: str) -> None:
    def ccm_a_b(x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        a = np.zeros_like(x)
        b = np.zeros_like(x)
        ir = (x >= 0.3) & (x < 1.1)
        a[ir] = 0.574 * x[ir] ** 1.61
        b[ir] = -0.527 * x[ir] ** 1.61

        opt = (x >= 1.1) & (x < 3.3)
        y = x[opt] - 1.82
        a[opt] = (
            1.0
            + 0.17699 * y
            - 0.50447 * y ** 2
            - 0.02427 * y ** 3
            + 0.72085 * y ** 4
            + 0.01979 * y ** 5
            - 0.77530 * y ** 6
            + 0.32999 * y ** 7
        )
        b[opt] = (
            1.41338 * y
            + 2.28305 * y ** 2
            + 1.07233 * y ** 3
            - 5.38434 * y ** 4
            - 0.62251 * y ** 5
            + 5.30260 * y ** 6
            - 2.09002 * y ** 7
        )

        uv = (x >= 3.3) & (x <= 8.0)
        xu = x[uv]
        fa = np.zeros_like(xu)
        fb = np.zeros_like(xu)
        high = xu > 5.9
        fa[high] = -0.04473 * (xu[high] - 5.9) ** 2 - 0.009779 * (xu[high] - 5.9) ** 3
        fb[high] = 0.2130 * (xu[high] - 5.9) ** 2 + 0.1207 * (xu[high] - 5.9) ** 3
        a[uv] = 1.752 - 0.316 * xu - 0.104 / ((xu - 4.67) ** 2 + 0.341) + fa
        b[uv] = -3.090 + 1.825 * xu + 1.206 / ((xu - 4.62) ** 2 + 0.263) + fb
        return a, b

    lam = np.linspace(0.125, 2.2, 650)
    x = 1.0 / lam
    a, b = ccm_a_b(x)
    fig, axes = plt.subplots(1, 2, figsize=(6.95, 2.55))
    for rv, color in [(2.5, COLORS["orange"]), (3.1, COLORS["blue"]), (5.5, COLORS["green"])]:
        axes[0].plot(lam, a + b / rv, color=color, label=fr"$R_V={rv}$")
    axes[0].axvline(0.2175, color=COLORS["grey"], lw=0.8, ls=":")
    axes[0].set(xlabel=r"wavelength $\lambda$ [$\mu$m]", ylabel=r"$A_\lambda/A_V$")
    axes[0].set_xlim(0.125, 2.2)
    axes[0].set_ylim(0.0, 7.0)
    axes[0].legend(frameon=False)
    panel_label(axes[0], "a")

    lam_pol = np.linspace(0.25, 1.2, 500)
    for lam_max, color in [(0.45, COLORS["orange"]), (0.55, COLORS["blue"]), (0.65, COLORS["green"])]:
        k = 1.66 * lam_max + 0.01
        p = np.exp(-k * np.log(lam_max / lam_pol) ** 2)
        axes[1].plot(lam_pol, p, color=color, label=fr"$\lambda_{{max}}={lam_max:.2f}$")
    axes[1].set(xlabel=r"wavelength $\lambda$ [$\mu$m]", ylabel=r"$P(\lambda)/P_{\rm max}$")
    axes[1].legend(frameon=False, fontsize=6.8)
    panel_label(axes[1], "b")
    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch14_lensing_time_delay(outdir: Path, filename: str) -> None:
    x = np.linspace(-2.2, 2.2, 180)
    y = np.linspace(-2.2, 2.2, 180)
    xx, yy = np.meshgrid(x, y)
    beta_x, beta_y = 0.35, 0.0
    r = np.sqrt(xx ** 2 + yy ** 2 + 0.05 ** 2)
    phi = 0.5 * ((xx - beta_x) ** 2 + (yy - beta_y) ** 2) - np.log(r)
    fig, axes = plt.subplots(
        1,
        2,
        figsize=(8.05, 2.75),
        gridspec_kw={"width_ratios": [1.05, 1.0], "wspace": 0.78},
    )
    im = axes[0].contourf(xx, yy, phi, levels=24, cmap="viridis")
    axes[0].contour(xx, yy, phi, colors="white", linewidths=0.35, alpha=0.7)
    theta_plus = 0.5 * (beta_x + np.sqrt(beta_x ** 2 + 4.0))
    theta_minus = 0.5 * (beta_x - np.sqrt(beta_x ** 2 + 4.0))
    axes[0].scatter([theta_plus, theta_minus, beta_x], [0.0, 0.0, 0.0], c=[COLORS["orange"], COLORS["orange"], COLORS["black"]], s=[30, 30, 18])
    axes[0].set(xlabel=r"$\theta_x/\theta_E$", ylabel=r"$\theta_y/\theta_E$", aspect="equal")
    cbar = fig.colorbar(im, ax=axes[0], fraction=0.046, pad=0.035)
    cbar.set_label(r"Fermat potential", labelpad=3)
    panel_label(axes[0], "a")

    mass = np.logspace(-6, 12, 700)
    delay = 4.0 * 4.92549095e-6 * mass
    axes[1].loglog(mass, delay, color=COLORS["blue"])
    axes[1].axhline(1e-6, color=COLORS["grey"], lw=0.75, ls=":")
    axes[1].axhline(86400.0, color=COLORS["grey"], lw=0.75, ls=":")
    axes[1].text(1.5e-5, 1.4e-6, r"$1\,\mu$s", fontsize=6.8, color=COLORS["grey"])
    axes[1].text(1e8, 1.2e5, "1 d", fontsize=6.8, color=COLORS["grey"])
    axes[1].set(xlabel=r"lens mass [$M_\odot$]", ylabel=r"$4GM/c^3$ [s]")
    panel_label(axes[1], "b")
    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch14_wave_lensing_interference(outdir: Path, filename: str) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(6.95, 2.55))
    freq = np.linspace(20.0, 1200.0, 1500)
    for delay_ms, color in [(0.8, COLORS["orange"]), (2.0, COLORS["blue"]), (6.0, COLORS["green"])]:
        delay = delay_ms * 1e-3
        amp = 1.0 + 0.34 * np.cos(2.0 * np.pi * freq * delay)
        axes[0].plot(freq, amp, color=color, label=fr"$\Delta t={delay_ms:.1f}$ ms")
    axes[0].set(xlabel="frequency f [Hz]", ylabel=r"relative $|F(f)|^2$")
    axes[0].legend(frameon=False, fontsize=6.8)
    panel_label(axes[0], "a")

    mass = np.logspace(-2, 9, 280)
    fgrid = np.logspace(-4, 3, 260)
    mm, ff = np.meshgrid(mass, fgrid)
    w = 8.0 * np.pi * 4.92549095e-6 * mm * ff
    im = axes[1].pcolormesh(mass, fgrid, np.log10(w), shading="auto", cmap="viridis", vmin=-3, vmax=3)
    cs = axes[1].contour(mass, fgrid, w, levels=[1.0, 100.0], colors="white", linewidths=0.8)
    axes[1].clabel(cs, inline=True, fmt={1.0: "w=1", 100.0: "w=100"}, fontsize=6.6)
    axes[1].set_xscale("log")
    axes[1].set_yscale("log")
    axes[1].set(xlabel=r"lens mass [$M_\odot$]", ylabel="wave frequency [Hz]")
    fig.colorbar(im, ax=axes[1], pad=0.02, label=r"$\log_{10} w$")
    panel_label(axes[1], "b")
    for ax in axes:
        clean_axis(ax)
    save_figure(fig, outdir, filename)


def ch14_cosmic_bell_lightcones(outdir: Path, filename: str) -> None:
    fig, ax = plt.subplots(figsize=(4.1, 3.05))
    ax.set_xlim(-5.2, 5.2)
    ax.set_ylim(-5.2, 1.1)
    ax.fill_between([-5.2, 0.0, 5.2], [-5.2, 0.0, -5.2], -5.2, color=COLORS["light_grey"], alpha=0.65)
    ax.plot([-4.5, 0.0], [-4.5, 0.0], color=COLORS["blue"], lw=1.4)
    ax.plot([4.5, 0.0], [-4.5, 0.0], color=COLORS["orange"], lw=1.4)
    ax.plot([-2.6, -0.85], [-3.2, 0.0], color=COLORS["green"], lw=1.4)
    ax.plot([2.6, 0.85], [-3.2, 0.0], color=COLORS["green"], lw=1.4)
    ax.plot([0.0, -0.85], [-1.15, 0.0], color=COLORS["black"], lw=1.0, ls="--")
    ax.plot([0.0, 0.85], [-1.15, 0.0], color=COLORS["black"], lw=1.0, ls="--")
    ax.scatter([-0.85, 0.85, 0.0, -2.6, 2.6], [0.0, 0.0, -1.15, -3.2, -3.2], s=[34, 34, 26, 30, 30], color=[COLORS["blue"], COLORS["orange"], COLORS["black"], COLORS["green"], COLORS["green"]])
    ax.text(-1.35, 0.18, "Alice", ha="center", fontsize=7.5)
    ax.text(1.35, 0.18, "Bob", ha="center", fontsize=7.5)
    ax.text(
        0.0,
        -1.42,
        "entangled\nsource",
        ha="center",
        va="bottom",
        fontsize=7.2,
        bbox=dict(fc="white", ec="none", alpha=0.78, pad=0.4),
    )
    ax.text(-3.75, -3.0, "setting\nphoton", ha="center", fontsize=7.2, color=COLORS["green"])
    ax.text(3.75, -3.0, "setting\nphoton", ha="center", fontsize=7.2, color=COLORS["green"])
    ax.text(0.0, -4.75, "common-cause region pushed into the past", ha="center", fontsize=7.2, color=COLORS["grey"])
    ax.set(xlabel="space", ylabel=r"$ct$")
    clean_axis(ax, grid=False)
    save_figure(fig, outdir, filename)


def ch15_axion_conversion(outdir: Path, filename: str) -> None:
    ql = np.linspace(0.0, 28.0, 700)
    coherence = np.sinc(ql / (2.0 * np.pi)) ** 2
    length = np.logspace(-2, 2, 500)
    fig, axes = plt.subplots(1, 2, figsize=(6.95, 2.55))
    axes[0].plot(ql, coherence, color=COLORS["blue"])
    axes[0].axvline(np.pi, color=COLORS["grey"], lw=0.8, ls=":")
    axes[0].set(xlabel=r"phase mismatch $qL$", ylabel=r"$\mathrm{sinc}^2(qL/2)$")
    panel_label(axes[0], "a")

    for b_micro, color in [(1, COLORS["blue"]), (10, COLORS["orange"]), (100, COLORS["green"])]:
        probability = 2.3e-4 * (b_micro * length) ** 2
        axes[1].loglog(length, np.clip(probability, 1e-9, 1.0), color=color, label=fr"$B_\perp={b_micro}\,\mu$G")
    axes[1].set(xlabel=r"coherent path $L$ [kpc]", ylabel=r"$P_{a\to\gamma}$ for $g_{11}=1$")
    axes[1].legend(frameon=False, fontsize=6.8)
    panel_label(axes[1], "b")
    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch15_cosmic_birefringence(outdir: Path, filename: str) -> None:
    ell = np.arange(30, 1600)
    ee = 0.07 * (ell / 80.0) ** 0.15 * np.exp(-ell / 1800.0) * (
        1.0 + 0.55 * np.sin(ell / 72.0) ** 2
    )
    bb = 0.003 * (ell / 80.0) ** 0.3 * np.exp(-ell / 900.0)
    fig, axes = plt.subplots(1, 2, figsize=(6.95, 2.55))
    for beta_deg, color in [(0.1, COLORS["green"]), (0.35, COLORS["blue"]), (1.0, COLORS["orange"])]:
        beta = np.radians(beta_deg)
        eb = 0.5 * np.sin(4.0 * beta) * (ee - bb)
        axes[0].plot(ell, eb, color=color, label=fr"$\beta={beta_deg}^\circ$")
    axes[0].set(xlabel=r"multipole $\ell$", ylabel=r"mock $C_\ell^{EB}$")
    axes[0].legend(frameon=False, fontsize=6.8)
    panel_label(axes[0], "a")

    alpha = np.linspace(-0.8, 0.8, 220)
    beta = np.linspace(-0.3, 0.9, 220)
    aa, bbeta = np.meshgrid(alpha, beta)
    chi2 = ((aa + bbeta - 0.29) / 0.06) ** 2 + ((aa + 0.05) / 0.28) ** 2 + ((bbeta - 0.35) / 0.24) ** 2
    im = axes[1].contourf(alpha, beta, np.exp(-0.5 * chi2), levels=24, cmap="viridis")
    axes[1].contour(alpha, beta, chi2, levels=[2.3, 6.17], colors="white", linewidths=0.8)
    axes[1].set(xlabel=r"detector angle error $\alpha$ [deg]", ylabel=r"cosmic angle $\beta$ [deg]")
    fig.colorbar(im, ax=axes[1], pad=0.02, label="relative likelihood")
    panel_label(axes[1], "b")
    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch15_axion_polarization_oscillation(outdir: Path, filename: str) -> None:
    days = np.linspace(0.0, 240.0, 900)
    fig, axes = plt.subplots(1, 2, figsize=(6.95, 2.55))
    for mass, color in [(3e-22, COLORS["green"]), (1e-21, COLORS["blue"]), (1e-20, COLORS["orange"])]:
        period_days = 47.9 * (1e-21 / mass)
        angle = 0.12 * np.cos(2.0 * np.pi * days / period_days)
        axes[0].plot(days, angle, color=color, label=fr"$m_a={mass:.0e}$ eV")
    axes[0].set(xlabel="observing time [d]", ylabel=r"$\Delta\psi$ [deg]")
    axes[0].legend(frameon=False, fontsize=6.6)
    panel_label(axes[0], "a")

    mass = np.logspace(-23, -18, 500)
    period_yr = 0.131 * (1e-21 / mass)
    coherence_yr = period_yr / 1e-6
    axes[1].loglog(mass, period_yr, color=COLORS["blue"], label="period")
    axes[1].loglog(mass, coherence_yr, color=COLORS["orange"], label=r"$t_{\rm coh}$")
    axes[1].set(xlabel=r"axion mass $m_a$ [eV]", ylabel="time scale [yr]")
    axes[1].legend(frameon=False)
    panel_label(axes[1], "b")
    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch15_black_hole_axion_cloud(outdir: Path, filename: str) -> None:
    mass_bh = np.logspace(5, 10.5, 600)
    fig, axes = plt.subplots(1, 2, figsize=(6.95, 2.55))
    for alpha_g, color in [(0.1, COLORS["green"]), (0.4, COLORS["blue"]), (1.0, COLORS["orange"])]:
        ma = 1.336e-10 * alpha_g / mass_bh
        axes[0].loglog(mass_bh, ma, color=color, label=fr"$\alpha_G={alpha_g}$")
    axes[0].scatter([4.3e6, 6.5e9], [1.336e-10 * 0.4 / 4.3e6, 1.336e-10 * 0.4 / 6.5e9], s=24, color=COLORS["black"])
    axes[0].text(5.0e6, 2e-17, "Sgr A*", fontsize=6.7)
    axes[0].text(2.0e9, 1.0e-20, "M87*", fontsize=6.7)
    axes[0].set(xlabel=r"black-hole mass [$M_\odot$]", ylabel=r"matched $m_a$ [eV]")
    axes[0].legend(frameon=False, fontsize=6.8)
    panel_label(axes[0], "a")

    t = np.linspace(0.0, 8.0, 800)
    axes[1].plot(t, 8.0 * np.cos(2.0 * np.pi * t / 3.0), color=COLORS["blue"], label="M87*: days")
    axes_twin = axes[1].twiny()
    t2 = np.linspace(0.0, 1200.0, 800)
    axes_twin.plot(t2, 3.0 * np.cos(2.0 * np.pi * t2 / 420.0), color=COLORS["orange"], label="Sgr A*: seconds")
    axes[1].set(xlabel="M87* observing time [d]", ylabel=r"$\Delta\psi$ [deg]")
    axes_twin.set_xlabel("Sgr A* observing time [s]")
    axes[1].legend(frameon=False, fontsize=6.8, loc="upper right")
    axes_twin.legend(frameon=False, fontsize=6.8, loc="lower right")
    panel_label(axes[1], "b")
    clean_axis(axes_twin)
    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch15_frb_faraday_foreground(outdir: Path, filename: str) -> None:
    c_ghz_m = 0.299792458
    nu = np.linspace(0.7, 8.0, 900)
    lam2 = (c_ghz_m / nu) ** 2
    fig, axes = plt.subplots(1, 2, figsize=(6.95, 2.55))
    for rm, color in [(1e2, COLORS["green"]), (1e4, COLORS["blue"]), (1e5, COLORS["orange"])]:
        psi = np.degrees(np.mod(rm * lam2, np.pi))
        axes[0].plot(nu, psi, color=color, label=fr"RM={rm:.0e}")
    axes[0].set(xlabel=r"frequency $\nu$ [GHz]", ylabel=r"angle modulo $180^\circ$ [deg]")
    axes[0].legend(frameon=False, fontsize=6.8)
    panel_label(axes[0], "a")

    dnu = np.logspace(-2, 1.3, 500)
    nu0 = 1.4
    for rm, color in [(1e3, COLORS["green"]), (1e4, COLORS["blue"]), (1e5, COLORS["orange"])]:
        dlam2 = 2.0 * (c_ghz_m ** 2) * (dnu / 1000.0) / (nu0 ** 3)
        x = rm * dlam2
        depol = np.abs(np.sinc(x / np.pi))
        axes[1].semilogx(dnu, depol, color=color, label=fr"RM={rm:.0e}")
    axes[1].set(xlabel=r"channel width $\Delta\nu$ [MHz] at 1.4 GHz", ylabel="linear-pol. retention")
    axes[1].legend(frameon=False, fontsize=6.8)
    panel_label(axes[1], "b")
    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch15_pulsar_array_correlation(outdir: Path, filename: str) -> None:
    years = np.linspace(0.0, 6.0, 900)
    rng = np.random.default_rng(15)
    fig, axes = plt.subplots(1, 2, figsize=(6.95, 2.55))
    earth = 35.0 * np.sin(2.0 * np.pi * years / 3.2)
    for idx, color in enumerate(PALETTE[:5]):
        phase = rng.uniform(0, 2 * np.pi)
        residual = earth + 18.0 * np.sin(2.0 * np.pi * years / 3.2 + phase)
        axes[0].plot(years, residual + 80 * idx, color=color, lw=1.0)
    axes[0].set(xlabel="time [yr]", ylabel="timing residual + offset [ns]")
    panel_label(axes[0], "a")

    n = 8
    corr = 0.5 * np.ones((n, n))
    np.fill_diagonal(corr, 1.0)
    im = axes[1].imshow(corr, vmin=0, vmax=1, cmap="viridis")
    axes[1].set(xlabel="pulsar index", ylabel="pulsar index")
    fig.colorbar(im, ax=axes[1], pad=0.02, label=r"$\zeta_{\alpha\beta}$")
    panel_label(axes[1], "b")
    for ax in axes:
        clean_axis(ax)
    save_figure(fig, outdir, filename)


def ch15_dark_matter_lensing(outdir: Path, filename: str) -> None:
    mass = np.logspace(4, 10, 500)
    fig, axes = plt.subplots(1, 2, figsize=(6.95, 2.55))
    g_const = 6.6743e-11
    c_si = 299792458.0
    msun = 1.98847e30
    gpc = 3.085677581e25
    dl, ds, dls = 1.0 * gpc, 2.0 * gpc, 1.0 * gpc
    theta_e = np.sqrt(4.0 * g_const * mass * msun / c_si ** 2 * dls / (dl * ds))
    theta_mas = theta_e * 180.0 / np.pi * 3600.0 * 1000.0
    axes[0].loglog(mass, theta_mas, color=COLORS["blue"])
    axes[0].set(xlabel=r"subhalo mass [$M_\odot$]", ylabel=r"$\theta_E$ [mas]")
    panel_label(axes[0], "a")

    impact = np.logspace(-1, 2.0, 500)
    for m, color in [(1e6, COLORS["green"]), (1e8, COLORS["blue"]), (1e10, COLORS["orange"])]:
        th = np.interp(m, mass, theta_mas)
        shift_uas = 1000.0 * th ** 2 / impact
        axes[1].loglog(impact, shift_uas, color=color, label=fr"$M={m:.0e}M_\odot$")
    axes[1].set(xlabel="impact angle [mas]", ylabel=r"astrometric shift [$\mu$as]")
    axes[1].legend(frameon=False, fontsize=6.8)
    panel_label(axes[1], "b")
    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch16_cmb_blackbody(outdir: Path, filename: str) -> None:
    nu_ghz = np.logspace(0, 3.1, 600)
    nu = nu_ghz * 1e9
    h = 6.62607015e-34
    k_b = 1.380649e-23
    c_si = 299792458.0
    t_cmb = 2.7255
    x = h * nu / (k_b * t_cmb)
    n_nu = 1.0 / np.expm1(x)
    intensity_mjy_sr = 2.0 * h * nu ** 3 / c_si ** 2 * n_nu / 1e-20

    fig, axes = plt.subplots(1, 2, figsize=(6.9, 2.55))
    axes[0].semilogx(nu_ghz, intensity_mjy_sr, color=COLORS["blue"])
    axes[0].axvline(160.2, color=COLORS["grey"], lw=0.8, ls="--")
    axes[0].text(166, 365, "near peak", fontsize=7.2, color=COLORS["grey"])
    axes[0].set(xlabel=r"frequency $\nu$ [GHz]", ylabel=r"$I_\nu$ [MJy sr$^{-1}$]")
    panel_label(axes[0], "a")

    axes[1].loglog(nu_ghz, n_nu, color=COLORS["orange"])
    for freq in [30, 150, 353]:
        occ = 1.0 / np.expm1(h * freq * 1e9 / (k_b * t_cmb))
        axes[1].scatter([freq], [occ], s=20, color=COLORS["black"], zorder=3)
        axes[1].text(freq * 1.08, occ * 1.12, f"{freq} GHz", fontsize=6.8)
    axes[1].set(xlabel=r"frequency $\nu$ [GHz]", ylabel=r"occupation $n_\nu$")
    panel_label(axes[1], "b")
    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch16_cmb_power_spectrum(outdir: Path, filename: str) -> None:
    ell = np.arange(2, 2500)
    damping = np.exp(-(ell / 1850.0) ** 1.25)
    peaks = (
        5300 * np.exp(-0.5 * ((ell - 220) / 72) ** 2)
        + 2550 * np.exp(-0.5 * ((ell - 540) / 88) ** 2)
        + 2450 * np.exp(-0.5 * ((ell - 810) / 115) ** 2)
        + 1250 * np.exp(-0.5 * ((ell - 1120) / 145) ** 2)
    )
    plateau = 750 * (ell / 80.0) ** 0.18 * np.exp(-ell / 3600.0)
    dl = (plateau + peaks) * damping
    cv_frac = np.sqrt(2.0 / (2.0 * ell + 1.0))

    fig, axes = plt.subplots(1, 2, figsize=(6.95, 2.55))
    axes[0].plot(ell, dl, color=COLORS["blue"])
    axes[0].fill_between(
        ell,
        dl * (1.0 - cv_frac),
        dl * (1.0 + cv_frac),
        color=COLORS["sky"],
        alpha=0.22,
        lw=0,
        label="cosmic variance",
    )
    axes[0].set(xlabel=r"multipole $\ell$", ylabel=r"$D_\ell^{TT}$ [$\mu$K$^2$]")
    axes[0].set_xlim(2, 2400)
    axes[0].legend(frameon=False, loc="upper right")
    panel_label(axes[0], "a")

    axes[1].loglog(ell, cv_frac, color=COLORS["purple"])
    axes[1].axhline(0.01, color=COLORS["grey"], lw=0.8, ls="--")
    axes[1].text(8, 0.012, "1%", fontsize=7.2, color=COLORS["grey"])
    axes[1].set(xlabel=r"multipole $\ell$", ylabel=r"$\Delta C_\ell/C_\ell$")
    axes[1].set_ylim(5e-3, 0.8)
    panel_label(axes[1], "b")
    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch16_squeezed_modes(outdir: Path, filename: str) -> None:
    n_efolds = np.linspace(-5, 8, 500)
    k_over_ah = np.exp(-n_efolds)
    squeezing = np.maximum(n_efolds, 0.0)

    fig, axes = plt.subplots(1, 2, figsize=(6.9, 2.55))
    axes[0].semilogy(n_efolds, k_over_ah, color=COLORS["blue"], label=r"$k/(aH)$")
    axes[0].plot(n_efolds, np.exp(-squeezing), color=COLORS["orange"], label=r"decaying quadrature")
    axes[0].axvline(0, color=COLORS["grey"], lw=0.8, ls="--")
    axes[0].text(0.18, 7e1, "horizon exit", fontsize=7.2, color=COLORS["grey"])
    axes[0].set(xlabel="e-folds after horizon exit", ylabel="relative scale")
    axes[0].legend(frameon=False)
    panel_label(axes[0], "a")

    theta = np.linspace(0, 2 * np.pi, 300)
    for r, color in [(0.0, COLORS["grey"]), (1.7, COLORS["green"]), (3.2, COLORS["purple"])]:
        q = np.exp(r) * np.cos(theta)
        p = np.exp(-r) * np.sin(theta)
        axes[1].plot(q, p, color=color, label=fr"$r_k={r:.1f}$")
    axes[1].set(xlabel=r"field quadrature $q_k$", ylabel=r"momentum quadrature $p_k$")
    axes[1].set_xlim(-28, 28)
    axes[1].set_ylim(-1.35, 1.35)
    axes[1].legend(frameon=False, loc="upper right")
    panel_label(axes[1], "b")
    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch16_non_gaussian_templates(outdir: Path, filename: str) -> None:
    x = np.linspace(0.06, 1.95, 600)
    local = 1.0 / (x ** 2 + 0.015)
    local /= local.max()
    equilateral = np.exp(-0.5 * (np.log(x) / 0.28) ** 2)
    orthogonal = equilateral * (1.0 - 2.3 * (x - 1.0) ** 2)
    orthogonal /= np.max(np.abs(orthogonal))

    fig, axes = plt.subplots(1, 2, figsize=(6.95, 2.55))
    axes[0].plot(x, local, color=COLORS["blue"], label="local")
    axes[0].plot(x, equilateral, color=COLORS["orange"], label="equilateral")
    axes[0].plot(x, orthogonal, color=COLORS["green"], label="orthogonal")
    axes[0].axvline(1, color=COLORS["grey"], lw=0.8, ls="--")
    axes[0].set(xlabel=r"triangle ratio $k_3/k_1$ with $k_1=k_2$", ylabel="normalized shape")
    axes[0].legend(frameon=False)
    panel_label(axes[0], "a")

    labels = ["local", "equil.", "orth."]
    vals = np.array([-0.9, -26.0, -38.0])
    errs = np.array([5.1, 47.0, 24.0])
    y = np.arange(len(labels))
    axes[1].errorbar(vals, y, xerr=errs, fmt="o", color=COLORS["black"], capsize=3)
    axes[1].axvline(0, color=COLORS["grey"], lw=0.8, ls="--")
    axes[1].set_yticks(y, labels)
    axes[1].set(xlabel=r"Planck 2018 $f_{\rm NL}$")
    axes[1].set_xlim(-95, 55)
    panel_label(axes[1], "b")
    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch16_bmode_constraints(outdir: Path, filename: str) -> None:
    ell = np.arange(2, 320)
    lens = 0.0015 * (ell / 80.0) ** 2.1 * np.exp(-(ell / 520.0) ** 1.15)

    def tensor_bb(r: float) -> np.ndarray:
        recomb = 0.85 * r * np.exp(-0.5 * ((ell - 82) / 34.0) ** 2)
        reion = 0.13 * r * np.exp(-0.5 * ((ell - 6) / 4.5) ** 2)
        return recomb + reion

    fig, axes = plt.subplots(1, 2, figsize=(6.95, 2.55))
    axes[0].loglog(ell, lens, color=COLORS["grey"], lw=1.3, label="lensing")
    for r, color in [(0.036, COLORS["orange"]), (0.01, COLORS["blue"]), (0.001, COLORS["green"])]:
        axes[0].loglog(ell, tensor_bb(r), color=color, label=fr"tensor $r={r:g}$")
    axes[0].set(xlabel=r"multipole $\ell$", ylabel=r"$D_\ell^{BB}$ [$\mu$K$^2$]")
    axes[0].set_ylim(1e-5, 8e-2)
    axes[0].legend(frameon=False, fontsize=6.6)
    panel_label(axes[0], "a")

    years = np.array([2014, 2016, 2018, 2021])
    limits = np.array([0.12, 0.09, 0.07, 0.036])
    axes[1].plot(years, limits, marker="o", color=COLORS["purple"])
    axes[1].fill_between(years, limits, 0.14, color=COLORS["purple"], alpha=0.12)
    axes[1].set(xlabel="BICEP/Keck publication year", ylabel=r"95% upper limit on $r$")
    axes[1].set_ylim(0, 0.14)
    axes[1].set_xticks(years)
    panel_label(axes[1], "b")
    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch16_birefringence_eb(outdir: Path, filename: str) -> None:
    beta = np.linspace(-1.0, 1.0, 500)
    leakage = 0.5 * np.sin(4.0 * np.radians(beta))
    induced_bb = np.sin(2.0 * np.radians(beta)) ** 2

    fig, axes = plt.subplots(1, 2, figsize=(6.95, 2.55))
    axes[0].plot(beta, leakage, color=COLORS["blue"], label=r"$EB/(EE-BB)$")
    axes[0].plot(beta, induced_bb, color=COLORS["orange"], label=r"induced $BB/EE$")
    axes[0].axvspan(0.35 - 0.14, 0.35 + 0.14, color=COLORS["sky"], alpha=0.25, lw=0)
    axes[0].set(xlabel=r"rotation $\beta$ [deg]", ylabel="relative leakage")
    axes[0].legend(frameon=False)
    panel_label(axes[0], "a")

    a = np.linspace(-0.8, 0.8, 220)
    b = np.linspace(-0.2, 0.9, 220)
    aa, bb = np.meshgrid(a, b)
    cmb_only = ((aa + bb - 0.35) / 0.12) ** 2
    foreground = ((aa + 0.02) / 0.22) ** 2 + ((bb - 0.35) / 0.14) ** 2
    chi2 = cmb_only + foreground
    axes[1].contour(aa, bb, chi2, levels=[2.3, 6.17], colors=[COLORS["black"], COLORS["grey"]], linewidths=[1.2, 0.9])
    axes[1].plot(a, 0.35 - a, color=COLORS["purple"], lw=1.0, ls="--", label=r"CMB: $\alpha+\beta$")
    axes[1].set(xlabel=r"detector angle $\alpha$ [deg]", ylabel=r"cosmic angle $\beta$ [deg]")
    axes[1].legend(frameon=False, loc="lower left")
    panel_label(axes[1], "b")
    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch17_architecture_loss(outdir: Path, filename: str) -> None:
    distance = np.linspace(0, 50, 500)
    fig, axes = plt.subplots(1, 2, figsize=(6.95, 2.55))
    for loss_db, label, color in [
        (25.0, "visible fiber 25 dB/km", COLORS["orange"]),
        (0.2, "telecom fiber 0.2 dB/km", COLORS["blue"]),
        (0.5, "clear free-space 0.5 dB/km", COLORS["green"]),
    ]:
        transmission = 10 ** (-loss_db * distance / 10.0)
        axes[0].semilogy(distance, transmission, color=color, label=label)
    axes[0].axhline(1e-6, color=COLORS["grey"], lw=0.8, ls="--")
    axes[0].set(xlabel="physical signal transport [km]", ylabel="single-photon transmission")
    axes[0].legend(frameon=False, fontsize=6.5)
    panel_label(axes[0], "a")

    baseline = np.logspace(0, 6, 500)
    wavelength = 600e-9
    theta_uas = 206265e6 * wavelength / baseline
    axes[1].loglog(baseline / 1000.0, theta_uas, color=COLORS["purple"])
    axes[1].axhline(100, color=COLORS["grey"], lw=0.8, ls="--")
    axes[1].axhline(10, color=COLORS["grey"], lw=0.8, ls=":")
    axes[1].set(xlabel="baseline [km]", ylabel=r"$\lambda/B$ [$\mu$as] at 600 nm")
    panel_label(axes[1], "b")
    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch17_entanglement_resources(outdir: Path, filename: str) -> None:
    r_gamma = np.logspace(0, 8, 500)
    baseline = np.logspace(1, 7, 500)
    c = 299792458.0
    fig, axes = plt.subplots(1, 2, figsize=(6.95, 2.55))
    for pairs, color in [(1, COLORS["blue"]), (5, COLORS["green"]), (20, COLORS["orange"])]:
        axes[0].loglog(r_gamma, pairs * r_gamma, color=color, label=fr"{pairs} Bell pairs/event")
    axes[0].axhline(1e3, color=COLORS["grey"], lw=0.8, ls="--", label="1 kHz")
    axes[0].set(xlabel=r"accepted stellar events $R_\star$ [s$^{-1}$]", ylabel=r"required $R_{\rm ent}$ [s$^{-1}$]")
    axes[0].legend(frameon=False, fontsize=6.5)
    panel_label(axes[0], "a")

    axes[1].loglog(baseline / 1000.0, baseline / c, color=COLORS["purple"], label=r"$B/c$")
    axes[1].axhline(1e-3, color=COLORS["grey"], lw=0.8, ls="--", label="1 ms")
    axes[1].axhline(1.0, color=COLORS["grey"], lw=0.8, ls=":", label="1 s")
    axes[1].set(xlabel="baseline [km]", ylabel=r"minimum storage time [s]")
    axes[1].legend(frameon=False, fontsize=6.5)
    panel_label(axes[1], "b")
    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch17_timebin_scaling(outdir: Path, filename: str) -> None:
    eps = np.logspace(-7, -1, 500)
    n_bins = 1.0 / eps
    fig, axes = plt.subplots(1, 2, figsize=(6.95, 2.55))
    axes[0].loglog(eps, n_bins, color=COLORS["orange"], label="unary: one pair/bin")
    axes[0].loglog(eps, np.log2(n_bins + 1.0), color=COLORS["blue"], label=r"binary: $\log_2(N+1)$")
    axes[0].invert_xaxis()
    axes[0].set(xlabel=r"mean photon number per bin $\epsilon$", ylabel="Bell pairs per window")
    axes[0].legend(frameon=False, fontsize=6.5)
    panel_label(axes[0], "a")

    bandwidth = np.logspace(3, 9, 500)
    t_window = 1.0
    bins = bandwidth * t_window
    axes[1].semilogx(bandwidth, np.log2(bins + 1.0), color=COLORS["green"])
    axes[1].axhline(20, color=COLORS["grey"], lw=0.8, ls="--")
    axes[1].text(1.6e3, 20.8, "20 memory qubits", fontsize=7.0, color=COLORS["grey"])
    axes[1].set(xlabel=r"signal bandwidth $\Delta f$ [Hz] for 1 s window", ylabel=r"$\log_2(\Delta f T+1)$")
    panel_label(axes[1], "b")
    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch17_fidelity_distance(outdir: Path, filename: str) -> None:
    distance = np.linspace(0, 100, 500)
    t_storage = np.linspace(0, 5, 500)
    fig, axes = plt.subplots(1, 2, figsize=(6.95, 2.55))
    for loss_db, color in [(0.2, COLORS["blue"]), (0.5, COLORS["green"]), (3.0, COLORS["orange"])]:
        eta = 10 ** (-loss_db * distance / 10.0)
        axes[0].semilogy(distance, eta, color=color, label=fr"{loss_db:g} dB/km")
    axes[0].set(xlabel="entanglement distribution distance [km]", ylabel=r"channel factor $\eta$")
    axes[0].legend(frameon=False, fontsize=6.5)
    panel_label(axes[0], "a")

    for t2, color in [(0.01, COLORS["orange"]), (1.0, COLORS["blue"]), (10.0, COLORS["green"])]:
        axes[1].semilogy(t_storage, np.exp(-t_storage / t2), color=color, label=fr"$T_2={t2:g}$ s")
    axes[1].set(xlabel="stored time [s]", ylabel=r"memory coherence factor $e^{-T/T_2}$")
    axes[1].legend(frameon=False, fontsize=6.5)
    panel_label(axes[1], "b")
    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch17_fisher_visibility(outdir: Path, filename: str) -> None:
    p_succ = np.logspace(-6, 0, 500)
    fig, axes = plt.subplots(1, 2, figsize=(6.95, 2.55))
    for visibility, color in [(0.03, COLORS["grey"]), (0.09, COLORS["blue"]), (0.36, COLORS["orange"])]:
        axes[0].loglog(p_succ, p_succ * visibility ** 2, color=color, label=fr"$V={visibility:g}$")
    axes[0].set(xlabel=r"herald probability $p_{\rm succ}$", ylabel=r"FI per trial $\propto p_{\rm succ}V^2$")
    axes[0].legend(frameon=False, fontsize=6.5)
    panel_label(axes[0], "a")

    n_trials = np.logspace(2, 9, 500)
    for p, v, color in [(1e-3, 0.09, COLORS["blue"]), (1e-4, 0.36, COLORS["orange"]), (1e-2, 0.03, COLORS["grey"])]:
        sigma = 1.0 / np.sqrt(n_trials * p * v ** 2)
        axes[1].loglog(n_trials, sigma, color=color, label=fr"$p={p:g}, V={v:g}$")
    axes[1].set(xlabel="number of protocol trials", ylabel=r"$\sigma_\phi$ [rad]")
    axes[1].legend(frameon=False, fontsize=6.5)
    panel_label(axes[1], "b")
    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch17_network_parameter_space(outdir: Path, filename: str) -> None:
    rate = np.logspace(0, 7, 190)
    memory = np.logspace(-6, 1, 180)
    rr, mm = np.meshgrid(rate, memory)
    baseline_km = np.array([1, 100, 1e4])
    c_km_s = 299792.458
    score = np.log10(rr) + np.log10(mm) - 0.7
    fig, ax = plt.subplots(figsize=(3.7, 2.9))
    im = ax.contourf(rate, memory, score, levels=22, cmap="viridis")
    for b, style in zip(baseline_km, ["-", "--", ":"]):
        ax.axhline(b / c_km_s, color="white", lw=1.0, ls=style)
        ax.text(1.25, b / c_km_s * 1.08, fr"{b:g} km", color="white", fontsize=6.7)
    ax.scatter([13, 1.9, 1e3], [0.01, 0.01, 1.0], s=26, c=[COLORS["orange"], COLORS["purple"], COLORS["blue"]], edgecolor="white", linewidth=0.4)
    ax.set(xscale="log", yscale="log", xlabel=r"$R_{\rm ent}$ [s$^{-1}$]", ylabel=r"$T_{\rm mem}$ [s]")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03, label=r"$\log_{10}(R_{\rm ent}T_{\rm mem})$")
    clean_axis(ax)
    save_figure(fig, outdir, filename)


def ch18_photon_rate_magnitude(outdir: Path, filename: str) -> None:
    mag = np.linspace(-1, 12, 500)
    lam = 550e-9
    dlam = 10e-9
    c = 299792458.0
    h = 6.62607015e-34
    fnu0 = 3631e-26
    dnu = c * dlam / lam ** 2
    eta = 0.25
    fig, ax = plt.subplots(figsize=(3.65, 2.55))
    for diameter, color in [(1.0, COLORS["grey"]), (4.0, COLORS["green"]), (12.0, COLORS["blue"]), (17.0, COLORS["orange"])]:
        area = np.pi * (diameter / 2.0) ** 2
        fnu = fnu0 * 10 ** (-0.4 * mag)
        rate = area * eta * fnu * dnu / (h * c / lam)
        ax.semilogy(mag, rate, color=color, label=fr"$D={diameter:g}$ m")
    ax.axhspan(1e8, 1e10, color=COLORS["light_grey"], alpha=0.75, lw=0)
    ax.text(7.1, 2.2e8, "fast-detector pressure", fontsize=7.0, color=COLORS["grey"])
    ax.set(xlabel=r"$m_{\rm AB}$ at 550 nm", ylabel=r"$R_\gamma$ in 10 nm [s$^{-1}$]")
    ax.legend(frameon=False, ncol=2)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch18_coherence_dilution(outdir: Path, filename: str) -> None:
    dlam_nm = np.logspace(-1, 2, 500)
    lam = 416e-9
    c = 299792458.0
    tau_c = lam ** 2 / (c * dlam_nm * 1e-9)
    fig, ax = plt.subplots(figsize=(3.65, 2.55))
    for dt_ns, color in [(0.1, COLORS["green"]), (1.0, COLORS["blue"]), (4.0, COLORS["orange"])]:
        contrast = 0.5 * tau_c / (dt_ns * 1e-9)
        ax.loglog(dlam_nm, contrast, color=color, label=fr"$\Delta t={dt_ns:g}$ ns")
    ax.axvline(13.0, color=COLORS["grey"], lw=0.8, ls="--")
    ax.text(13.8, 1.1e-6, "VERITAS-like\nbandpass", fontsize=6.9, color=COLORS["grey"])
    ax.set(xlabel=r"optical bandpass $\Delta\lambda$ [nm]", ylabel=r"zero-baseline contrast $\simeq\tau_c/(2\Delta t)$")
    ax.legend(frameon=False)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch18_snr_heatmap(outdir: Path, filename: str) -> None:
    mag = np.linspace(1.5, 9.0, 170)
    tint_h = np.logspace(-1, 1.4, 150)
    mm, tt = np.meshgrid(mag, tint_h)
    area = 100.0
    alpha = 0.30
    delta_f = 1.0e9
    visibility2 = 0.5
    n = 5.0e-5 * 10 ** (-0.4 * mm)
    snr = area * alpha * n * visibility2 * np.sqrt(delta_f * tt * 3600.0 / 2.0)
    fig, ax = plt.subplots(figsize=(3.75, 2.9))
    levels = np.linspace(0, 12, 25)
    im = ax.contourf(mag, tint_h, snr, levels=levels, cmap="viridis", extend="max")
    cs = ax.contour(mag, tint_h, snr, levels=[3, 5, 10], colors="white", linewidths=0.65)
    ax.clabel(cs, fmt="%g", fontsize=6.5)
    ax.scatter([6.7], [5.0], s=26, color=COLORS["orange"], edgecolor="white", linewidth=0.45, zorder=3)
    ax.text(6.77, 5.2, r"$m_V\simeq6.7,\ 5$ h", fontsize=6.8, color="white")
    ax.set(yscale="log", xlabel=r"visual magnitude $m_V$", ylabel="integration time [h]")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03, label="SNR")
    clean_axis(ax)
    save_figure(fig, outdir, filename)


def ch18_visibility_fisher(outdir: Path, filename: str) -> None:
    baseline = np.linspace(5, 650, 700)
    lam = 416e-9
    mas_to_rad = np.pi / (180.0 * 3600.0 * 1000.0)
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.6))
    theta_mas_values = [0.5, 1.0, 2.0]
    for theta_mas, color in zip(theta_mas_values, [COLORS["blue"], COLORS["orange"], COLORS["green"]]):
        x = np.pi * (theta_mas * mas_to_rad) * baseline / lam
        v2 = disk_visibility(x) ** 2
        axes[0].plot(baseline, v2, color=color, label=fr"$\theta={theta_mas:g}$ mas")
        dtheta = 0.002 * theta_mas * mas_to_rad
        x_plus = np.pi * (theta_mas * mas_to_rad + dtheta) * baseline / lam
        x_minus = np.pi * (theta_mas * mas_to_rad - dtheta) * baseline / lam
        deriv = (disk_visibility(x_plus) ** 2 - disk_visibility(x_minus) ** 2) / (2.0 * dtheta)
        fisher = deriv ** 2 / np.maximum(v2 * (1.0 - v2) + 0.02, 0.02)
        fisher = fisher / fisher.max()
        axes[1].plot(baseline, fisher, color=color)
    axes[0].set(xlabel="baseline [m]", ylabel=r"$|V|^2$")
    axes[1].set(xlabel="baseline [m]", ylabel="relative diameter information")
    axes[0].legend(frameon=False)
    for ax, label in zip(axes, ["a", "b"]):
        panel_label(ax, label)
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch18_uv_coverage(outdir: Path, filename: str) -> None:
    rng = np.random.default_rng(18)
    veritas = np.array([[0, 0], [80, -35], [135, 60], [40, 150]], dtype=float)
    r = 2000.0 * np.sqrt(rng.uniform(size=60))
    phi = rng.uniform(0, 2.0 * np.pi, size=60)
    cta = np.column_stack([r * np.cos(phi), r * np.sin(phi)])

    def uv_points(pos: np.ndarray, n_angles: int) -> np.ndarray:
        pairs = []
        for i in range(len(pos)):
            for j in range(i + 1, len(pos)):
                pairs.append(pos[j] - pos[i])
        pairs = np.asarray(pairs)
        angles = np.linspace(-0.8, 0.8, n_angles)
        pts = []
        for a in angles:
            ca = np.cos(a)
            sa = np.sin(a)
            p = np.column_stack([pairs[:, 0] * ca - pairs[:, 1] * sa, pairs[:, 0] * sa + pairs[:, 1] * ca])
            pts.append(p)
            pts.append(-p)
        return np.vstack(pts)

    fig, axes = plt.subplots(1, 2, figsize=(7.1, 2.85))
    for ax, pts, title, lim, color in [
        (axes[0], uv_points(veritas, 18), "4 telescopes / 6 baselines", 230, COLORS["blue"]),
        (axes[1], uv_points(cta, 8), "60 telescopes / 1770 baselines", 4300, COLORS["orange"]),
    ]:
        ax.scatter(pts[:, 0], pts[:, 1], s=5, color=color, alpha=0.38, linewidths=0)
        ax.axhline(0, color=COLORS["light_grey"], lw=0.7)
        ax.axvline(0, color=COLORS["light_grey"], lw=0.7)
        ax.set(xlabel=r"$u$ [m]", ylabel=r"$v$ [m]", title=title, xlim=(-lim, lim), ylim=(-lim, lim), aspect="equal")
        clean_axis(ax)
    panel_label(axes[0], "a")
    panel_label(axes[1], "b")
    save_figure(fig, outdir, filename)


def ch18_background_dilution(outdir: Path, filename: str) -> None:
    beta = np.linspace(0, 2.0, 500)
    dilution_equal = 1.0 / (1.0 + beta) ** 2
    correction_equal = (1.0 + beta) ** 2
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.55))
    axes[0].plot(beta, dilution_equal, color=COLORS["blue"])
    axes[0].axvline(0.03, color=COLORS["grey"], lw=0.8, ls="--")
    axes[0].axvline(0.5, color=COLORS["orange"], lw=0.8, ls="--")
    axes[0].text(0.05, 0.86, "3% off-source", fontsize=6.8, color=COLORS["grey"])
    axes[0].text(0.53, 0.34, "bright background", fontsize=6.8, color=COLORS["orange"])
    axes[0].set(xlabel=r"background/star ratio $\beta$", ylabel="measured contrast factor")
    axes[1].plot(beta, correction_equal, color=COLORS["green"])
    axes[1].set(xlabel=r"background/star ratio $\beta$", ylabel="multiplicative correction")
    for ax, label in zip(axes, ["a", "b"]):
        panel_label(ax, label)
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch18_error_budget(outdir: Path, filename: str) -> None:
    time_h = np.logspace(-1, 2, 360)
    stat = 0.12 / np.sqrt(time_h)
    background = np.full_like(time_h, 0.018)
    timing = np.full_like(time_h, 0.012)
    calibration = np.full_like(time_h, 0.025)
    model = np.full_like(time_h, 0.020)
    total = np.sqrt(stat ** 2 + background ** 2 + timing ** 2 + calibration ** 2 + model ** 2)
    fig, axes = plt.subplots(1, 2, figsize=(7.15, 2.65))
    for y, label, color in [
        (stat, "statistical", COLORS["blue"]),
        (background, "background", COLORS["orange"]),
        (timing, "timing", COLORS["green"]),
        (calibration, "calibration", COLORS["purple"]),
        (model, "model", COLORS["grey"]),
    ]:
        axes[0].loglog(time_h, y * 100.0, color=color, label=label)
    axes[0].loglog(time_h, total * 100.0, color=COLORS["black"], lw=2.0, label="quadrature total")
    axes[0].set(xlabel="integration time [h]", ylabel=r"fractional error in $|V|^2$ [%]")
    axes[0].legend(frameon=False, fontsize=6.2, ncol=2)

    labels = ["stat", "sky", "timing", "cal", "model"]
    vals = np.array([stat[np.argmin(np.abs(time_h - 10))], 0.018, 0.012, 0.025, 0.020])
    axes[1].bar(labels, vals ** 2 / np.sum(vals ** 2) * 100.0, color=PALETTE[:5])
    axes[1].set(ylabel="variance share at 10 h [%]")
    axes[1].tick_params(axis="x", rotation=20)
    for ax, label in zip(axes, ["a", "b"]):
        panel_label(ax, label)
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch19_science_case_feasibility(outdir: Path, filename: str) -> None:
    cases = [
        ("stellar diameters", 2.0, 1.0, COLORS["blue"]),
        (r"$\beta$ UMa", 2.4, 1.07, COLORS["green"]),
        (r"$\gamma$ Cas", 2.5, 0.43, COLORS["orange"]),
        ("Be/WR lines", 4.0, 0.30, COLORS["purple"]),
        ("Cepheids", 5.5, 1.2, COLORS["sky"]),
        ("nova shells", 7.0, 0.4, COLORS["yellow"]),
        ("SN Ia", 12.0, 0.03, COLORS["grey"]),
        ("AGN BLR", 13.5, 0.003, COLORS["black"]),
    ]
    fig, ax = plt.subplots(figsize=(4.0, 3.0))
    ax.axvspan(-0.5, 5.5, color=COLORS["light_grey"], alpha=0.45, lw=0)
    ax.text(0.2, 0.006, "near-term brightness", fontsize=7.0, color=COLORS["grey"])
    ax.axhspan(0.1, 3.0, color=COLORS["blue"], alpha=0.06, lw=0)
    ax.axhline(0.1, color=COLORS["grey"], ls="--", lw=0.8)
    label_pos = {
        "stellar diameters": (1.62, 1.25, "left"),
        r"$\beta$ UMa": (2.90, 1.34, "right"),
        r"$\gamma$ Cas": (2.35, 0.58, "left"),
        "Be/WR lines": (4.25, 0.27, "left"),
        "Cepheids": (6.35, 0.98, "left"),
        "nova shells": (7.15, 0.52, "left"),
        "SN Ia": (12.28, 0.035, "left"),
        "AGN BLR": (13.78, 0.0036, "left"),
    }
    for name, mag, theta, color in cases:
        ax.scatter(mag, theta, s=56, color=color, edgecolor="white", linewidth=0.4, zorder=3)
        x_text, y_text, ha = label_pos[name]
        ax.text(
            x_text,
            y_text,
            name,
            fontsize=6.8,
            ha=ha,
            va="center",
            bbox=dict(fc="white", ec="none", alpha=0.65, pad=0.18),
        )
    ax.set(yscale="log", xlabel="typical apparent magnitude", ylabel="angular scale [mas]", xlim=(-0.5, 15), ylim=(1e-3, 4))
    ax.invert_xaxis()
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch19_binary_visibility(outdir: Path, filename: str) -> None:
    baseline = np.linspace(0, 360, 900)
    lam = 416e-9
    mas_to_rad = np.pi / (180.0 * 3600.0 * 1000.0)
    sep = 1.0 * mas_to_rad
    fig, ax = plt.subplots(figsize=(3.75, 2.65))
    for ratio, color in [(1.0, COLORS["blue"]), (0.3, COLORS["orange"]), (0.1, COLORS["green"])]:
        phase = 2.0 * np.pi * baseline * sep / lam
        vis2 = (1.0 + ratio ** 2 + 2.0 * ratio * np.cos(phase)) / (1.0 + ratio) ** 2
        ax.plot(baseline, vis2, color=color, label=fr"$f={ratio:g}$")
    ax.set(xlabel="projected baseline [m]", ylabel=r"$|V_{\rm binary}|^2$")
    ax.legend(frameon=False, title="flux ratio")
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch19_transient_expansion(outdir: Path, filename: str) -> None:
    day = np.logspace(-1, 2.0, 400)
    rad_to_mas = 180.0 / np.pi * 3600.0 * 1000.0
    pc = 3.085677581e16
    cases = [
        ("nova: 1000 km/s, 2 kpc", 1.0e6, 2.0e3 * pc, COLORS["blue"]),
        ("SN Ia: 10000 km/s, 10 Mpc", 1.0e7, 10.0e6 * pc, COLORS["orange"]),
        ("SN Ia: 10000 km/s, 20 Mpc", 1.0e7, 20.0e6 * pc, COLORS["green"]),
    ]
    fig, axes = plt.subplots(1, 2, figsize=(7.1, 2.65))
    for label, v, dist, color in cases:
        theta = 2.0 * v * day * 86400.0 / dist * rad_to_mas
        axes[0].loglog(day, theta, color=color, label=label)
        baseline = 416e-9 / (theta / rad_to_mas)
        axes[1].loglog(day, baseline / 1000.0, color=color)
    axes[0].set(xlabel="days after explosion", ylabel="angular diameter [mas]")
    axes[1].set(xlabel="days after explosion", ylabel=r"$B\simeq\lambda/\theta$ [km]")
    axes[0].legend(frameon=False, fontsize=6.2)
    for ax, label in zip(axes, ["a", "b"]):
        panel_label(ax, label)
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch19_natural_laser_statistics(outdir: Path, filename: str) -> None:
    modes = np.logspace(0, 5, 500)
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.55))
    axes[0].loglog(modes, 1.0 / modes, color=COLORS["blue"], label="thermal modes")
    axes[0].axhline(0.0 + 1e-5, color=COLORS["black"], lw=0.9, ls="--", label="coherent limit")
    axes[0].set(xlabel="effective mode number M", ylabel=r"$g^{(2)}(0)-1$")
    axes[0].legend(frameon=False)

    width = np.logspace(3, 10, 500)
    tau_c = 1.0 / (np.pi * width)
    for dt, color in [(0.1e-9, COLORS["green"]), (1e-9, COLORS["orange"]), (10e-9, COLORS["purple"])]:
        axes[1].loglog(width, np.minimum(1.0, tau_c / dt), color=color, label=fr"$\Delta t={dt*1e9:g}$ ns")
    axes[1].set(xlabel="line width [Hz]", ylabel="resolvable contrast scale")
    axes[1].legend(frameon=False)
    for ax, label in zip(axes, ["a", "b"]):
        panel_label(ax, label)
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch19_crab_phase_windows(outdir: Path, filename: str) -> None:
    phase = np.linspace(0, 1, 900)
    profile = 0.11
    profile += 1.0 * np.exp(-0.5 * ((phase - 0.03) / 0.018) ** 2)
    profile += 0.42 * np.exp(-0.5 * ((phase - 0.40) / 0.035) ** 2)
    profile += 0.16 * np.exp(-0.5 * ((phase - 0.22) / 0.08) ** 2)
    profile /= profile.max()
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.55))
    axes[0].plot(phase, profile, color=COLORS["purple"])
    axes[0].fill_between(phase, 0, profile, where=(phase < 0.08), color=COLORS["purple"], alpha=0.20, label="main pulse")
    axes[0].fill_between(phase, 0, profile, where=((phase > 0.34) & (phase < 0.48)), color=COLORS["orange"], alpha=0.20, label="interpulse")
    axes[0].set(xlabel=r"rotational phase $\phi$", ylabel="normalized optical counts")
    axes[0].legend(frameon=False)
    dt = np.logspace(-9, -3, 400)
    for period, label, color in [(0.033, "Crab", COLORS["blue"]), (0.005, "millisecond pulsar", COLORS["orange"]), (2.0, "magnetar", COLORS["green"])]:
        axes[1].loglog(dt * 1e6, dt / period, color=color, label=label)
    axes[1].axhline(1e-3, color=COLORS["grey"], lw=0.8, ls="--")
    axes[1].set(xlabel=r"timing error $\Delta t$ [$\mu$s]", ylabel=r"phase error $\Delta\phi$")
    axes[1].legend(frameon=False, fontsize=6.5)
    for ax, label in zip(axes, ["a", "b"]):
        panel_label(ax, label)
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch19_priority_matrix(outdir: Path, filename: str) -> None:
    labels = ["stellar diam.", "rapid rotators", "binaries", "Be/WR lines", "novae", "Crab stats", "natural lasers", "SN Ia", "AGN BLR", "dark lensing"]
    readiness = np.array([0.92, 0.76, 0.72, 0.62, 0.50, 0.55, 0.48, 0.25, 0.18, 0.16])
    value = np.array([0.66, 0.82, 0.74, 0.78, 0.68, 0.62, 0.58, 0.90, 0.82, 0.78])
    risk = np.array([0.25, 0.45, 0.42, 0.50, 0.68, 0.60, 0.70, 0.88, 0.90, 0.93])
    fig, ax = plt.subplots(figsize=(4.15, 3.05))
    sizes = 80 + 260 * risk
    colors = [PALETTE[i % len(PALETTE)] for i in range(len(labels))]
    ax.scatter(readiness, value, s=sizes, c=colors, alpha=0.82, edgecolor="white", linewidth=0.5)
    offsets = {
        "stellar diam.": (0.025, -0.010),
        "rapid rotators": (0.025, 0.020),
        "binaries": (0.022, -0.018),
        "Be/WR lines": (0.024, 0.018),
        "novae": (0.020, 0.020),
        "Crab stats": (0.018, -0.028),
        "natural lasers": (0.020, -0.030),
        "SN Ia": (0.025, 0.030),
        "AGN BLR": (0.025, 0.030),
        "dark lensing": (0.028, -0.020),
    }
    for x, y, label in zip(readiness, value, labels):
        dx, dy = offsets[label]
        ax.text(x + dx, y + dy, label, fontsize=6.4, va="center")
    ax.axvline(0.6, color=COLORS["grey"], lw=0.8, ls="--")
    ax.axhline(0.7, color=COLORS["grey"], lw=0.8, ls="--")
    ax.text(0.62, 0.31, "first-generation zone", fontsize=7.0, color=COLORS["grey"])
    ax.set(xlabel="technical readiness", ylabel="science return", xlim=(0, 1.04), ylim=(0.28, 1.0))
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch20_hbt_lab_histogram(outdir: Path, filename: str) -> None:
    rng = np.random.default_rng(20)
    tau = np.linspace(-10.0, 10.0, 201)
    delta_tau = tau[1] - tau[0]
    pair_floor = 3.0e5
    tau_c = 1.15
    contrast = 0.075
    model_g2 = 1.0 + contrast * np.exp(-0.5 * (tau / tau_c) ** 2)
    random_pairs = pair_floor * (1.0 + 0.018 * np.cos(2 * np.pi * tau / 17.0))
    raw_pairs = rng.poisson(random_pairs * model_g2)
    shifted_pairs = rng.poisson(random_pairs)
    g2_hat = raw_pairs / np.maximum(shifted_pairs, 1)

    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.55))
    axes[0].step(tau, raw_pairs / 1e5, where="mid", color=COLORS["blue"], label="same-time pairs")
    axes[0].step(tau, shifted_pairs / 1e5, where="mid", color=COLORS["orange"], label="time-shift background")
    axes[0].set(xlabel=r"delay $\tau$ [ns]", ylabel=r"pairs per bin [$10^5$]")
    axes[0].legend(frameon=False)
    axes[1].errorbar(tau[::3], g2_hat[::3], yerr=np.sqrt(raw_pairs[::3]) / np.maximum(shifted_pairs[::3], 1), fmt="o", ms=2.2, color=COLORS["blue"], ecolor=COLORS["light_grey"], capsize=0)
    axes[1].plot(tau, model_g2, color=COLORS["black"], label=fr"$\tau_c={tau_c:.1f}$ ns")
    axes[1].axhline(1.0, color=COLORS["grey"], lw=0.8, ls="--")
    axes[1].set(xlabel=r"delay $\tau$ [ns]", ylabel=r"$\hat g^{(2)}(\tau)$", ylim=(0.985, 1.095))
    axes[1].legend(frameon=False)
    for ax, label in zip(axes, ["a", "b"]):
        panel_label(ax, label)
        clean_axis(ax, grid=True)
    fig.text(0.12, 0.01, fr"bin width $\Delta\tau={delta_tau:.2f}$ ns", fontsize=7.0, color=COLORS["grey"])
    save_figure(fig, outdir, filename)


def ch20_event_table_simulation(outdir: Path, filename: str) -> None:
    rng = np.random.default_rng(200)
    t = np.linspace(0, 120, 1201)
    dt = t[1] - t[0]
    rate = 180 + 42 * np.sin(2 * np.pi * t / 37) + 70 * np.exp(-0.5 * ((t - 72) / 8.5) ** 2)
    rate = np.clip(rate, 20, None)
    counts = rng.poisson(rate * dt)
    events = np.repeat(t, counts)
    energy = 500 + 42 * rng.normal(size=len(events)) + 18 * np.sin(2 * np.pi * events / 37)
    quality = rng.random(len(events)) > (0.06 + 0.16 * np.exp(-0.5 * ((events - 72) / 5.0) ** 2))
    bins = np.arange(0, 121, 4)
    good_counts, _ = np.histogram(events[quality], bins=bins)
    all_counts, _ = np.histogram(events, bins=bins)

    fig, axes = plt.subplots(1, 3, figsize=(8.05, 2.5), gridspec_kw={"wspace": 0.42})
    axes[0].plot(t, rate, color=COLORS["blue"])
    axes[0].fill_between(t, 0, rate, color=COLORS["blue"], alpha=0.14)
    axes[0].set(xlabel="time [s]", ylabel=r"rate $r(t)$ [s$^{-1}$]")
    axes[1].scatter(events[::18], energy[::18], s=3.8, c=np.where(quality[::18], COLORS["black"], COLORS["orange"]), alpha=0.45, linewidths=0)
    axes[1].set(xlabel="arrival time [s]", ylabel="channel energy [nm]")
    centers = 0.5 * (bins[1:] + bins[:-1])
    axes[2].step(centers, all_counts / np.diff(bins), where="mid", color=COLORS["grey"], label="all events")
    axes[2].step(centers, good_counts / np.diff(bins), where="mid", color=COLORS["green"], label="quality cut")
    axes[2].set(xlabel="time [s]", ylabel=r"binned rate [s$^{-1}$]")
    axes[2].legend(frameon=False)
    for ax, label in zip(axes, ["a", "b", "c"]):
        panel_label(ax, label)
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch20_uniform_disk_fit(outdir: Path, filename: str) -> None:
    rng = np.random.default_rng(201)
    lam = 416e-9
    mas_to_rad = np.pi / (180.0 * 3600.0 * 1000.0)
    theta_true = 1.0
    baselines = np.array([35, 55, 75, 95, 115, 140, 170, 210, 260, 320], dtype=float)
    x_true = np.pi * theta_true * mas_to_rad * baselines / lam
    vis2_true = disk_visibility(x_true) ** 2
    sigma = 0.025 + 0.05 * (1.0 - vis2_true)
    data = np.clip(vis2_true + rng.normal(0.0, sigma), 0.0, 1.05)
    b_grid = np.linspace(0, 340, 800)

    theta_grid = np.linspace(0.62, 1.42, 520)
    chi2 = []
    for theta in theta_grid:
        model = disk_visibility(np.pi * theta * mas_to_rad * baselines / lam) ** 2
        chi2.append(np.sum(((data - model) / sigma) ** 2))
    chi2 = np.array(chi2)
    posterior = np.exp(-0.5 * (chi2 - chi2.min()))
    posterior /= np.trapezoid(posterior, theta_grid)

    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.55))
    axes[0].errorbar(baselines, data, yerr=sigma, fmt="o", color=COLORS["black"], ecolor=COLORS["light_grey"], capsize=2.2, label="simulated data")
    for theta, color in [(0.82, COLORS["green"]), (1.0, COLORS["blue"]), (1.18, COLORS["orange"])]:
        axes[0].plot(b_grid, disk_visibility(np.pi * theta * mas_to_rad * b_grid / lam) ** 2, color=color, label=fr"$\theta={theta:.2f}$ mas")
    axes[0].set(xlabel="baseline B [m]", ylabel=r"$|V(B)|^2$", ylim=(-0.04, 1.08))
    axes[0].legend(frameon=False, ncol=2)
    axes[1].plot(theta_grid, posterior, color=COLORS["purple"])
    axes[1].axvline(theta_true, color=COLORS["grey"], lw=0.8, ls="--", label="input")
    axes[1].set(xlabel=r"disk diameter $\theta$ [mas]", ylabel="relative posterior")
    axes[1].legend(frameon=False)
    for ax, label in zip(axes, ["a", "b"]):
        panel_label(ax, label)
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch20_binary_visibility(outdir: Path, filename: str) -> None:
    lam = 500e-9
    mas_to_rad = np.pi / (180.0 * 3600.0 * 1000.0)
    b = np.linspace(0, 330, 900)
    sep_mas = 0.55
    phase = 2.0 * np.pi * b * sep_mas * mas_to_rad / lam

    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.55))
    for rho, color in [(1.0, COLORS["blue"]), (0.35, COLORS["orange"]), (0.12, COLORS["green"])]:
        vis2 = (1.0 + rho ** 2 + 2.0 * rho * np.cos(phase)) / (1.0 + rho) ** 2
        axes[0].plot(b, vis2, color=color, label=fr"$\rho={rho}$")
    axes[0].set(xlabel="projected baseline B [m]", ylabel=r"$|V|^2$", ylim=(-0.03, 1.05))
    axes[0].legend(frameon=False)

    phase_orbit = np.linspace(0, 1, 360)
    a_mas = 0.68
    inc = np.deg2rad(62.0)
    x = a_mas * np.cos(2 * np.pi * phase_orbit)
    y = a_mas * np.sin(2 * np.pi * phase_orbit) * np.cos(inc)
    baseline_angle = np.deg2rad(25.0)
    projected_sep = x * np.cos(baseline_angle) + y * np.sin(baseline_angle)
    vis2_orbit = (1.0 + 0.35 ** 2 + 2.0 * 0.35 * np.cos(2.0 * np.pi * 180.0 * projected_sep * mas_to_rad / lam)) / (1.0 + 0.35) ** 2
    axes[1].plot(phase_orbit, projected_sep, color=COLORS["purple"], label=r"$\mathbf{B}\cdot\mathbf{s}$")
    ax2 = axes[1].twinx()
    ax2.plot(phase_orbit, vis2_orbit, color=COLORS["orange"], label=r"$|V|^2$")
    axes[1].set(xlabel="orbital phase", ylabel="projected separation [mas]")
    ax2.set(ylabel=r"$|V|^2$", ylim=(-0.03, 1.05))
    lines, labels = axes[1].get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    axes[1].legend(lines + lines2, labels + labels2, frameon=False, loc="upper right")
    for ax, label in zip(axes, ["a", "b"]):
        panel_label(ax, label)
        clean_axis(ax, grid=True)
    ax2.spines["top"].set_visible(False)
    save_figure(fig, outdir, filename)


def ch20_correlator_scaling(outdir: Path, filename: str) -> None:
    n_tel = np.arange(2, 81)
    baselines = n_tel * (n_tel - 1) / 2
    bins_per_second = np.logspace(6, 10, 400)
    channels = [1, 8, 64]
    bits = 16.0

    fig, axes = plt.subplots(1, 2, figsize=(7.1, 2.55))
    axes[0].plot(n_tel, baselines, color=COLORS["blue"], label=r"$N_{\rm tel}(N_{\rm tel}-1)/2$")
    axes[0].plot(n_tel, n_tel * 12, color=COLORS["grey"], ls="--", label="linear reference")
    axes[0].set(xlabel="number of telescopes", ylabel="baselines")
    axes[0].legend(frameon=False)
    for n_ch, color in zip(channels, [COLORS["green"], COLORS["orange"], COLORS["purple"]]):
        rate_gbps = bins_per_second * bits * n_ch / 1e9
        axes[1].loglog(1.0 / bins_per_second * 1e9, rate_gbps, color=color, label=fr"$N_\nu={n_ch}$")
    axes[1].axvline(4.0, color=COLORS["grey"], lw=0.85, ls="--")
    axes[1].set(xlabel=r"time bin $\Delta t$ [ns]", ylabel="single-channel stream [Gb/s]")
    axes[1].legend(frameon=False)
    for ax, label in zip(axes, ["a", "b"]):
        panel_label(ax, label)
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch20_spade_exercise(outdir: Path, filename: str) -> None:
    import math

    d = np.linspace(0.005, 4.0, 700)
    q = d ** 2 / 16.0
    direct = d ** 2 / (4.0 + d ** 2)
    qfi = np.ones_like(d)
    fig, axes = plt.subplots(1, 2, figsize=(7.1, 2.55))
    axes[0].plot(d, direct, color=COLORS["blue"], label="direct image pixels")
    axes[0].plot(d, qfi, color=COLORS["orange"], label="ideal mode sorting")
    axes[0].set(xlabel=r"separation $s/\sigma$", ylabel=r"relative Fisher information", ylim=(-0.02, 1.08))
    axes[0].legend(frameon=False)
    for n, color in zip(range(4), PALETTE[:4]):
        axes[1].plot(d, np.exp(-q) * q ** n / math.factorial(n), color=color, label=fr"$n={n}$")
    axes[1].set(xlabel=r"separation $s/\sigma$", ylabel=r"mode probability $p_n$")
    axes[1].legend(frameon=False, ncol=2)
    for ax, label in zip(axes, ["a", "b"]):
        panel_label(ax, label)
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch20_typeia_distance_posterior(outdir: Path, filename: str) -> None:
    rng = np.random.default_rng(202)
    c = 2.99792458e8
    pc = 3.085677581e16
    uas_per_rad = 180.0 / np.pi * 3600.0 * 1e6
    v = 1.05e7
    days = np.linspace(3, 34, 240)
    distances_mpc = [8.0, 16.0, 32.0]

    obs_days = np.array([8.0, 13.0, 19.0, 27.0])
    d_true = 16.0
    theta_true = v * obs_days * 86400.0 / (d_true * 1e6 * pc) * uas_per_rad
    sigma_theta = 0.16 * theta_true + 0.18
    theta_obs = theta_true + rng.normal(0.0, sigma_theta)
    d_grid = np.linspace(6.0, 34.0, 600)
    chi2 = []
    for dist in d_grid:
        theta_model = v * obs_days * 86400.0 / (dist * 1e6 * pc) * uas_per_rad
        chi2.append(np.sum(((theta_obs - theta_model) / sigma_theta) ** 2))
    chi2 = np.array(chi2)
    posterior = np.exp(-0.5 * (chi2 - chi2.min()))
    posterior /= np.trapezoid(posterior, d_grid)

    fig, axes = plt.subplots(1, 2, figsize=(7.1, 2.55))
    for dist, color in zip(distances_mpc, [COLORS["blue"], COLORS["orange"], COLORS["green"]]):
        theta = v * days * 86400.0 / (dist * 1e6 * pc) * uas_per_rad
        axes[0].plot(days, theta, color=color, label=fr"{dist:.0f} Mpc")
    axes[0].errorbar(obs_days, theta_obs, yerr=sigma_theta, fmt="o", color=COLORS["black"], ecolor=COLORS["light_grey"], capsize=2.2)
    axes[0].set(xlabel="days after explosion", ylabel=r"angular radius [$\mu$as]")
    axes[0].legend(frameon=False)
    axes[1].plot(d_grid, posterior, color=COLORS["purple"])
    axes[1].axvline(d_true, color=COLORS["grey"], lw=0.85, ls="--", label="input distance")
    axes[1].set(xlabel="angular-diameter distance [Mpc]", ylabel="relative posterior")
    axes[1].legend(frameon=False)
    for ax, label in zip(axes, ["a", "b"]):
        panel_label(ax, label)
        clean_axis(ax, grid=True)
    fig.text(0.11, 0.01, fr"velocity scale $v={v / c:.3f}c$", fontsize=7.0, color=COLORS["grey"])
    save_figure(fig, outdir, filename)


def ch21_g2_scaling_mistake(outdir: Path, filename: str) -> None:
    ratio = np.logspace(0, 8, 600)
    bandwidth_nm = np.logspace(-3, 2, 500)
    lam = 500e-9
    c = 2.99792458e8
    dt = 1e-9
    tau_c = lam ** 2 / (c * bandwidth_nm * 1e-9)

    fig, axes = plt.subplots(1, 2, figsize=(7.1, 2.55))
    for modes, color in zip([1, 10, 100, 1000], PALETTE[:4]):
        axes[0].loglog(ratio, 1.0 / (modes * ratio), color=color, label=fr"$M={modes}$")
    axes[0].axhline(1e-5, color=COLORS["grey"], lw=0.85, ls="--", label=r"$10^{-5}$ floor")
    axes[0].set(xlabel=r"time bin $\Delta t/\tau_c$", ylabel=r"observed contrast $g^{(2)}(0)-1$")
    axes[0].legend(frameon=False, ncol=2)

    for modes, color in zip([1, 10, 100], [COLORS["blue"], COLORS["orange"], COLORS["green"]]):
        contrast = np.minimum(1.0, tau_c / dt) / modes
        axes[1].loglog(bandwidth_nm, contrast, color=color, label=fr"$M={modes}$")
    axes[1].axvline(10.0, color=COLORS["grey"], lw=0.85, ls="--")
    axes[1].set(xlabel=r"filter width $\Delta\lambda$ [nm]", ylabel=fr"contrast at $\Delta t={dt*1e9:.0f}$ ns")
    axes[1].legend(frameon=False)
    for ax, label in zip(axes, ["a", "b"]):
        panel_label(ax, label)
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch21_poisson_false_alarm(outdir: Path, filename: str) -> None:
    n = np.arange(0, 42)
    mu = 8.0
    p = poisson_pmf(n, mu)
    threshold = 17
    p0 = p[n >= threshold].sum()
    trials = np.logspace(0, 9, 500)

    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.55))
    axes[0].bar(n, p, color=COLORS["blue"], width=0.86)
    axes[0].axvspan(threshold - 0.5, n.max() + 0.5, color=COLORS["orange"], alpha=0.22, label=fr"$p_0={p0:.1e}$")
    axes[0].set(xlabel="counts in one bin", ylabel=r"$P(N|\mu=8)$", yscale="log", ylim=(1e-8, 0.25))
    axes[0].legend(frameon=False)
    for single_p, color in zip([p0, 1e-5, 1e-3], [COLORS["orange"], COLORS["green"], COLORS["purple"]]):
        axes[1].semilogx(trials, 1.0 - (1.0 - single_p) ** trials, color=color, label=fr"$p_0={single_p:.0e}$")
    axes[1].axhline(0.5, color=COLORS["grey"], lw=0.85, ls="--")
    axes[1].set(xlabel=r"number of trials $N_{\rm trial}$", ylabel=r"$p_{\rm any}$", ylim=(-0.02, 1.02))
    axes[1].legend(frameon=False)
    for ax, label in zip(axes, ["a", "b"]):
        panel_label(ax, label)
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch21_calibration_artifacts(outdir: Path, filename: str) -> None:
    tau = np.linspace(-25, 25, 500)
    sky = 5.0e-5 * np.exp(-0.5 * (tau / 3.2) ** 2)
    crosstalk = 8.0e-4 * np.exp(-0.5 * (tau / 0.75) ** 2)
    residual = 2.5e-5 * np.exp(-0.5 * (tau / 1.2) ** 2)
    hours = np.logspace(-1, 2.2, 500)
    stat = 2.2e-4 / np.sqrt(hours)

    fig, axes = plt.subplots(1, 2, figsize=(7.1, 2.55))
    axes[0].plot(tau, (sky + crosstalk) * 1e4, color=COLORS["blue"], label="raw excess")
    axes[0].plot(tau, sky * 1e4, color=COLORS["green"], label="stellar bunching")
    axes[0].plot(tau, crosstalk * 1e4, color=COLORS["orange"], label="electronic artefact")
    axes[0].plot(tau, residual * 1e4, color=COLORS["purple"], ls="--", label="residual after subtraction")
    axes[0].set(xlabel=r"delay $\tau$ [ns]", ylabel=r"excess correlation [$10^{-4}$]")
    axes[0].legend(frameon=False, fontsize=6.7)
    for floor, color, label in [(3e-5, COLORS["orange"], r"floor $3\times10^{-5}$"), (1e-5, COLORS["green"], r"floor $10^{-5}$")]:
        axes[1].loglog(hours, np.sqrt(stat ** 2 + floor ** 2), color=color, label=label)
    axes[1].loglog(hours, stat, color=COLORS["grey"], ls="--", label=r"$T^{-1/2}$ only")
    axes[1].set(xlabel="integration time [h]", ylabel=r"uncertainty in $g^{(2)}-1$")
    axes[1].legend(frameon=False)
    for ax, label in zip(axes, ["a", "b"]):
        panel_label(ax, label)
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch21_phase_loss(outdir: Path, filename: str) -> None:
    theta = np.array([0.0, 0.72])
    flux = np.array([1.0, 0.36])
    u = np.linspace(0.0, 7.0, 700)
    v_forward = (flux[0] + flux[1] * np.exp(-2j * np.pi * u * theta[1])) / flux.sum()
    v_mirror = (flux[0] + flux[1] * np.exp(2j * np.pi * u * theta[1])) / flux.sum()

    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.55))
    axes[0].vlines(theta, 0, flux, color=COLORS["blue"], lw=2.0, label="source")
    axes[0].plot(theta, flux, "o", color=COLORS["blue"])
    axes[0].vlines(-theta, 0, flux, color=COLORS["orange"], lw=1.7, ls="--", label="mirror")
    axes[0].plot(-theta, flux, "o", color=COLORS["orange"], ms=3.4)
    axes[0].set(xlabel=r"sky coordinate $\theta$ [arb.]", ylabel="relative brightness", xlim=(-0.95, 0.95), ylim=(0, 1.08))
    axes[0].legend(frameon=False)
    axes[1].plot(u, np.abs(v_forward) ** 2, color=COLORS["black"], label=r"$|V|^2$ both")
    ax2 = axes[1].twinx()
    ax2.plot(u, np.unwrap(np.angle(v_forward)), color=COLORS["blue"], label="phase")
    ax2.plot(u, np.unwrap(np.angle(v_mirror)), color=COLORS["orange"], ls="--", label="mirror phase")
    axes[1].set(xlabel=r"spatial frequency $u=B/\lambda$", ylabel=r"$|V|^2$", ylim=(-0.03, 1.05))
    ax2.set(ylabel="visibility phase [rad]")
    lines, labels = axes[1].get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    axes[1].legend(lines + lines2, labels + labels2, frameon=False, fontsize=6.7, loc="lower left")
    for ax, label in zip(axes, ["a", "b"]):
        panel_label(ax, label)
        clean_axis(ax, grid=True)
    ax2.spines["top"].set_visible(False)
    save_figure(fig, outdir, filename)


def ch21_superresolution_budget(outdir: Path, filename: str) -> None:
    n_ph = np.logspace(2, 10, 600)
    sep = 0.20
    f_direct = sep ** 2 / 8.0
    f_spade = 0.25
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.55))
    axes[0].loglog(n_ph, np.sqrt(1.0 / (n_ph * f_direct)), color=COLORS["blue"], label="direct image")
    axes[0].loglog(n_ph, np.sqrt(1.0 / (n_ph * f_spade)), color=COLORS["orange"], label="ideal mode sorting")
    for floor, color in [(0.01, COLORS["green"]), (0.003, COLORS["purple"])]:
        axes[0].loglog(n_ph, np.sqrt(1.0 / (n_ph * f_spade) + floor ** 2), color=color, ls="--", label=fr"mode + floor {floor:.3f}")
    axes[0].set(xlabel="detected photons", ylabel=r"uncertainty in $s/\sigma$")
    axes[0].legend(frameon=False, fontsize=6.6)

    modes = np.arange(1, 13)
    moments = np.arange(1, 13)
    photons_needed = 2e3 * np.exp(0.38 * moments)
    axes[1].semilogy(modes, photons_needed, "o-", color=COLORS["purple"])
    axes[1].set(xlabel="highest recovered mode or moment", ylabel="toy photons needed")
    axes[1].axhline(1e6, color=COLORS["grey"], lw=0.85, ls="--")
    axes[1].text(1.4, 1.35e6, r"$10^6$ photons", fontsize=7.0, color=COLORS["grey"])
    for ax, label in zip(axes, ["a", "b"]):
        panel_label(ax, label)
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch21_nonpoisson_diagnostics(outdir: Path, filename: str) -> None:
    dt = np.logspace(-4, 2, 500)
    rate = 600.0
    modulation = 0.35
    poisson = np.ones_like(dt)
    variable = 1.0 + 0.5 * modulation ** 2 * rate * dt
    deadtime = np.full_like(dt, 1.0 / (1.0 + rate * 80e-9) ** 2)
    afterpulse = 1.0 + 0.018 * np.exp(-dt / 0.015)
    tau = np.linspace(0, 200, 500)
    ap_kernel = 0.012 * np.exp(-tau / 35.0)
    dead_kernel = -0.010 * np.exp(-0.5 * (tau / 8.0) ** 2)

    fig, axes = plt.subplots(1, 2, figsize=(7.1, 2.55))
    axes[0].loglog(dt, poisson, color=COLORS["black"], label="steady Poisson")
    axes[0].loglog(dt, variable, color=COLORS["blue"], label="variable source")
    axes[0].loglog(dt, deadtime, color=COLORS["orange"], label="dead-time toy")
    axes[0].loglog(dt, afterpulse, color=COLORS["green"], label="afterpulse toy")
    axes[0].set(xlabel="counting bin width [s]", ylabel="Fano factor Var(N)/E(N)")
    axes[0].legend(frameon=False, fontsize=6.7)
    axes[1].plot(tau, ap_kernel * 100.0, color=COLORS["green"], label="afterpulsing")
    axes[1].plot(tau, dead_kernel * 100.0, color=COLORS["orange"], label="dead-time deficit")
    axes[1].axhline(0.0, color=COLORS["grey"], lw=0.8)
    axes[1].set(xlabel=r"delay $\tau$ [ns]", ylabel=r"short-lag excess [%]")
    axes[1].legend(frameon=False)
    for ax, label in zip(axes, ["a", "b"]):
        panel_label(ax, label)
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch21_maser_mixed_statistics(outdir: Path, filename: str) -> None:
    f_line = np.linspace(0, 1, 500)
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.55))
    for modes, color in zip([1, 10, 100], [COLORS["blue"], COLORS["orange"], COLORS["green"]]):
        contrast = (1.0 - f_line) ** 2 / modes
        axes[0].plot(f_line, contrast, color=color, label=fr"thermal continuum $M={modes}$")
    axes[0].plot(f_line, 0.12 * f_line ** 2, color=COLORS["purple"], ls="--", label="noisy unsaturated line")
    axes[0].set(xlabel="fraction of flux in narrow line", ylabel=r"$g^{(2)}(0)-1$ before timing dilution", ylim=(-0.02, 1.05))
    axes[0].legend(frameon=False, fontsize=6.7)

    width_mhz = np.logspace(0, 5, 500)
    tau_c_ns = 1.0e3 / (np.pi * width_mhz)
    for dt_ns, color in zip([0.1, 1.0, 10.0], [COLORS["green"], COLORS["blue"], COLORS["orange"]]):
        axes[1].loglog(width_mhz, np.minimum(1.0, tau_c_ns / dt_ns), color=color, label=fr"$\Delta t={dt_ns:g}$ ns")
    axes[1].set(xlabel=r"line width $\Delta\nu$ [MHz]", ylabel="timing dilution factor")
    axes[1].legend(frameon=False)
    for ax, label in zip(axes, ["a", "b"]):
        panel_label(ax, label)
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch22_roadmap_trade_space(outdir: Path, filename: str) -> None:
    labels = ["stellar SII", "binary disks", "spectral SII", "SN Ia", "Crab timing", "mode sorting", "network telescope", "teaching lab"]
    readiness = np.array([0.86, 0.72, 0.52, 0.33, 0.62, 0.42, 0.16, 0.95])
    value = np.array([0.66, 0.74, 0.78, 0.92, 0.56, 0.72, 0.88, 0.38])
    cost = np.array([0.40, 0.52, 0.62, 0.80, 0.35, 0.58, 0.95, 0.10])
    risk = np.array([0.28, 0.44, 0.58, 0.80, 0.48, 0.62, 0.92, 0.15])
    fig, ax = plt.subplots(figsize=(4.25, 3.05))
    sizes = 110 + 310 * cost
    colors = [PALETTE[i % len(PALETTE)] for i in range(len(labels))]
    ax.scatter(readiness, value, s=sizes, c=colors, alpha=0.78, edgecolor="white", linewidth=0.5)
    for x, y, r, label in zip(readiness, value, risk, labels):
        dx = 0.016
        dy = 0.014 if y < 0.82 else -0.035
        ax.text(x + dx, y + dy, label, fontsize=6.8)
    ax.axvspan(0.68, 1.02, color=COLORS["light_grey"], alpha=0.45, lw=0)
    ax.axhline(0.70, color=COLORS["grey"], lw=0.8, ls="--")
    ax.text(0.70, 0.18, "first proposals", fontsize=7.0, color=COLORS["grey"])
    ax.text(0.19, 0.93, "high value,\nhigh risk", fontsize=7.0, color=COLORS["grey"])
    ax.set(xlabel="technical readiness", ylabel="science return", xlim=(0.05, 1.04), ylim=(0.12, 1.02))
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch22_program_timeline(outdir: Path, filename: str) -> None:
    tasks = [
        ("course HBT + simulator", 2026, 2028.0, COLORS["green"]),
        ("detectors + timing", 2026.5, 2030.0, COLORS["blue"]),
        ("stellar SII sample", 2028.0, 2033.0, COLORS["orange"]),
        ("spectral/polarized SII", 2030.0, 2037.0, COLORS["purple"]),
        ("transient follow-up", 2031.0, 2038.0, COLORS["sky"]),
        ("local mode sorting", 2029.0, 2036.0, COLORS["yellow"]),
        ("network pathfinder", 2034.0, 2045.0, COLORS["black"]),
    ]
    fig, ax = plt.subplots(figsize=(4.55, 3.05))
    for i, (label, start, end, color) in enumerate(tasks):
        ax.barh(i, end - start, left=start, height=0.50, color=color, alpha=0.86)
        text_color = "white" if color in [COLORS["purple"], COLORS["black"], COLORS["orange"]] else COLORS["black"]
        bbox = dict(fc="white", ec="none", alpha=0.72, pad=0.15) if color == COLORS["blue"] else None
        ax.text(start + 0.10, i, label, va="center", ha="left", color=text_color, fontsize=7.0, bbox=bbox)
    for year in [2030, 2040]:
        ax.axvline(year, color=COLORS["grey"], lw=0.8, ls="--")
    ax.set(yticks=[], xlabel="year", xlim=(2026, 2046), ylim=(-0.8, len(tasks) - 0.2))
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch22_milestone_gates(outdir: Path, filename: str) -> None:
    phases = ["lab", "first stars", "sample", "multi-channel", "network"]
    metrics = ["photon rate", "timing", "calibration", "pipeline", "science sample"]
    readiness = np.array([
        [0.95, 0.80, 0.65, 0.70, 0.20],
        [0.82, 0.76, 0.55, 0.62, 0.38],
        [0.75, 0.82, 0.72, 0.78, 0.70],
        [0.52, 0.72, 0.48, 0.58, 0.62],
        [0.20, 0.42, 0.20, 0.30, 0.28],
    ])
    fig, ax = plt.subplots(figsize=(4.65, 2.85))
    im = ax.imshow(readiness, cmap="viridis", vmin=0, vmax=1, aspect="auto")
    for i in range(readiness.shape[0]):
        for j in range(readiness.shape[1]):
            ax.text(j, i, f"{readiness[i, j]:.2f}", ha="center", va="center", color="white" if readiness[i, j] < 0.55 else COLORS["black"], fontsize=6.8)
    ax.set_xticks(np.arange(len(metrics)), metrics, rotation=28, ha="right")
    ax.set_yticks(np.arange(len(phases)), phases)
    ax.set_xlabel("milestone gate")
    cbar = fig.colorbar(im, ax=ax, fraction=0.045, pad=0.025)
    cbar.set_label("readiness score")
    clean_axis(ax)
    save_figure(fig, outdir, filename)


def ch22_data_product_stack(outdir: Path, filename: str) -> None:
    fig, ax = plt.subplots(figsize=(4.55, 3.05))
    ax.set_axis_off()
    boxes = [
        (0.08, 0.72, 0.22, 0.15, "event table\nt, d, nu, p, q", COLORS["blue"]),
        (0.39, 0.72, 0.22, 0.15, "correlations\ng2, C_ab", COLORS["orange"]),
        (0.70, 0.72, 0.22, 0.15, "visibility\n|V|2", COLORS["green"]),
        (0.24, 0.39, 0.22, 0.15, "likelihood\nL(theta)", COLORS["purple"]),
        (0.55, 0.39, 0.22, 0.15, "posterior\nscience model", COLORS["sky"]),
        (0.39, 0.10, 0.22, 0.15, "archive\ncode + null tests", COLORS["yellow"]),
    ]
    for x, y, w, h, text, color in boxes:
        ax.add_patch(Rectangle((x, y), w, h, fc=color, ec="white", lw=0.8, alpha=0.88))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=7.2, color="white" if color in [COLORS["blue"], COLORS["purple"], COLORS["green"]] else COLORS["black"])
    arrows = [
        ((0.30, 0.795), (0.39, 0.795)),
        ((0.61, 0.795), (0.70, 0.795)),
        ((0.81, 0.72), (0.66, 0.54)),
        ((0.50, 0.72), (0.35, 0.54)),
        ((0.46, 0.465), (0.55, 0.465)),
        ((0.66, 0.39), (0.52, 0.25)),
        ((0.35, 0.39), (0.46, 0.25)),
    ]
    for start, end in arrows:
        ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=11, lw=1.0, color=COLORS["black"]))
    ax.text(0.5, 0.94, "proposal deliverables should name each data product", ha="center", fontsize=8.0, color=COLORS["black"])
    save_figure(fig, outdir, filename)


def ch22_risk_register(outdir: Path, filename: str) -> None:
    labels = ["target too faint", "timing drift", "zero-baseline bias", "weather selection", "model degeneracy", "data volume", "network loss"]
    probability = np.array([0.55, 0.32, 0.46, 0.60, 0.52, 0.42, 0.82])
    impact = np.array([0.72, 0.78, 0.82, 0.55, 0.65, 0.58, 0.92])
    mitigation = np.array([0.45, 0.65, 0.55, 0.40, 0.50, 0.70, 0.25])
    fig, ax = plt.subplots(figsize=(4.25, 3.05))
    ax.scatter(probability, impact, s=90 + 260 * (1 - mitigation), c=PALETTE[:len(labels)], alpha=0.82, edgecolor="white", linewidth=0.5)
    offsets = {
        "target too faint": (0.035, 0.030, "left"),
        "timing drift": (0.040, -0.040, "left"),
        "zero-baseline bias": (-0.260, 0.065, "left"),
        "weather selection": (-0.255, -0.035, "left"),
        "model degeneracy": (0.035, -0.025, "left"),
        "data volume": (-0.090, 0.055, "left"),
        "network loss": (-0.255, -0.045, "left"),
    }
    for x, y, label in zip(probability, impact, labels):
        dx, dy, ha = offsets[label]
        ax.text(
            x + dx,
            y + dy,
            label,
            fontsize=6.6,
            ha=ha,
            va="center",
            bbox=dict(fc="white", ec="none", alpha=0.70, pad=0.2),
        )
    ax.axvline(0.5, color=COLORS["grey"], lw=0.8, ls="--")
    ax.axhline(0.7, color=COLORS["grey"], lw=0.8, ls="--")
    ax.set(xlabel="probability", ylabel="impact", xlim=(0.05, 1.0), ylim=(0.25, 1.02))
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


RECIPES = {
    "ch01_event_table_map.pdf": ch01_event_table_map,
    "ch01_phase_interference.pdf": ch01_phase_interference,
    "ch01_projected_baseline.pdf": ch01_projected_baseline,
    "ch01_thermal_fluctuation_hbt.pdf": ch01_thermal_fluctuation_hbt,
    "ch01_fourier_visibility.pdf": ch01_fourier_visibility,
    "ch01_hbt_schematic.pdf": ch01_hbt_schematic,
    "ch01_photon_count_statistics.pdf": ch01_photon_count_statistics,
    "ch01_resolution_baseline.pdf": ch01_resolution_baseline,
    "ch01_correlation_dilution_budget.pdf": ch01_correlation_dilution_budget,
    "ch01_polarization_mueller_matrix.pdf": ch01_polarization_mueller_matrix,
    "ch01_quantum_detection_map.pdf": ch01_quantum_detection_map,
    "ch01_fisher_visibility_design.pdf": ch01_fisher_visibility_design,
    "ch02_mean_intensity_vs_correlation.pdf": ch02_mean_intensity_vs_correlation,
    "ch02_event_table_information.pdf": ch02_event_table_information,
    "ch02_contrast_dilution.pdf": ch02_contrast_dilution,
    "ch02_revival_timeline.pdf": ch02_revival_timeline,
    "ch02_science_case_map.pdf": ch02_science_case_map,
    "ch03_phase_space_states.pdf": ch03_phase_space_states,
    "ch03_state_count_distributions.pdf": ch03_state_count_distributions,
    "ch03_blackbody_mode_occupation.pdf": ch03_blackbody_mode_occupation,
    "ch03_coherence_time_dilution.pdf": ch03_coherence_time_dilution,
    "ch03_detection_loss_background.pdf": ch03_detection_loss_background,
    "ch03_nonclassical_mixing_boundary.pdf": ch03_nonclassical_mixing_boundary,
    "ch04_mandel_q_g2.pdf": ch04_mandel_q_g2,
    "ch04_siegert_relation.pdf": ch04_siegert_relation,
    "ch04_factorial_moments.pdf": ch04_factorial_moments,
    "ch04_response_convolution.pdf": ch04_response_convolution,
    "ch04_delay_histogram_estimator.pdf": ch04_delay_histogram_estimator,
    "ch04_deadtime_pileup_bias.pdf": ch04_deadtime_pileup_bias,
    "ch04_g3_closure_phase.pdf": ch04_g3_closure_phase,
    "ch04_frequency_polarization_matrix.pdf": ch04_frequency_polarization_matrix,
    "ch05_vcz_visibility_models.pdf": ch05_vcz_visibility_models,
    "ch05_sii_signal_vs_baseline.pdf": ch05_sii_signal_vs_baseline,
    "ch05_uniform_disk_resolution.pdf": ch05_uniform_disk_resolution,
    "ch05_snr_scaling.pdf": ch05_snr_scaling,
    "ch05_uv_coverage.pdf": ch05_uv_coverage,
    "ch05_zero_baseline_calibration.pdf": ch05_zero_baseline_calibration,
    "ch05_phase_ambiguity.pdf": ch05_phase_ambiguity,
    "ch05_error_budget.pdf": ch05_error_budget,
    "ch06_detector_timing_response.pdf": ch06_detector_timing_response,
    "ch06_deadtime_saturation.pdf": ch06_deadtime_saturation,
    "ch06_event_table_schema.pdf": ch06_event_table_schema,
    "ch06_detector_trade_space.pdf": ch06_detector_trade_space,
    "ch06_time_budget.pdf": ch06_time_budget,
    "ch06_spectral_resolution_coherence.pdf": ch06_spectral_resolution_coherence,
    "ch07_poisson_likelihood.pdf": ch07_poisson_likelihood,
    "ch07_time_shift_background.pdf": ch07_time_shift_background,
    "ch07_correlator_scaling.pdf": ch07_correlator_scaling,
    "ch07_covariance_matrix.pdf": ch07_covariance_matrix,
    "ch07_fisher_scaling.pdf": ch07_fisher_scaling,
    "ch08_rayleigh_information.pdf": ch08_rayleigh_information,
    "ch08_spade_probabilities.pdf": ch08_spade_probabilities,
    "ch08_cramer_rao_bound.pdf": ch08_cramer_rao_bound,
    "ch08_direct_image_vs_modes.pdf": ch08_direct_image_vs_modes,
    "ch08_visibility_fisher_design.pdf": ch08_visibility_fisher_design,
    "ch09_radiation_g2_diagnostics.pdf": ch09_radiation_g2_diagnostics,
    "ch09_brightness_temperature_scale.pdf": ch09_brightness_temperature_scale,
    "ch09_thermal_mode_dilution.pdf": ch09_thermal_mode_dilution,
    "ch09_spectral_mechanisms.pdf": ch09_spectral_mechanisms,
    "ch09_diagnostic_plane.pdf": ch09_diagnostic_plane,
    "ch10_stellar_diameter_visibility.pdf": ch10_stellar_diameter_visibility,
    "ch10_binary_visibility.pdf": ch10_binary_visibility,
    "ch10_limb_darkening.pdf": ch10_limb_darkening,
    "ch10_rotation_oblateness.pdf": ch10_rotation_oblateness,
    "ch10_teff_error_budget.pdf": ch10_teff_error_budget,
    "ch11_white_dwarf_mass_radius.pdf": ch11_white_dwarf_mass_radius,
    "ch11_magnetic_cv_flow_map.pdf": ch11_magnetic_cv_flow_map,
    "ch11_light_cylinder_phase.pdf": ch11_light_cylinder_phase,
    "ch11_stokes_qu_track.pdf": ch11_stokes_qu_track,
    "ch11_birefringence_energy.pdf": ch11_birefringence_energy,
    "ch11_hotspot_lightcurve.pdf": ch11_hotspot_lightcurve,
    "ch12_black_hole_scales.pdf": ch12_black_hole_scales,
    "ch12_accretion_disk_radii.pdf": ch12_accretion_disk_radii,
    "ch12_blr_reverberation_interferometry.pdf": ch12_blr_reverberation_interferometry,
    "ch12_photon_ring_visibility.pdf": ch12_photon_ring_visibility,
    "ch12_variability_autocorrelation.pdf": ch12_variability_autocorrelation,
    "ch12_hawking_temperature_scale.pdf": ch12_hawking_temperature_scale,
    "ch13_transient_event_likelihood.pdf": ch13_transient_event_likelihood,
    "ch13_expanding_fireball_resolution.pdf": ch13_expanding_fireball_resolution,
    "ch13_multimessenger_delay.pdf": ch13_multimessenger_delay,
    "ch13_kilonova_color_evolution.pdf": ch13_kilonova_color_evolution,
    "ch13_afterglow_synchrotron_breaks.pdf": ch13_afterglow_synchrotron_breaks,
    "ch13_tde_fallback_reprocessing.pdf": ch13_tde_fallback_reprocessing,
    "ch14_dispersion_delay.pdf": ch14_dispersion_delay,
    "ch14_faraday_rotation.pdf": ch14_faraday_rotation,
    "ch14_scattering_broadening.pdf": ch14_scattering_broadening,
    "ch14_dust_extinction_polarization.pdf": ch14_dust_extinction_polarization,
    "ch14_lensing_time_delay.pdf": ch14_lensing_time_delay,
    "ch14_wave_lensing_interference.pdf": ch14_wave_lensing_interference,
    "ch14_cosmic_bell_lightcones.pdf": ch14_cosmic_bell_lightcones,
    "ch15_axion_conversion.pdf": ch15_axion_conversion,
    "ch15_axion_polarization_oscillation.pdf": ch15_axion_polarization_oscillation,
    "ch15_cosmic_birefringence.pdf": ch15_cosmic_birefringence,
    "ch15_black_hole_axion_cloud.pdf": ch15_black_hole_axion_cloud,
    "ch15_frb_faraday_foreground.pdf": ch15_frb_faraday_foreground,
    "ch15_pulsar_array_correlation.pdf": ch15_pulsar_array_correlation,
    "ch15_dark_matter_lensing.pdf": ch15_dark_matter_lensing,
    "ch16_cmb_blackbody.pdf": ch16_cmb_blackbody,
    "ch16_cmb_power_spectrum.pdf": ch16_cmb_power_spectrum,
    "ch16_squeezed_modes.pdf": ch16_squeezed_modes,
    "ch16_non_gaussian_templates.pdf": ch16_non_gaussian_templates,
    "ch16_bmode_constraints.pdf": ch16_bmode_constraints,
    "ch16_birefringence_eb.pdf": ch16_birefringence_eb,
    "ch17_architecture_loss.pdf": ch17_architecture_loss,
    "ch17_entanglement_resources.pdf": ch17_entanglement_resources,
    "ch17_timebin_scaling.pdf": ch17_timebin_scaling,
    "ch17_fidelity_distance.pdf": ch17_fidelity_distance,
    "ch17_fisher_visibility.pdf": ch17_fisher_visibility,
    "ch17_network_parameter_space.pdf": ch17_network_parameter_space,
    "ch18_photon_rate_magnitude.pdf": ch18_photon_rate_magnitude,
    "ch18_coherence_dilution.pdf": ch18_coherence_dilution,
    "ch18_snr_heatmap.pdf": ch18_snr_heatmap,
    "ch18_visibility_fisher.pdf": ch18_visibility_fisher,
    "ch18_uv_coverage.pdf": ch18_uv_coverage,
    "ch18_background_dilution.pdf": ch18_background_dilution,
    "ch18_error_budget.pdf": ch18_error_budget,
    "ch19_science_case_feasibility.pdf": ch19_science_case_feasibility,
    "ch19_binary_visibility.pdf": ch19_binary_visibility,
    "ch19_transient_expansion.pdf": ch19_transient_expansion,
    "ch19_natural_laser_statistics.pdf": ch19_natural_laser_statistics,
    "ch19_crab_phase_windows.pdf": ch19_crab_phase_windows,
    "ch19_priority_matrix.pdf": ch19_priority_matrix,
    "ch20_hbt_lab_histogram.pdf": ch20_hbt_lab_histogram,
    "ch20_event_table_simulation.pdf": ch20_event_table_simulation,
    "ch20_uniform_disk_fit.pdf": ch20_uniform_disk_fit,
    "ch20_binary_visibility.pdf": ch20_binary_visibility,
    "ch20_correlator_scaling.pdf": ch20_correlator_scaling,
    "ch20_spade_exercise.pdf": ch20_spade_exercise,
    "ch20_typeia_distance_posterior.pdf": ch20_typeia_distance_posterior,
    "ch21_g2_scaling_mistake.pdf": ch21_g2_scaling_mistake,
    "ch21_poisson_false_alarm.pdf": ch21_poisson_false_alarm,
    "ch21_calibration_artifacts.pdf": ch21_calibration_artifacts,
    "ch21_phase_loss.pdf": ch21_phase_loss,
    "ch21_superresolution_budget.pdf": ch21_superresolution_budget,
    "ch21_nonpoisson_diagnostics.pdf": ch21_nonpoisson_diagnostics,
    "ch21_maser_mixed_statistics.pdf": ch21_maser_mixed_statistics,
    "ch22_roadmap_trade_space.pdf": ch22_roadmap_trade_space,
    "ch22_program_timeline.pdf": ch22_program_timeline,
    "ch22_milestone_gates.pdf": ch22_milestone_gates,
    "ch22_data_product_stack.pdf": ch22_data_product_stack,
    "ch22_risk_register.pdf": ch22_risk_register,
}
