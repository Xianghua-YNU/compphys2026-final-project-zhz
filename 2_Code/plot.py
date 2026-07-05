"""
==========================================================
plot.py

RR Lyrae Analysis Plot Module

功能
----------------------------------------------------------
1. Light Curve
2. Lomb–Scargle Periodogram
3. FFT Spectrum
4. Phase Folding（第二部分）
5. Summary Figure（第二部分）

Author : Orion Lee
==========================================================
"""

import matplotlib.pyplot as plt
import numpy as np


# ==========================================================
# 绘图风格
# ==========================================================

plt.rcParams["figure.dpi"] = 120
plt.rcParams["savefig.dpi"] = 300

plt.rcParams["font.size"] = 12
plt.rcParams["axes.labelsize"] = 12
plt.rcParams["axes.titlesize"] = 13

plt.rcParams["xtick.direction"] = "in"
plt.rcParams["ytick.direction"] = "in"

plt.rcParams["axes.grid"] = True


# ==========================================================
# Light Curve
# ==========================================================

def plot_lightcurve(
        time,
        flux,
        target
):

    fig, ax = plt.subplots(
        figsize=(10,4)
    )

    ax.scatter(
        time,
        flux,
        s=3,
        color="black",
        alpha=0.7
    )

    ax.set_xlabel("Time (day)")
    ax.set_ylabel("Normalized Flux")

    ax.set_title(target)

    return fig


# ==========================================================
# Lomb–Scargle
# ==========================================================

def plot_lomb_scargle(
        ls_result
):

    fig, ax = plt.subplots(
        figsize=(8,5)
    )

    ax.plot(
        ls_result["period"],
        ls_result["power"],
        color="black",
        lw=1
    )

    ax.axvline(
        ls_result["best_period"],
        color="red",
        linestyle="--",
        linewidth=2,
        label=f"P = {ls_result['best_period']:.6f} d"
    )

    ax.scatter(
        ls_result["best_period"],
        ls_result["max_power"],
        color="red",
        zorder=5
    )

    ax.set_xlabel("Period (day)")
    ax.set_ylabel("Power")

    ax.set_title("Lomb–Scargle Periodogram")

    ax.legend()

    return fig


# ==========================================================
# FFT
# ==========================================================

def plot_fft(
        fft_result
):

    fig, ax = plt.subplots(
        figsize=(8,5)
    )

    ax.plot(
        fft_result["period"],
        fft_result["power"],
        color="black",
        lw=1
    )

    ax.axvline(
        fft_result["best_period"],
        color="red",
        linestyle="--",
        linewidth=2,
        label=f"P = {fft_result['best_period']:.6f} d"
    )

    ax.scatter(
        fft_result["best_period"],
        fft_result["max_power"],
        color="red",
        zorder=5
    )

    ax.set_xlabel("Period (day)")
    ax.set_ylabel("Power")

    ax.set_title("FFT Spectrum")

    ax.legend()

    return fig

# ==========================================================
# Phase Folding
# ==========================================================

def plot_phase(phase_result):

    fig, ax = plt.subplots(figsize=(8,5))

    # 双周期散点
    ax.scatter(
        phase_result["phase2"],
        phase_result["flux2"],
        s=4,
        color="black",
        alpha=0.45,
        label="Observation"
    )

    # 第一周期平均曲线
    ax.errorbar(
        phase_result["bin_center"],
        phase_result["bin_mean"],
        yerr=phase_result["bin_std"],
        fmt="o-",
        color="red",
        markersize=4,
        linewidth=2,
        capsize=2,
        label="Mean"
    )

    # 第二周期平均曲线
    ax.errorbar(
        phase_result["bin_center"] + 1,
        phase_result["bin_mean"],
        yerr=phase_result["bin_std"],
        fmt="o-",
        color="red",
        markersize=4,
        linewidth=2,
        capsize=2
    )

    ax.set_xlim(0,2)

    ax.set_xlabel("Phase")
    ax.set_ylabel("Normalized Flux")

    ax.set_title(
        f"Phase Folding (P={phase_result['period']:.6f} d)"
    )

    ax.legend()

    return fig


# ==========================================================
# Summary Figure (2×2)
# ==========================================================

def plot_summary(
        target,
        time,
        flux,
        ls_result,
        fft_result,
        phase_result
):

    fig, axes = plt.subplots(
        2,
        2,
        figsize=(12,8)
    )

    # ------------------------------------------------------
    # Light Curve
    # ------------------------------------------------------

    ax = axes[0,0]

    ax.scatter(
        time,
        flux,
        s=2,
        color="black"
    )

    ax.set_title("Light Curve")

    ax.set_xlabel("Time (day)")
    ax.set_ylabel("Flux")


    # ------------------------------------------------------
    # Lomb–Scargle
    # ------------------------------------------------------

    ax = axes[0,1]

    ax.plot(
        ls_result["period"],
        ls_result["power"],
        color="black"
    )

    ax.axvline(
        ls_result["best_period"],
        color="red",
        linestyle="--"
    )

    ax.set_title("Lomb–Scargle")

    ax.set_xlabel("Period (day)")
    ax.set_ylabel("Power")


    # ------------------------------------------------------
    # FFT
    # ------------------------------------------------------

    ax = axes[1,0]

    ax.plot(
        fft_result["period"],
        fft_result["power"],
        color="black"
    )

    ax.axvline(
        fft_result["best_period"],
        color="red",
        linestyle="--"
    )

    ax.set_title("FFT")

    ax.set_xlabel("Period (day)")
    ax.set_ylabel("Power")


    # ------------------------------------------------------
    # Phase Folding
    # ------------------------------------------------------

    ax = axes[1,1]

    ax.scatter(
        phase_result["phase2"],
        phase_result["flux2"],
        s=2,
        color="black",
        alpha=0.45
    )

    ax.plot(
        phase_result["bin_center"],
        phase_result["bin_mean"],
        color="red",
        linewidth=2
    )

    ax.plot(
        phase_result["bin_center"] + 1,
        phase_result["bin_mean"],
        color="red",
        linewidth=2
    )

    ax.set_xlim(0,2)

    ax.set_title("Phase Folding")

    ax.set_xlabel("Phase")
    ax.set_ylabel("Flux")


    fig.suptitle(
        target,
        fontsize=16
    )

    fig.tight_layout()

    return fig