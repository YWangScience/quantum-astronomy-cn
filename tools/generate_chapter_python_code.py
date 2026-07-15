#!/usr/bin/env python3
"""Generate Nature-style plotting code for the textbook figures."""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

from figure_catalog import FIGURES, figures_by_chapter


ROOT = Path(__file__).resolve().parents[1]
CODE_DIR = ROOT / "code"


PLOT_STYLE = r'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shared Nature-style plotting helpers for the textbook figures."""

from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(__file__).resolve().parents[1] / "tmp" / "matplotlib"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]

COLORS = {
    "blue": "#0072B2",
    "orange": "#D55E00",
    "green": "#009E73",
    "purple": "#CC79A7",
    "sky": "#56B4E9",
    "yellow": "#E69F00",
    "black": "#1A1A1A",
    "grey": "#7A7A7A",
    "light_grey": "#E6E6E6",
}

PALETTE = [
    COLORS["blue"],
    COLORS["orange"],
    COLORS["green"],
    COLORS["purple"],
    COLORS["yellow"],
    COLORS["sky"],
    COLORS["black"],
]


def apply_nature_style() -> None:
    plt.rcParams.update({
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
        "font.family": "DejaVu Sans",
        "font.size": 8.5,
        "axes.titlesize": 9.5,
        "axes.labelsize": 8.5,
        "xtick.labelsize": 7.5,
        "ytick.labelsize": 7.5,
        "legend.fontsize": 7.2,
        "axes.linewidth": 0.8,
        "lines.linewidth": 1.65,
        "lines.markersize": 4.2,
        "xtick.direction": "out",
        "ytick.direction": "out",
        "xtick.major.width": 0.7,
        "ytick.major.width": 0.7,
        "xtick.major.size": 3.0,
        "ytick.major.size": 3.0,
        "axes.prop_cycle": plt.cycler(color=PALETTE),
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })


def clean_axis(ax, grid: bool = False) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    if grid:
        ax.grid(True, color="#D9D9D9", lw=0.55, alpha=0.55)


def panel_label(ax, label: str) -> None:
    ax.text(
        -0.13,
        1.08,
        label,
        transform=ax.transAxes,
        fontsize=10,
        fontweight="bold",
        va="top",
        ha="left",
    )


def save_figure(fig, outdir: Path, filename: str) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    path = outdir / filename
    fig.savefig(path, dpi=320, bbox_inches="tight", pad_inches=0.035)
    plt.close(fig)
    print(f"saved {path.relative_to(ROOT)}")


def poisson_pmf(n: np.ndarray, mu: float) -> np.ndarray:
    import math

    return np.exp(-mu) * np.array([mu ** int(k) / math.factorial(int(k)) for k in n])


def j0_numeric(x: np.ndarray) -> np.ndarray:
    phi = np.linspace(0.0, 2.0 * np.pi, 1600)
    return np.mean(np.cos(np.outer(x, np.cos(phi))), axis=1)


def j1_numeric(x: np.ndarray) -> np.ndarray:
    phi = np.linspace(0.0, np.pi, 1600)
    return np.mean(np.cos(phi[None, :] - x[:, None] * np.sin(phi)[None, :]), axis=1)


def gaussian_visibility(u: np.ndarray, sigma: float) -> np.ndarray:
    return np.exp(-2.0 * (np.pi * sigma * u) ** 2)


def disk_visibility(x: np.ndarray) -> np.ndarray:
    y = np.ones_like(x)
    mask = np.abs(x) > 1e-8
    y[mask] = 2.0 * j1_numeric(x[mask]) / x[mask]
    return y
