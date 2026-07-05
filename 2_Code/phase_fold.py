"""
==========================================================
phase_fold.py

Phase Folding 相位折叠模块

功能
----------------------------------------------------------
1. 相位计算
2. 数据排序
3. 双周期展开
4. Phase Bin统计
5. RMS计算
6. Scatter计算

Author : Orion Lee
==========================================================
"""

import numpy as np


# ==========================================================
# Phase Folding
# ==========================================================

def phase_fold(
        time,
        flux,
        period,
        nbins=50
):
    """
    Parameters
    ----------
    time : ndarray

    flux : ndarray

    period : float

    nbins : int
        相位Bin数量

    Returns
    -------
    result : dict
    """

    print()
    print("Running Phase Folding ...")

    # ======================================================
    # Phase
    # ======================================================

    phase = (time / period) % 1.0

    # ======================================================
    # 排序
    # ======================================================

    order = np.argsort(phase)

    phase = phase[order]

    flux = flux[order]

    # ======================================================
    # 双周期
    # ======================================================

    phase2 = np.concatenate(
        [phase, phase + 1]
    )

    flux2 = np.concatenate(
        [flux, flux]
    )

    # ======================================================
    # Phase Bin
    # ======================================================

    bins = np.linspace(
        0,
        1,
        nbins + 1
    )

    center = 0.5 * (
        bins[:-1] + bins[1:]
    )

    mean_flux = np.zeros(nbins)

    std_flux = np.zeros(nbins)

    number = np.zeros(nbins, dtype=int)

    # ======================================================
    # 每个Bin统计
    # ======================================================

    for i in range(nbins):

        mask = (
            (phase >= bins[i])
            &
            (phase < bins[i + 1])
        )

        if np.sum(mask) > 0:

            mean_flux[i] = np.mean(
                flux[mask]
            )

            std_flux[i] = np.std(
                flux[mask]
            )

            number[i] = np.sum(mask)

        else:

            mean_flux[i] = np.nan

            std_flux[i] = np.nan

            number[i] = 0

    # ======================================================
    # RMS
    # ======================================================

    rms = np.sqrt(
        np.mean(
            flux ** 2
        )
    )

    # ======================================================
    # Scatter
    # ======================================================

    scatter = np.nanmean(
        std_flux
    )

    # ======================================================
    # 输出
    # ======================================================

    print("------------------------------------------")

    print("Period       :", period)

    print("Phase Points :", len(phase))

    print("RMS          :", rms)

    print("Scatter      :", scatter)

    print("------------------------------------------")

    # ======================================================
    # 返回
    # ======================================================

    result = {

        "period": period,

        "phase": phase,

        "flux": flux,

        "phase2": phase2,

        "flux2": flux2,

        "bin_center": center,

        "bin_mean": mean_flux,

        "bin_std": std_flux,

        "bin_number": number,

        "rms": rms,

        "scatter": scatter

    }

    return result