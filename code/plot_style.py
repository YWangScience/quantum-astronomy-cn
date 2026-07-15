#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shared Nature-style plotting helpers for the textbook figures."""

from __future__ import annotations

import os
from pathlib import Path

_MPLCONFIGDIR = Path(__file__).resolve().parents[1] / "tmp" / "matplotlib"
_MPLCONFIGDIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(_MPLCONFIGDIR))

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
        0.028,
        0.965,
        label,
        transform=ax.transAxes,
        fontsize=9.0,
        fontweight="bold",
        va="top",
        ha="left",
        clip_on=True,
        zorder=20,
        bbox=dict(
            facecolor="white",
            edgecolor="none",
            alpha=0.86,
            boxstyle="round,pad=0.13,rounding_size=0.02",
        ),
    )


def save_figure(fig, outdir: Path, filename: str) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    path = outdir / filename
    fig.savefig(path, dpi=320, bbox_inches="tight", pad_inches=0.055)
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
