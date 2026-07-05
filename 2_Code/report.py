"""
==========================================================
report.py

RR Lyrae Analysis Report Module

功能
----------------------------------------------------------
1. 保存所有图片
2. 保存CSV结果
3. 保存TXT分析报告

Author : Orion Lee
==========================================================
"""

import os
import csv

from plot import (
    plot_lightcurve,
    plot_lomb_scargle,
    plot_fft,
    plot_phase,
    plot_summary
)


# ==========================================================
# 保存全部图片
# ==========================================================

def save_figures(
        target,
        output_dir,
        time,
        flux,
        ls_result,
        fft_result,
        phase_result
):

    target_dir = os.path.join(output_dir, target)

    os.makedirs(target_dir, exist_ok=True)

    # ------------------------------------------------------
    # Light Curve
    # ------------------------------------------------------

    fig = plot_lightcurve(
        time,
        flux,
        target
    )

    fig.savefig(
        os.path.join(
            target_dir,
            "LightCurve.png"
        ),
        dpi=300,
        bbox_inches="tight"
    )

    fig.clf()


    # ------------------------------------------------------
    # Lomb–Scargle
    # ------------------------------------------------------

    fig = plot_lomb_scargle(
        ls_result
    )

    fig.savefig(
        os.path.join(
            target_dir,
            "LombScargle.png"
        ),
        dpi=300,
        bbox_inches="tight"
    )

    fig.clf()


    # ------------------------------------------------------
    # FFT
    # ------------------------------------------------------

    fig = plot_fft(
        fft_result
    )

    fig.savefig(
        os.path.join(
            target_dir,
            "FFT.png"
        ),
        dpi=300,
        bbox_inches="tight"
    )

    fig.clf()


    # ------------------------------------------------------
    # Phase Folding
    # ------------------------------------------------------

    fig = plot_phase(
        phase_result
    )

    fig.savefig(
        os.path.join(
            target_dir,
            "Phase.png"
        ),
        dpi=300,
        bbox_inches="tight"
    )

    fig.clf()


    # ------------------------------------------------------
    # Summary Figure
    # ------------------------------------------------------

    fig = plot_summary(
        target,
        time,
        flux,
        ls_result,
        fft_result,
        phase_result
    )

    fig.savefig(
        os.path.join(
            target_dir,
            "Summary.png"
        ),
        dpi=300,
        bbox_inches="tight"
    )

    fig.clf()


# ==========================================================
# 保存CSV
# ==========================================================

def save_csv(
        output_dir,
        all_results
):

    if len(all_results) == 0:
        return

    filename = os.path.join(
        output_dir,
        "Result.csv"
    )

    keys = list(all_results[0].keys())

    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=keys
        )

        writer.writeheader()

        writer.writerows(
            all_results
        )

    print("CSV Saved :", filename)


# ==========================================================
# 保存TXT报告
# ==========================================================

def save_report(
        target,
        output_dir,
        result
):

    target_dir = os.path.join(
        output_dir,
        target
    )

    os.makedirs(
        target_dir,
        exist_ok=True
    )

    filename = os.path.join(
        target_dir,
        "Report.txt"
    )

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as f:

        f.write("="*60 + "\n")
        f.write("RR Lyrae Automatic Analysis Report\n")
        f.write("="*60 + "\n\n")

        for key, value in result.items():

            f.write(
                f"{key:<25}: {value}\n"
            )

        f.write("\n")

        f.write("="*60 + "\n")

        f.write("Generated automatically by RR Lyrae Pipeline.\n")

    print("TXT Report Saved :", filename)

