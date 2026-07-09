"""
==========================================================
fft_analysis.py

FFT周期分析模块

功能
----------------------------------------------------------
1. 将非均匀采样插值到均匀采样
2. FFT计算
3. 功率谱计算
4. 自动寻找主峰
5. 周期计算
6. 峰宽估计
7. SNR计算
8. 返回完整结果

Author : Orion Lee
==========================================================
"""

import numpy as np
from scipy.fft import fft
from scipy.fft import fftfreq


# ==========================================================
# FFT分析
# ==========================================================

def fft_analysis(
        time,
        flux,
        min_period=0.2,
        max_period=1.0
):

    print()
    print("Running FFT ...")

    # ======================================================
    # 中位采样间隔
    # ======================================================

    dt = np.median(np.diff(time))

    # ======================================================
    # 建立均匀时间序列
    # ======================================================

    uniform_time = np.arange(
        time.min(),
        time.max(),
        dt
    )

    # ======================================================
    # 线性插值
    # ======================================================

    uniform_flux = np.interp(
        uniform_time,
        time,
        flux
    )

    # ======================================================
    # FFT
    # ======================================================

    N = len(uniform_flux)

    fft_result = fft(uniform_flux)

    frequency = fftfreq(
        N,
        d=dt
    )

    # ======================================================
    # 保留正频率
    # ======================================================

    positive = frequency > 0

    frequency = frequency[positive]

    power = np.abs(
        fft_result[positive]
    ) ** 2

    # ======================================================
    # 周期
    # ======================================================

    period = 1.0 / frequency

    # ======================================================
    # 限制周期范围
    # ======================================================

    mask = (
        (period >= min_period)
        &
        (period <= max_period)
    )

    frequency = frequency[mask]

    period = period[mask]

    power = power[mask]

    # ======================================================
    # 主峰
    # ======================================================

    peak = np.argmax(power)

    best_frequency = frequency[peak]

    best_period = period[peak]

    max_power = power[peak]

    # ======================================================
    # 半高宽估计
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

        period_error = width / (
            best_frequency ** 2
        )

    else:

        period_error = np.nan

    # ======================================================
    # SNR
    # ======================================================

    background = np.median(power)

    snr = max_power / background

    # ======================================================
    # 输出
    # ======================================================

    print("------------------------------------------")
    print("Sampling Interval :", dt)
    print("FFT Points        :", N)
    print("Best Frequency    :", best_frequency)
    print("Best Period       :", best_period)
    print("Maximum Power     :", max_power)
    print("SNR               :", snr)
    print("Period Error      :", period_error)
    print("------------------------------------------")

    # ======================================================
    # 返回
    # ======================================================

    result = {

        "uniform_time": uniform_time,

        "uniform_flux": uniform_flux,

        "frequency": frequency,

        "period": period,

        "power": power,

        "best_frequency": best_frequency,

        "best_period": best_period,

        "max_power": max_power,

        "snr": snr,

        "period_error": period_error,

        "sampling_interval": dt,

        "fft_points": N

    }

    return result