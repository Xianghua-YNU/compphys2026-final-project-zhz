import os
import glob

from preprocess import preprocess_fits
from lomb_scargle import lomb_scargle_analysis
from fft_analysis import fft_analysis
from phase_fold import phase_fold
from report import (
    save_figures,
    save_csv,
    save_report,
)

from utils import (
    make_output_folder,
)

# ==========================================================
# 参数设置
# ==========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 工程根目录(Project)
PROJECT_DIR = os.path.dirname(BASE_DIR)

# 数据目录
DATA_DIR = os.path.join(PROJECT_DIR, "3_Data")


# 输出目录
OUTPUT_DIR = os.path.join(PROJECT_DIR, "output")

MIN_PERIOD = 0.2
MAX_PERIOD = 1.0

LITERATURE_PERIOD = None

# ==========================================================
# 建立输出目录
# ==========================================================

make_output_folder(OUTPUT_DIR)

# ==========================================================
# 搜索所有fits
# ==========================================================

fits_files = sorted(glob.glob(os.path.join(DATA_DIR, "*.fits")))

if len(fits_files) == 0:
    print("No FITS files found!")
    exit()

print("=" * 60)
print("RR Lyrae Automatic Analysis Pipeline")
print("Number of targets :", len(fits_files))
print("=" * 60)

# 保存所有目标结果
all_results = []

# ==========================================================
# 循环分析
# ==========================================================

for filename in fits_files:

    target = os.path.splitext(os.path.basename(filename))[0]

    print()
    print("=" * 60)
    print("Target :", target)
    print("=" * 60)

    # ------------------------------------------------------
    # 数据预处理
    # ------------------------------------------------------

    time, flux, info = preprocess_fits(filename)

    # ------------------------------------------------------
    # Lomb-Scargle
    # ------------------------------------------------------

    ls_result = lomb_scargle_analysis(
        time,
        flux,
        min_period=MIN_PERIOD,
        max_period=MAX_PERIOD
    )

    # ------------------------------------------------------
    # FFT
    # ------------------------------------------------------

    fft_result = fft_analysis(
        time,
        flux,
        min_period=MIN_PERIOD,
        max_period=MAX_PERIOD
    )

    # ------------------------------------------------------
    # Phase Folding
    # ------------------------------------------------------

    phase_result = phase_fold(
        time,
        flux,
        ls_result["best_period"]
    )

    # ------------------------------------------------------
    # 保存图片
    # ------------------------------------------------------

    save_figures(
        target,
        OUTPUT_DIR,
        time,
        flux,
        ls_result,
        fft_result,
        phase_result
    )

    # ------------------------------------------------------
    # 结果保存
    # ------------------------------------------------------

    result = {

        "Target": target,

        "Observation Span (day)":
            info["baseline"],

        "Data Points":
            info["npoints"],

        "LS Period":
            ls_result["best_period"],

        "FFT Period":
            fft_result["best_period"],

        "Difference":
            abs(
                ls_result["best_period"]
                -
                fft_result["best_period"]
            ),

        "Max Power":
            ls_result["max_power"],

        "FAP":
            ls_result["fap"],

        "Period Error":
            ls_result["period_error"]

    }

    # 文献比较
    if LITERATURE_PERIOD is not None:

        result["Literature"] = LITERATURE_PERIOD

        result["Relative Error (%)"] = (
            abs(
                ls_result["best_period"]
                - LITERATURE_PERIOD
            )
            /
            LITERATURE_PERIOD
            * 100
        )

    all_results.append(result)

    # ------------------------------------------------------
    # TXT报告
    # ------------------------------------------------------

    save_report(
        target,
        OUTPUT_DIR,
        result
    )

    # ------------------------------------------------------
    # 屏幕输出
    # ------------------------------------------------------

    print(f"Best LS Period : {ls_result['best_period']:.8f} day")

    print(f"Best FFT Period: {fft_result['best_period']:.8f} day")

    print(f"Max Power      : {ls_result['max_power']:.5f}")

    print(f"FAP            : {ls_result['fap']:.3e}")

    print(f"Period Error   : {ls_result['period_error']:.8f} day")

# ==========================================================
# 保存CSV
# ==========================================================

save_csv(
    OUTPUT_DIR,
    all_results
)

print()
print("=" * 60)
print("Analysis Finished.")
print(f"Results saved to : {OUTPUT_DIR}")
print("=" * 60)