"""
==========================================================
lomb_scargle.py

Lomb–Scargle 周期分析

功能

1. 建立频率网格
2. 计算功率谱
3. 寻找最高峰
4. 计算最佳周期
5. False Alarm Probability
6. 周期误差估计
7. 返回完整结果

Author : Orion Lee
==========================================================
"""

import numpy as np
from astropy.timeseries import LombScargle


# ==========================================================
# Lomb–Scargle分析
# ==========================================================

def lomb_scargle_analysis(
        time,
        flux,
        min_period=0.2,
        max_period=1.0,
        oversampling=10
):
    """
    Parameters
    ----------
    time : ndarray

    flux : ndarray

    min_period : float
        最短搜索周期(day)

    max_period : float
        最长搜索周期(day)

    oversampling : int
        频率过采样倍率

    Returns
    -------
    dict
    """

    print()

    print("Running Lomb-Scargle ...")

    # ======================================================
    # 时间跨度
    # ======================================================

    baseline = time.max() - time.min()

    # ======================================================
    # 频率范围
    # ======================================================

    minimum_frequency = 1.0 / max_period

    maximum_frequency = 1.0 / min_period

    # ======================================================
    # 频率分辨率
    #
    # Δf≈1/T
    #
    # 为了更高精度
    # 使用oversampling
    # ======================================================

    df = 1.0 / baseline / oversampling

    frequency = np.arange(
        minimum_frequency,
        maximum_frequency,
        df
    )

    print("Frequency Grid :", len(frequency))

    # ======================================================
    # Lomb–Scargle
    # ======================================================

    ls = LombScargle(time, flux)

    power = ls.power(frequency)

    # ======================================================
    # 最大峰
    # ======================================================

    peak = np.argmax(power)

    best_frequency = frequency[peak]

    best_period = 1.0 / best_frequency

    max_power = power[peak]

    # ======================================================
    # False Alarm Probability
    # ======================================================

    try:

        fap = ls.false_alarm_probability(
            max_power
        )

    except Exception:

        fap = np.nan

    # ======================================================
    # 半高宽估计周期误差
    # ======================================================

    half = max_power / 2

    index = np.where(
        power >= half
    )[0]

    if len(index) >= 2:

        width = (
            frequency[index[-1]]
            -
            frequency[index[0]]
        )

        period_error = width / (best_frequency ** 2)

    else:

        period_error = np.nan

    # ======================================================
    # 信噪比(SNR)
    # ======================================================

    background = np.median(power)

    snr = max_power / background

    # ======================================================
    # 输出
    # ======================================================

    print("------------------------------------------")

    print("Best Frequency :", best_frequency)

    print("Best Period    :", best_period)

    print("Maximum Power  :", max_power)

    print("SNR            :", snr)

    print("FAP            :", fap)

    print("Period Error   :", period_error)

    print("------------------------------------------")

    # ======================================================
    # 返回
    # ======================================================

    result = {

        "frequency": frequency,

        "period": 1.0 / frequency,

        "power": power,

        "best_frequency": best_frequency,

        "best_period": best_period,

        "max_power": max_power,

        "period_error": period_error,

        "snr": snr,

        "fap": fap,

        "ls_object": ls

    }

    return result