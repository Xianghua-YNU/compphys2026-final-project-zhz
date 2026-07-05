"""
==========================================================
utils.py

公共工具模块

功能
----------------------------------------------------------
1. 创建输出目录
2. 打印标题
3. 相对误差
4. RMS
5. SNR
6. Scatter
7. 统计信息
8. 设置Matplotlib风格

Author : Orion Lee
==========================================================
"""

import os
import numpy as np
import matplotlib.pyplot as plt


# ==========================================================
# 创建输出目录
# ==========================================================

def make_output_folder(output_dir):

    os.makedirs(output_dir, exist_ok=True)


# ==========================================================
# 打印标题
# ==========================================================

def print_title(title):

    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


# ==========================================================
# 相对误差(%)
# ==========================================================

def relative_error(measured, reference):

    if reference == 0:
        return np.nan

    return abs(measured-reference)/reference*100


# ==========================================================
# RMSE
# ==========================================================

def rmse(x):

    x = np.asarray(x)

    return np.sqrt(np.mean(x**2))


# ==========================================================
# 信噪比
# ==========================================================

def calculate_snr(signal):

    signal = np.asarray(signal)

    background = np.median(signal)

    if background == 0:
        return np.nan

    return np.max(signal)/background


# ==========================================================
# Phase Scatter
# ==========================================================

def phase_scatter(std_flux):

    std_flux = np.asarray(std_flux)

    return np.nanmean(std_flux)


# ==========================================================
# 数据统计
# ==========================================================

def observation_information(time):

    time = np.asarray(time)

    baseline = time.max()-time.min()

    cadence = np.median(np.diff(time))

    npoints = len(time)

    return {

        "baseline": baseline,

        "cadence": cadence,

        "npoints": npoints

    }


# ==========================================================
# Matplotlib统一风格
# ==========================================================

def set_plot_style():

    plt.rcParams["figure.dpi"] = 120

    plt.rcParams["savefig.dpi"] = 300

    plt.rcParams["font.size"] = 12

    plt.rcParams["axes.labelsize"] = 12

    plt.rcParams["axes.titlesize"] = 13

    plt.rcParams["legend.fontsize"] = 10

    plt.rcParams["xtick.direction"] = "in"

    plt.rcParams["ytick.direction"] = "in"

    plt.rcParams["axes.grid"] = True


# ==========================================================
# 打印分析结果
# ==========================================================

def print_summary(result):

    print()

    print("-"*45)

    for key,value in result.items():

        print(f"{key:<20}: {value}")

    print("-"*45)


# ==========================================================
# 判断是否RR Lyrae
# ==========================================================

def classify_rrlyrae(period):

    if 0.2 <= period <= 1.0:

        return "Possible RR Lyrae"

    elif period < 0.2:

        return "Too Short"

    else:

        return "Long Period Variable"