'''


PLOT_RECIPES = r'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Plot recipes for Nature-style textbook figures."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse

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


def ch01_photon_count_statistics(outdir: Path, filename: str) -> None:
    n = np.arange(0, 26)
    mu = 5.0
    poisson = poisson_pmf(n, mu)
    thermal = mu ** n / (1.0 + mu) ** (n + 1.0)
    sub = poisson_pmf(n, mu) * np.exp(-0.06 * (n - mu) ** 2)
    sub = sub / sub.sum()
    fig, ax = plt.subplots(figsize=(3.5, 2.45))
    ax.bar(n - 0.24, poisson, width=0.24, label="Poisson", color=COLORS["blue"])
    ax.bar(n, thermal, width=0.24, label="thermal", color=COLORS["orange"])
    ax.bar(n + 0.24, sub, width=0.24, label="sub-Poisson toy", color=COLORS["green"])
    ax.set(xlabel="photon count N", ylabel="P(N)")
    ax.legend(frameon=False)
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
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.35))
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


def ch05_vcz_visibility_models(outdir: Path, filename: str) -> None:
    u = np.linspace(0.0, 12.0, 700)
    fig, ax = plt.subplots(figsize=(3.55, 2.45))
    ax.plot(u, gaussian_visibility(u, 0.12) ** 2, label="Gaussian")
    ax.plot(u, np.cos(np.pi * 0.65 * u) ** 2, label="binary")
    ax.plot(u, j0_numeric(2 * np.pi * 0.17 * u) ** 2, label="thin ring")
    ax.set(xlabel=r"$u=B/\lambda$", ylabel=r"$|V|^2$")
    ax.legend(frameon=False)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch05_sii_signal_vs_baseline(outdir: Path, filename: str) -> None:
    baseline = np.linspace(0.0, 500.0, 650)
    wavelength = 500e-9
    c_inst = 0.02
    mas_to_rad = np.pi / (180 * 3600 * 1000)
    fig, ax = plt.subplots(figsize=(3.55, 2.45))
    for theta_mas in [0.2, 0.5, 1.0]:
        theta = theta_mas * mas_to_rad
        u = baseline / wavelength
        ax.plot(baseline, c_inst * np.exp(-(np.pi * theta * u) ** 2), label=fr"{theta_mas} mas")
    ax.set(xlabel="baseline B [m]", ylabel=r"$g^{(2)}_{12}(0)-1$")
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


def ch06_detector_timing_response(outdir: Path, filename: str) -> None:
    tau = np.linspace(-5, 5, 900)
    intrinsic = 0.35
    fig, ax = plt.subplots(figsize=(3.55, 2.45))
    for sigma_t in [0.0, 0.4, 0.8, 1.5]:
        sigma = np.sqrt(intrinsic ** 2 + sigma_t ** 2)
        ax.plot(tau, intrinsic / sigma * np.exp(-0.5 * (tau / sigma) ** 2), label=fr"$\sigma_t={sigma_t}$")
    ax.set(xlabel=r"delay $\tau$", ylabel=r"$g^{(2)}(\tau)-1$")
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


def ch07_poisson_likelihood(outdir: Path, filename: str) -> None:
    rng = np.random.default_rng(7)
    t = np.linspace(0, 30, 1200)
    rate = 2 + 18 * np.exp(-0.5 * ((t - 10) / 2.8) ** 2) + 8 * np.exp(-0.5 * ((t - 20) / 4.2) ** 2)
    dt = t[1] - t[0]
    events = np.repeat(t, rng.poisson(rate * dt))
    fig, axes = plt.subplots(2, 1, figsize=(4.1, 3.2), sharex=True)
    axes[0].plot(t, rate)
    axes[0].set(ylabel=r"$\lambda(t)$")
    axes[1].eventplot(events, lineoffsets=0, linelengths=0.8, colors=COLORS["black"])
    axes[1].set(xlabel="time", yticks=[], ylabel="events")
    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch07_covariance_matrix(outdir: Path, filename: str) -> None:
    rng = np.random.default_rng(71)
    n_tel = 7
    cov = 0.04 * rng.normal(size=(n_tel, n_tel))
    cov = (cov + cov.T) / 2
    for i in range(n_tel):
        cov[i, i] = 1.0
    cov[1, 4] = cov[4, 1] = 0.32
    cov[2, 5] = cov[5, 2] = 0.22
    fig, ax = plt.subplots(figsize=(3.15, 2.85))
    im = ax.imshow(cov, cmap="viridis", vmin=-0.1, vmax=1.0)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03, label="covariance")
    ax.set(xlabel="telescope", ylabel="telescope")
    clean_axis(ax)
    save_figure(fig, outdir, filename)


def ch07_fisher_scaling(outdir: Path, filename: str) -> None:
    n = np.logspace(2, 8, 500)
    fig, ax = plt.subplots(figsize=(3.55, 2.45))
    ax.loglog(n, 1 / np.sqrt(n), label="statistics only")
    ax.loglog(n, np.sqrt(1 / n + 2e-4 ** 2), label="with systematic floor")
    ax.set(xlabel="effective photon number", ylabel="parameter uncertainty")
    ax.legend(frameon=False)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch08_rayleigh_information(outdir: Path, filename: str) -> None:
    d = np.linspace(0.0, 3.0, 600)
    direct = d ** 2 / (1 + d ** 2)
    spade = np.ones_like(d) * 0.85
    fig, ax = plt.subplots(figsize=(3.55, 2.45))
    ax.plot(d, direct, label="direct imaging toy")
    ax.plot(d, spade, label="mode measurement toy")
    ax.axvline(1.0, color=COLORS["black"], lw=0.8, ls="--", label="Rayleigh scale")
    ax.set(xlabel=r"separation $d/\sigma$", ylabel="relative Fisher information", ylim=(-0.02, 1.05))
    ax.legend(frameon=False)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch08_spade_probabilities(outdir: Path, filename: str) -> None:
    d = np.linspace(0, 5, 600)
    lam = d ** 2 / 16
    fig, ax = plt.subplots(figsize=(3.55, 2.45))
    import math
    for n in range(4):
        ax.plot(d, np.exp(-lam) * lam ** n / math.factorial(n), label=fr"$p_{n}$")
    ax.set(xlabel=r"separation $d/\sigma$", ylabel="mode probability")
    ax.legend(frameon=False)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch08_cramer_rao_bound(outdir: Path, filename: str) -> None:
    n = np.logspace(1, 7, 500)
    floors = [0.0, 0.002, 0.01]
    fig, ax = plt.subplots(figsize=(3.55, 2.45))
    for floor in floors:
        ax.loglog(n, np.sqrt(1 / n + floor ** 2), label=fr"floor={floor:g}")
    ax.set(xlabel="events", ylabel=r"$\sqrt{\mathrm{Var}(\hat\theta)}$")
    ax.legend(frameon=False)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch09_radiation_g2_diagnostics(outdir: Path, filename: str) -> None:
    tau = np.linspace(-5, 5, 800)
    fig, ax = plt.subplots(figsize=(3.55, 2.45))
    ax.plot(tau, 1 + np.exp(-np.abs(tau)), label="thermal")
    ax.plot(tau, np.ones_like(tau), label="coherent")
    ax.plot(tau, 1 + 0.08 * np.cos(5 * tau) * np.exp(-np.abs(tau) / 2), label="maser toy")
    ax.set(xlabel=r"delay $\tau/\tau_c$", ylabel=r"$g^{(2)}(\tau)$")
    ax.legend(frameon=False)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch09_diagnostic_plane(outdir: Path, filename: str) -> None:
    labels = ["thermal", "synchrotron", "maser", "scattered", "line"]
    x = np.array([0.85, 0.55, 0.08, 0.35, 0.70])
    y = np.array([0.08, 0.55, 0.75, 0.25, 0.45])
    size = np.array([260, 180, 230, 160, 210])
    fig, ax = plt.subplots(figsize=(3.6, 2.8))
    ax.scatter(x, y, s=size, c=PALETTE[:5], alpha=0.78)
    for xi, yi, label in zip(x, y, labels):
        ax.text(xi + 0.02, yi + 0.02, label, fontsize=7.4)
    ax.set(xlabel=r"bunching contrast", ylabel="polarization fraction", xlim=(0, 1), ylim=(0, 1))
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch10_stellar_diameter_visibility(outdir: Path, filename: str) -> None:
    baseline = np.linspace(0, 850, 700)
    wavelength = 450e-9
    mas_to_rad = np.pi / (180 * 3600 * 1000)
    fig, ax = plt.subplots(figsize=(3.55, 2.45))
    for diameter in [0.1, 0.3, 0.8, 1.5]:
        theta = diameter * mas_to_rad
        u = baseline / wavelength
        ax.plot(baseline, np.exp(-(np.pi * theta * u) ** 2), label=fr"{diameter} mas")
    ax.set(xlabel="baseline B [m]", ylabel=r"$|V|^2$")
    ax.legend(frameon=False)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch10_binary_visibility(outdir: Path, filename: str) -> None:
    u = np.linspace(0, 18, 800)
    fig, ax = plt.subplots(figsize=(3.55, 2.45))
    for ratio in [1.0, 0.5, 0.2]:
        v = np.abs((1 + ratio * np.exp(-2j * np.pi * u * 0.45)) / (1 + ratio)) ** 2
        ax.plot(u, v, label=fr"flux ratio={ratio}")
    ax.set(xlabel=r"$u d$", ylabel=r"$|V|^2$")
    ax.legend(frameon=False)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch10_limb_darkening(outdir: Path, filename: str) -> None:
    r = np.linspace(0, 1, 500)
    fig, axes = plt.subplots(1, 2, figsize=(6.3, 2.35))
    for u_ld in [0.0, 0.4, 0.8]:
        intensity = 1 - u_ld * (1 - np.sqrt(1 - r ** 2))
        axes[0].plot(r, intensity, label=fr"$u={u_ld}$")
        x = np.linspace(0, 14, 500)
        axes[1].plot(x, np.abs(disk_visibility(x)) ** (2 - 0.35 * u_ld), label=fr"$u={u_ld}$")
    axes[0].set(xlabel="normalized radius", ylabel="surface brightness")
    axes[1].set(xlabel=r"$\pi\theta B/\lambda$", ylabel=r"$|V|^2$")
    for i, ax in enumerate(axes):
        panel_label(ax, "ab"[i])
        ax.legend(frameon=False)
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch11_stokes_qu_track(outdir: Path, filename: str) -> None:
    angle = np.linspace(0, np.pi, 500)
    q0, u0 = 0.6, 0.18
    q = q0 * np.cos(2 * angle) - u0 * np.sin(2 * angle)
    u = q0 * np.sin(2 * angle) + u0 * np.cos(2 * angle)
    fig, axes = plt.subplots(1, 2, figsize=(6.3, 2.45))
    axes[0].plot(np.degrees(angle), q, label="Q")
    axes[0].plot(np.degrees(angle), u, label="U")
    axes[0].set(xlabel="rotation angle [deg]", ylabel="Stokes parameter")
    axes[1].plot(q, u)
    axes[1].set(xlabel="Q", ylabel="U", aspect="equal")
    axes[0].legend(frameon=False)
    for i, ax in enumerate(axes):
        panel_label(ax, "ab"[i])
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch11_birefringence_energy(outdir: Path, filename: str) -> None:
    e = np.logspace(-1, 1.2, 500)
    fig, ax = plt.subplots(figsize=(3.55, 2.45))
    for scale in [1.0, 2.0, 4.0]:
        ax.semilogx(e, scale * np.log10(1 + e), label=fr"scale={scale}")
    ax.set(xlabel="photon energy [arb.]", ylabel="polarization angle rotation [deg]")
    ax.legend(frameon=False)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch12_photon_ring_visibility(outdir: Path, filename: str) -> None:
    ur = np.linspace(0, 12, 800)
    fig, ax = plt.subplots(figsize=(3.55, 2.45))
    ax.plot(ur, j0_numeric(2 * np.pi * ur) ** 2)
    ax.set(xlabel=r"$uR$", ylabel=r"$|V|^2$")
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch12_variability_autocorrelation(outdir: Path, filename: str) -> None:
    tau = np.linspace(0, 50, 500)
    fig, ax = plt.subplots(figsize=(3.55, 2.45))
    for tc in [3, 8, 20]:
        ax.plot(tau, np.exp(-tau / tc), label=fr"$t_c={tc}$")
    ax.set(xlabel="lag", ylabel="autocorrelation")
    ax.legend(frameon=False)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch13_transient_event_likelihood(outdir: Path, filename: str) -> None:
    rng = np.random.default_rng(13)
    t = np.linspace(0, 30, 1200)
    rate = 1.5 + 28 * np.exp(-(t - 8) / 6)
    rate[t < 8] = 1.5 + 28 * np.exp((t[t < 8] - 8) / 1.3)
    events = np.repeat(t, rng.poisson(rate * (t[1] - t[0])))
    fig, axes = plt.subplots(2, 1, figsize=(4.1, 3.2), sharex=True)
    axes[0].plot(t, rate)
    axes[0].set(ylabel=r"$\lambda(t)$")
    axes[1].eventplot(events, lineoffsets=0, linelengths=0.8, colors=COLORS["black"])
    axes[1].set(xlabel="time", ylabel="events", yticks=[])
    for ax in axes:
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch13_multimessenger_delay(outdir: Path, filename: str) -> None:
    channels = ["GW", "gamma", "optical", "radio"]
    t0 = np.array([0.0, 1.7, 11.2, 23.0])
    err = np.array([0.4, 0.2, 1.5, 4.0])
    fig, ax = plt.subplots(figsize=(3.8, 2.45))
    ax.errorbar(t0, np.arange(len(channels)), xerr=err, fmt="o", color=COLORS["blue"], ecolor=COLORS["grey"], capsize=2)
    ax.set(yticks=np.arange(len(channels)), yticklabels=channels, xlabel="arrival time relative to trigger")
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch14_dispersion_delay(outdir: Path, filename: str) -> None:
    nu = np.linspace(0.4, 2.0, 500)
    fig, ax = plt.subplots(figsize=(3.55, 2.45))
    for dm in [50, 300, 800]:
        ax.plot(nu, 4.15 * dm * (nu ** -2 - 2.0 ** -2), label=fr"DM={dm}")
    ax.set(xlabel=r"frequency $\nu$ [GHz]", ylabel="delay relative to 2 GHz [ms]")
    ax.legend(frameon=False)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch14_faraday_rotation(outdir: Path, filename: str) -> None:
    lam2 = np.linspace(0, 0.6, 500)
    fig, ax = plt.subplots(figsize=(3.55, 2.45))
    for rm in [10, 50, 150]:
        ax.plot(lam2, np.degrees(np.mod(rm * lam2, np.pi)), label=fr"RM={rm}")
    ax.set(xlabel=r"$\lambda^2$ [m$^2$]", ylabel="angle modulo pi [deg]")
    ax.legend(frameon=False)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch14_lensing_time_delay(outdir: Path, filename: str) -> None:
    x = np.linspace(-2.2, 2.2, 180)
    y = np.linspace(-2.2, 2.2, 180)
    xx, yy = np.meshgrid(x, y)
    beta_x, beta_y = 0.35, 0.0
    r = np.sqrt(xx ** 2 + yy ** 2 + 0.05 ** 2)
    phi = 0.5 * ((xx - beta_x) ** 2 + (yy - beta_y) ** 2) - np.log(r)
    fig, ax = plt.subplots(figsize=(3.35, 3.0))
    im = ax.contourf(xx, yy, phi, levels=24, cmap="viridis")
    ax.contour(xx, yy, phi, colors="white", linewidths=0.35, alpha=0.7)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.02, label="arrival-time surface")
    ax.set(xlabel=r"$\theta_x$", ylabel=r"$\theta_y$", aspect="equal")
    clean_axis(ax)
    save_figure(fig, outdir, filename)


def ch15_axion_conversion(outdir: Path, filename: str) -> None:
    length = np.linspace(0, 20, 800)
    fig, ax = plt.subplots(figsize=(3.55, 2.45))
    for g in [0.03, 0.06, 0.12]:
        p = (g * length) ** 2 * np.sinc(length / 8) ** 2
        ax.plot(length, np.clip(p, 0, 1), label=fr"$g={g}$")
    ax.set(xlabel="path length", ylabel="conversion probability")
    ax.legend(frameon=False)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch15_cosmic_birefringence(outdir: Path, filename: str) -> None:
    angle = np.linspace(0, np.pi / 3, 500)
    q0, u0 = 0.7, 0.0
    q = q0 * np.cos(2 * angle) - u0 * np.sin(2 * angle)
    u = q0 * np.sin(2 * angle) + u0 * np.cos(2 * angle)
    fig, ax = plt.subplots(figsize=(3.2, 3.0))
    ax.plot(q, u, color=COLORS["purple"])
    ax.scatter([q[0], q[-1]], [u[0], u[-1]], c=[COLORS["blue"], COLORS["orange"]], s=28)
    ax.set(xlabel="Q", ylabel="U", aspect="equal")
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch15_dark_matter_lensing(outdir: Path, filename: str) -> None:
    x = np.linspace(-2, 2, 500)
    smooth = 1 + 0.8 / (1 + (x / 0.55) ** 2)
    sub = smooth + 0.18 * np.exp(-0.5 * ((x - 0.65) / 0.08) ** 2)
    fig, ax = plt.subplots(figsize=(3.55, 2.45))
    ax.plot(x, smooth, label="smooth lens")
    ax.plot(x, sub, label="with small-scale clump")
    ax.set(xlabel="image coordinate", ylabel="relative magnification")
    ax.legend(frameon=False)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch16_cmb_power_spectrum(outdir: Path, filename: str) -> None:
    ell = np.arange(2, 2500)
    dl = 6000 * np.exp(-ell / 1800) * (
        1 + 2.1 * np.exp(-0.5 * ((ell - 220) / 70) ** 2)
        + 1.0 * np.exp(-0.5 * ((ell - 540) / 95) ** 2)
        + 0.55 * np.exp(-0.5 * ((ell - 820) / 120) ** 2)
    )
    fig, ax = plt.subplots(figsize=(3.75, 2.45))
    ax.plot(ell, dl)
    ax.set(xlabel=r"multipole $\ell$", ylabel=r"$D_\ell$ [arb.]")
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch16_birefringence_eb(outdir: Path, filename: str) -> None:
    alpha = np.linspace(-5, 5, 500)
    eb = np.sin(4 * np.radians(alpha))
    bb = np.sin(2 * np.radians(alpha)) ** 2
    fig, ax = plt.subplots(figsize=(3.55, 2.45))
    ax.plot(alpha, eb, label="EB leakage")
    ax.plot(alpha, bb, label="induced BB")
    ax.set(xlabel="polarization rotation [deg]", ylabel="relative signal")
    ax.legend(frameon=False)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch17_entanglement_resources(outdir: Path, filename: str) -> None:
    r_gamma = np.logspace(2, 9, 500)
    baseline = np.logspace(1, 7, 500)
    c = 299792458.0
    fig, axes = plt.subplots(1, 2, figsize=(6.4, 2.45))
    for eta in [1e-3, 1e-2, 1e-1]:
        axes[0].loglog(r_gamma, eta * r_gamma, label=fr"$\eta={eta:g}$")
    axes[0].set(xlabel=r"$R_\gamma$ [s$^{-1}$]", ylabel=r"$R_{\rm ent}$ [s$^{-1}$]")
    axes[1].loglog(baseline, baseline / c)
    axes[1].set(xlabel="baseline B [m]", ylabel=r"$T_{\rm mem}$ [s]")
    axes[0].legend(frameon=False)
    for i, ax in enumerate(axes):
        panel_label(ax, "ab"[i])
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch17_fidelity_distance(outdir: Path, filename: str) -> None:
    distance = np.linspace(0, 500, 500)
    fig, ax = plt.subplots(figsize=(3.55, 2.45))
    for loss in [0.002, 0.005, 0.01]:
        ax.plot(distance, np.exp(-loss * distance), label=fr"loss={loss}/km")
    ax.set(xlabel="link length [km]", ylabel="usable fidelity proxy")
    ax.legend(frameon=False)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch17_network_parameter_space(outdir: Path, filename: str) -> None:
    rate = np.logspace(1, 8, 180)
    memory = np.logspace(-7, 0, 180)
    rr, mm = np.meshgrid(rate, memory)
    score = np.log10(rr) + 0.8 * np.log10(mm + 1e-12)
    fig, ax = plt.subplots(figsize=(3.35, 2.85))
    im = ax.contourf(rate, memory, score, levels=20, cmap="magma")
    ax.set(xscale="log", yscale="log", xlabel=r"$R_{\rm ent}$ [s$^{-1}$]", ylabel=r"$T_{\rm mem}$ [s]")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03, label="resource score")
    clean_axis(ax)
    save_figure(fig, outdir, filename)


def ch18_photon_rate_magnitude(outdir: Path, filename: str) -> None:
    mag = np.linspace(0, 18, 500)
    fig, ax = plt.subplots(figsize=(3.55, 2.45))
    for area in [10, 100, 1000]:
        ax.semilogy(mag, 1e10 * area * 0.25 * 10 ** (-0.4 * mag), label=fr"{area} m$^2$")
    ax.set(xlabel=r"$m_{\rm AB}$", ylabel=r"$R_\gamma$ [arb. s$^{-1}$]")
    ax.legend(frameon=False)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch18_snr_heatmap(outdir: Path, filename: str) -> None:
    rate = np.logspace(3, 8, 160)
    tint = np.logspace(0, 5, 150)
    rr, tt = np.meshgrid(rate, tint)
    snr = 1e-5 * np.sqrt(rr * tt)
    fig, ax = plt.subplots(figsize=(3.35, 2.85))
    im = ax.contourf(rate, tint, snr, levels=22, cmap="viridis")
    ax.contour(rate, tint, snr, levels=[1, 3, 5, 10], colors="white", linewidths=0.5)
    ax.set(xscale="log", yscale="log", xlabel=r"$R_\gamma$ [s$^{-1}$]", ylabel="integration time [s]")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03, label="SNR")
    clean_axis(ax)
    save_figure(fig, outdir, filename)


def ch18_error_budget(outdir: Path, filename: str) -> None:
    labels = ["shot", "sky", "timing", "polarization", "model"]
    vals = np.array([1.0, 0.55, 0.35, 0.25, 0.45])
    fig, ax = plt.subplots(figsize=(3.65, 2.4))
    ax.bar(labels, vals, color=PALETTE[:5])
    ax.set(ylabel="relative error contribution")
    ax.tick_params(axis="x", rotation=25)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch19_science_case_feasibility(outdir: Path, filename: str) -> None:
    cases = {"hot stars": (1.0, 1e8), "Cepheids": (0.4, 2e7), "AGN": (0.05, 3e5), "SN Ia": (0.02, 2e4), "Eta Car": (0.8, 8e6)}
    fig, ax = plt.subplots(figsize=(3.65, 2.85))
    for i, (name, (theta, rate)) in enumerate(cases.items()):
        ax.scatter(theta, rate, s=58, color=PALETTE[i])
        ax.text(theta * 1.08, rate * 1.08, name, fontsize=7.2)
    ax.set(xscale="log", yscale="log", xlabel="angular scale [mas]", ylabel=r"$R_\gamma$ [arb.]")
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch19_priority_matrix(outdir: Path, filename: str) -> None:
    value = np.array([0.9, 0.7, 0.95, 0.5, 0.75])
    readiness = np.array([0.8, 0.65, 0.35, 0.9, 0.55])
    labels = ["SII stars", "Cepheids", "SN Ia", "lab HBT", "polarization"]
    fig, ax = plt.subplots(figsize=(3.5, 2.8))
    ax.scatter(readiness, value, s=90, color=PALETTE[:5])
    for x, y, label in zip(readiness, value, labels):
        ax.text(x + 0.02, y + 0.02, label, fontsize=7.2)
    ax.set(xlabel="technical readiness", ylabel="science value", xlim=(0, 1), ylim=(0, 1))
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch20_hbt_lab_histogram(outdir: Path, filename: str) -> None:
    rng = np.random.default_rng(20)
    tau = np.linspace(-8, 8, 160)
    true = 1 + 0.45 * np.exp(-0.5 * (tau / 1.2) ** 2)
    measured = rng.poisson(800 * true) / 800
    fig, ax = plt.subplots(figsize=(3.55, 2.45))
    ax.step(tau, measured, where="mid", label="simulated data")
    ax.plot(tau, true, color=COLORS["black"], label="input model")
    ax.set(xlabel=r"delay $\tau$ [ns]", ylabel=r"$g^{(2)}(\tau)$")
    ax.legend(frameon=False)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch20_event_table_simulation(outdir: Path, filename: str) -> None:
    rng = np.random.default_rng(200)
    t = np.linspace(0, 20, 800)
    rate = 8 + 5 * np.sin(2 * np.pi * t / 7) ** 2
    counts = rng.poisson(rate * (t[1] - t[0]))
    fig, axes = plt.subplots(1, 2, figsize=(6.2, 2.35))
    axes[0].plot(t, rate)
    axes[0].set(xlabel="time", ylabel="rate")
    axes[1].hist(np.repeat(t, counts), bins=48, color=COLORS["blue"])
    axes[1].set(xlabel="time", ylabel="events")
    for i, ax in enumerate(axes):
        panel_label(ax, "ab"[i])
        clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch20_spade_exercise(outdir: Path, filename: str) -> None:
    ch08_spade_probabilities(outdir, filename)


def ch21_g2_scaling_mistake(outdir: Path, filename: str) -> None:
    x = np.logspace(0, 5, 500)
    fig, ax = plt.subplots(figsize=(3.55, 2.45))
    for m in [1, 10, 100, 1000]:
        ax.loglog(x, 1 / (m * x), label=fr"$M={m}$")
    ax.set(xlabel=r"$\Delta t/\tau_c$", ylabel=r"$g^{(2)}(0)-1$")
    ax.legend(frameon=False)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch21_poisson_false_alarm(outdir: Path, filename: str) -> None:
    n = np.arange(0, 28)
    p = poisson_pmf(n, 8)
    fig, ax = plt.subplots(figsize=(3.55, 2.45))
    ax.bar(n, p, color=COLORS["blue"])
    ax.axvspan(16, 28, color=COLORS["orange"], alpha=0.22, label="tail events")
    ax.set(xlabel="count N", ylabel="P(N)")
    ax.legend(frameon=False)
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch22_roadmap_trade_space(outdir: Path, filename: str) -> None:
    labels = ["SII", "timing", "SN Ia", "network", "polarization", "lab"]
    readiness = np.array([0.85, 0.75, 0.45, 0.2, 0.55, 0.95])
    value = np.array([0.65, 0.6, 0.9, 0.85, 0.75, 0.35])
    cost = np.array([0.45, 0.35, 0.75, 0.95, 0.55, 0.1])
    fig, ax = plt.subplots(figsize=(3.7, 2.85))
    ax.scatter(readiness, value, s=360 * (0.2 + cost), color=PALETTE[:6], alpha=0.72)
    for x, y, label in zip(readiness, value, labels):
        ax.text(x + 0.015, y + 0.015, label, fontsize=7.2)
    ax.set(xlabel="technical readiness", ylabel="science return", xlim=(0, 1.05), ylim=(0, 1.05))
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


def ch22_program_timeline(outdir: Path, filename: str) -> None:
    tasks = [("lab HBT", 2026, 2027.2), ("detectors", 2026.5, 2029), ("stellar SII", 2028, 2032), ("transients", 2030, 2035), ("network pathfinder", 2032, 2040)]
    fig, ax = plt.subplots(figsize=(4.1, 2.65))
    for i, (label, start, end) in enumerate(tasks):
        ax.barh(i, end - start, left=start, height=0.46, color=PALETTE[i % len(PALETTE)])
        ax.text(start + 0.08, i, label, va="center", ha="left", color="white", fontsize=7.3)
    ax.set(yticks=[], xlabel="year", xlim=(2026, 2041))
    clean_axis(ax, grid=True)
    save_figure(fig, outdir, filename)


RECIPES = {
    "ch01_fourier_visibility.pdf": ch01_fourier_visibility,
    "ch01_photon_count_statistics.pdf": ch01_photon_count_statistics,
    "ch01_resolution_baseline.pdf": ch01_resolution_baseline,
    "ch02_mean_intensity_vs_correlation.pdf": ch02_mean_intensity_vs_correlation,
    "ch02_event_table_information.pdf": ch02_event_table_information,
    "ch03_phase_space_states.pdf": ch03_phase_space_states,
    "ch03_coherence_time_dilution.pdf": ch03_coherence_time_dilution,
    "ch04_mandel_q_g2.pdf": ch04_mandel_q_g2,
    "ch04_siegert_relation.pdf": ch04_siegert_relation,
    "ch04_factorial_moments.pdf": ch04_factorial_moments,
    "ch05_vcz_visibility_models.pdf": ch05_vcz_visibility_models,
    "ch05_sii_signal_vs_baseline.pdf": ch05_sii_signal_vs_baseline,
    "ch05_uv_coverage.pdf": ch05_uv_coverage,
    "ch06_detector_timing_response.pdf": ch06_detector_timing_response,
    "ch06_deadtime_saturation.pdf": ch06_deadtime_saturation,
    "ch07_poisson_likelihood.pdf": ch07_poisson_likelihood,
    "ch07_covariance_matrix.pdf": ch07_covariance_matrix,
    "ch07_fisher_scaling.pdf": ch07_fisher_scaling,
    "ch08_rayleigh_information.pdf": ch08_rayleigh_information,
    "ch08_spade_probabilities.pdf": ch08_spade_probabilities,
    "ch08_cramer_rao_bound.pdf": ch08_cramer_rao_bound,
    "ch09_radiation_g2_diagnostics.pdf": ch09_radiation_g2_diagnostics,
    "ch09_diagnostic_plane.pdf": ch09_diagnostic_plane,
    "ch10_stellar_diameter_visibility.pdf": ch10_stellar_diameter_visibility,
    "ch10_binary_visibility.pdf": ch10_binary_visibility,
    "ch10_limb_darkening.pdf": ch10_limb_darkening,
    "ch11_stokes_qu_track.pdf": ch11_stokes_qu_track,
    "ch11_birefringence_energy.pdf": ch11_birefringence_energy,
    "ch12_photon_ring_visibility.pdf": ch12_photon_ring_visibility,
    "ch12_variability_autocorrelation.pdf": ch12_variability_autocorrelation,
    "ch13_transient_event_likelihood.pdf": ch13_transient_event_likelihood,
    "ch13_multimessenger_delay.pdf": ch13_multimessenger_delay,
    "ch14_dispersion_delay.pdf": ch14_dispersion_delay,
    "ch14_faraday_rotation.pdf": ch14_faraday_rotation,
    "ch14_lensing_time_delay.pdf": ch14_lensing_time_delay,
    "ch15_axion_conversion.pdf": ch15_axion_conversion,
    "ch15_cosmic_birefringence.pdf": ch15_cosmic_birefringence,
    "ch15_dark_matter_lensing.pdf": ch15_dark_matter_lensing,
    "ch16_cmb_power_spectrum.pdf": ch16_cmb_power_spectrum,
    "ch16_birefringence_eb.pdf": ch16_birefringence_eb,
    "ch17_entanglement_resources.pdf": ch17_entanglement_resources,
    "ch17_fidelity_distance.pdf": ch17_fidelity_distance,
    "ch17_network_parameter_space.pdf": ch17_network_parameter_space,
    "ch18_photon_rate_magnitude.pdf": ch18_photon_rate_magnitude,
    "ch18_snr_heatmap.pdf": ch18_snr_heatmap,
    "ch18_error_budget.pdf": ch18_error_budget,
    "ch19_science_case_feasibility.pdf": ch19_science_case_feasibility,
    "ch19_priority_matrix.pdf": ch19_priority_matrix,
    "ch20_hbt_lab_histogram.pdf": ch20_hbt_lab_histogram,
    "ch20_event_table_simulation.pdf": ch20_event_table_simulation,
    "ch20_spade_exercise.pdf": ch20_spade_exercise,
    "ch21_g2_scaling_mistake.pdf": ch21_g2_scaling_mistake,
    "ch21_poisson_false_alarm.pdf": ch21_poisson_false_alarm,
    "ch22_roadmap_trade_space.pdf": ch22_roadmap_trade_space,
    "ch22_program_timeline.pdf": ch22_program_timeline,
}
'''


