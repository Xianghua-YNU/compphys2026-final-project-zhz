"""
==========================================================
preprocess.py

Kepler Light Curve 数据预处理模块

功能：
    1. 读取FITS
    2. 提取TIME和FLUX
    3. QUALITY筛选
    4. 删除NaN
    5. 3σ异常值剔除
    6. 去均值
    7. 返回统计信息

Author : Orion Lee
==========================================================
"""

import numpy as np
from astropy.io import fits


# ==========================================================
# 读取并预处理FITS
# ==========================================================

def preprocess_fits(filename):
    """
    Parameters
    ----------
    filename : str
        FITS文件路径

    Returns
    -------
    time : ndarray
        观测时间（day）

    flux : ndarray
        去均值后的光变数据

    info : dict
        数据统计信息
    """

    print("Reading :", filename)

    # ------------------------------------------------------
    # 打开FITS
    # ------------------------------------------------------

    hdul = fits.open(filename)

    data = hdul[1].data

    # ------------------------------------------------------
    # TIME
    # ------------------------------------------------------

    time = np.array(data["TIME"], dtype=float)

    # ------------------------------------------------------
    # Flux
    # 优先使用PDCSAP_FLUX
    # ------------------------------------------------------

    if "PDCSAP_FLUX" in data.names:

        flux = np.array(
            data["PDCSAP_FLUX"],
            dtype=float
        )

        flux_name = "PDCSAP_FLUX"

    else:

        flux = np.array(
            data["SAP_FLUX"],
            dtype=float
        )

        flux_name = "SAP_FLUX"

    # ------------------------------------------------------
    # QUALITY
    # ------------------------------------------------------

    if "QUALITY" in data.names:

        quality = np.array(
            data["QUALITY"]
        )

    else:

        quality = np.zeros(len(time))

    hdul.close()

    # ======================================================
    # 删除NaN
    # ======================================================

    mask = (
        np.isfinite(time)
        &
        np.isfinite(flux)
    )

    time = time[mask]
    flux = flux[mask]
    quality = quality[mask]

    print("After NaN removal :", len(time))

    # ======================================================
    # QUALITY筛选
    # ======================================================

    mask = (quality == 0)

    time = time[mask]
    flux = flux[mask]

    print("After QUALITY filter :", len(time))

    # ======================================================
    # 3σ异常值剔除
    # ======================================================

    mean = np.mean(flux)

    std = np.std(flux)

    mask = np.abs(flux - mean) < 3 * std

    time = time[mask]
    flux = flux[mask]

    print("After 3σ clipping :", len(time))

    # ======================================================
    # 去均值
    # ======================================================

    flux_mean = np.mean(flux)

    flux = flux - flux_mean

    # ======================================================
    # 数据统计
    # ======================================================

    baseline = time.max() - time.min()

    cadence = np.median(
        np.diff(time)
    )

    info = {

        "baseline": baseline,

        "cadence": cadence,

        "npoints": len(time),

        "flux_type": flux_name,

        "mean_flux": flux_mean,

        "std_flux": np.std(flux)

    }

    # ======================================================
    # 输出信息
    # ======================================================

    print("---------------------------------------")
    print("Flux Type :", flux_name)
    print("Data Points :", info["npoints"])
    print("Baseline :", baseline, "day")
    print("Cadence :", cadence, "day")
    print("---------------------------------------")

    return time, flux, info