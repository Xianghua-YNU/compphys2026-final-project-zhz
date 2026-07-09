# 2_Code/ - 源代码目录

**目的**: 存放所有用于模拟、分析和可视化的代码。代码的质量是评分的重要组成部分。

### **结构原则：**
本项目**不强制要求固定文件名**，但必须遵循**逻辑解耦**的原则。建议按照以下功能模块划分您的代码：

1.  **入口模块** (如 `main.py`): 负责设置物理参数、初始化环境、调用算法并启动流程。
2.  **物理/算法模块** (如 `solvers.py` 或 `physics.py`): 实现核心数值算法（如 RK4, Metropolis, PINN 损失函数等）。应保持独立性，不包含绘图逻辑。
3.  **分析与可视化** (如 `analysis.py` 或 `plot_utils.py`): 负责处理原始数据、计算物理量（如能量偏差、关联函数）并生成论文所需的图表。

### **必需文件：**
- **`README.md` (本文件)**: 必须清晰说明：
    - 每个代码文件的功能。
    - 如何配置环境 (`pip install -r requirements.txt`)。
    - **如何运行主程序**以得到论文中的结果。
- **`requirements.txt`**: 项目依赖清单。

### **代码规范要求：**
- **物理注释**: 必须对核心物理方程和算法步骤进行注释。
- **参数化设计**: 物理参数应集中定义，严禁在循环中出现“魔法数字”。
- **AI 声明**: 若使用 AI 辅助编写，需在代码中注明。


# 一、项目简介

本项目基于 **Kepler 光变曲线 FITS 数据**，实现 RR Lyrae 变星的自动周期分析。

程序主要完成以下功能：

- 自动读取 FITS 光变数据
- 数据预处理
- Lomb–Scargle 周期分析
- FFT 周期分析
- Phase Folding（相位折叠）
- 自动绘制分析图像
- 自动生成 CSV 统计结果
- 自动生成 TXT 分析报告

整个分析流程如下：

```
读取 FITS 数据
        │
        ▼
数据预处理
        │
        ▼
Lomb–Scargle 周期分析
        │
        ├────────► FFT 分析
        │
        ▼
Phase Folding
        │
        ▼
生成图片
        │
        ▼
生成 CSV
        │
        ▼
生成 TXT 报告
```

---

# 二、项目目录

```
Project/
│
├── main.py
├── preprocess.py
├── lomb_scargle.py
├── fft_analysis.py
├── phase_fold.py
├── plot.py
├── report.py
├── utils.py
│
├── *.fits
│
├── output/
│
├── requirements.txt
└── README.md
```

---

# 三、各代码文件功能说明

## 1. main.py

主程序。

负责整个分析流程的调度，包括：

- 搜索所有 FITS 文件
- 数据预处理
- Lomb–Scargle 周期分析
- FFT 分析
- Phase Folding
- 保存图片
- 保存 CSV
- 保存 TXT 报告

整个程序由 main.py 控制运行。

---

## 2. preprocess.py

数据预处理模块。

主要功能：

- 读取 FITS 文件
- 删除 NaN 数据
- 删除异常数据
- 获取时间序列
- 获取 Flux
- 统计观测跨度
- 统计数据点数量

输出：

- time
- flux
- observation information

---

## 3. lomb_scargle.py

Lomb–Scargle 周期分析模块。

主要功能：

- 建立频率搜索网格
- 计算 Lomb–Scargle 功率谱
- 搜索最大功率峰
- 计算最佳周期
- 计算 False Alarm Probability (FAP)
- 估计周期误差
- 计算信噪比（SNR）

输出：

- 最佳周期
- 功率谱
- FAP
- 周期误差

---

## 4. fft_analysis.py

FFT 周期分析模块。

主要功能：

- 插值均匀采样
- FFT 计算
- 搜索频率峰值
- 计算最佳周期

主要用于与 Lomb–Scargle 进行结果比较。

---

## 5. phase_fold.py

相位折叠模块。

主要功能：

- 根据最佳周期计算相位
- 排序相位
- 拼接两个周期
- 为绘制 Phase Folding 图做准备

---

## 6. plot.py

绘图模块。

负责绘制：

- Light Curve
- Lomb–Scargle 功率谱
- FFT 功率谱
- Phase Folding 图
- Summary 综合图

所有函数均返回 Figure，由 report.py 统一保存。

---

## 7. report.py

结果输出模块。

负责：

- 保存 PNG 图片
- 保存 Result.csv
- 保存 Report.txt

统一管理所有输出文件。

---

## 8. utils.py

工具模块。

负责一些公共函数，例如：

- 创建输出目录
- 文件路径处理
- 通用辅助函数