CHAPTER_HEADER = r'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第 {chapter:02d} 章图像脚本

运行方式：
    python code/chapter_{chapter:02d}.py

输出目录：
    figures/generated/chapter_{chapter:02d}/

备注：
    本脚本只生成本章需要的公式图。每张图的注释说明它对应的公式族、
    变量含义和阅读方式。默认参数用于展示标度关系，不代表某一次真实观测。
"""

from __future__ import annotations

from pathlib import Path

from plot_recipes import draw_figure
from plot_style import ROOT


OUTDIR = ROOT / "figures" / "generated" / "chapter_{chapter:02d}"


def main() -> None:
'''


def chapter_script(chapter: int, figures: list[dict[str, object]]) -> str:
    lines = [CHAPTER_HEADER.format(chapter=chapter).rstrip()]
    for idx, figure in enumerate(figures, start=1):
        filename = str(figure["filename"])
        caption = str(figure["caption"])
        lines.extend([
            "",
            f"    # 图 {idx}: {caption}",
            f"    # 输出文件: figures/generated/chapter_{chapter:02d}/{filename}",
            f"    draw_figure({filename!r}, OUTDIR)",
        ])
    lines.extend([
        "",
        "",
        'if __name__ == "__main__":',
        "    main()",
        "",
    ])
    return "\n".join(lines)


def readme() -> str:
    total = len(FIGURES)
    return f"""# Chapter Plotting Code

This directory contains one Python plotting script per chapter.

Run one chapter:

```bash
python code/chapter_01.py
```

Run all chapters:

```bash
for f in code/chapter_*.py; do python \"$f\"; done
```

Each chapter script may generate more than one figure. The current catalog
contains {total} generated figures. Output is written to:

```text
figures/generated/chapter_XX/
```

The default numerical values are teaching values for scaling and interpretation.
Replace them with instrument, catalog, or paper-specific values before treating
a plot as a research result.
"""


def main() -> int:
    CODE_DIR.mkdir(exist_ok=True)
    (CODE_DIR / "plot_style.py").write_text(PLOT_STYLE, encoding="utf-8")
    (CODE_DIR / "plot_recipes.py").write_text(PLOT_RECIPES, encoding="utf-8")
    by_chapter = figures_by_chapter()
    for chapter in range(1, 23):
        figures = by_chapter.get(chapter, [])
        (CODE_DIR / f"chapter_{chapter:02d}.py").write_text(chapter_script(chapter, figures), encoding="utf-8")
    (CODE_DIR / "README.md").write_text(readme(), encoding="utf-8")
    metadata = ROOT / "metadata"
    metadata.mkdir(exist_ok=True)
    (metadata / "figure_catalog.json").write_text(json.dumps(FIGURES, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(by_chapter)} chapter scripts and {len(FIGURES)} figure recipes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
