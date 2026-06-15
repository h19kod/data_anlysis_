# 🇮🇶 Iraq World Development Indicators Analysis
## تحليل مؤشرات التنمية العالمية للعراق

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Jupyter-Notebook-orange?logo=jupyter" alt="Jupyter">
  <img src="https://img.shields.io/badge/Pandas-Data%20Analysis-green?logo=pandas" alt="Pandas">
  <img src="https://img.shields.io/badge/Data%20Source-World%20Bank-blue" alt="World Bank">
</p>

<p align="center">
  <b>Professional Data Analysis Project | مشروع تحليل بيانات احترافي</b><br>
  <i>Comprehensive analysis of Iraq's socioeconomic trajectory (1960-2025)</i><br>
  <i>تحليل شامل للمسار الاقتصادي والاجتماعي للعراق (1960-2025)</i>
</p>

---

## 📋 Table of Contents | فهرس المحتويات

1. [Project Overview | نظرة عامة على المشروع](#-project-overview--نظرة-عامة-على-المشروع)
2. [Data Source | مصدر البيانات](#-data-source--مصدر-البيانات)
3. [Methodology | المنهجية](#-methodology--المنهجية)
4. [Key Findings | النتائج الرئيسية](#-key-findings--النتائج-الرئيسية)
5. [Project Structure | هيكل المشروع](#-project-structure--هيكل-المشروع)
6. [Installation & Usage | التثبيت والاستخدام](#-installation--usage--التثبيت-والاستخدام)
7. [Results & Deliverables | النتائج والمخرجات](#-results--deliverables--النتائج-والمخرجات)
8. [Future Work | العمل المستقبلي](#-future-work--العمل-المستقبلي)
9. [Author | المؤلف](#-author--المؤلف)

---

## 🎯 Project Overview | نظرة عامة على المشروع

### English
This project presents a **comprehensive data analysis** of Iraq's World Development Indicators (WDI) from the World Bank, covering **66 years (1960-2025)**. The analysis explores how decades of conflict, sanctions, and political instability have shaped Iraq's socioeconomic trajectory through rigorous data cleaning, exploratory analysis, feature engineering, and baseline modeling.

### العربية
يقدم هذا المشروع **تحليلاً شاملاً** لمؤشرات التنمية العالمية (WDI) للعراق من البنك الدولي، covering **66 عاماً (1960-2025)**. يستكشف التحليل كيف شكّلت عقود من الصراعات والعقوبات والت instability السياسي المسار الاقتصادي والاجتماعي للعراق من خلال تنظيف بيانات صارم، وتحليل استكشافي، وهندسة متغيرات، ونمذجة أساسية.

### Key Metrics | المؤشرات الرئيسية
- 📊 **1,486** total indicators | مؤشر إجمالي
- ✅ **1,334** indicators after cleaning | مؤشر بعد التنظيف
- 📅 **66** years of data | سنة من البيانات
- 🔢 **34,175** engineered observations | ملاحظة مهندسة
- 📈 **38.8%** data completeness | نسبة اكتمال البيانات

---

## 📊 Data Source | مصدر البيانات

**Source | المصدر:** World Bank Open Data Portal | بوابة البيانات المفتوحة للبنك الدولي  
**Dataset | مجموعة البيانات:** Iraq World Development Indicators (WDI) | مؤشرات التنمية العالمية للعراق  
**URL:** https://data.worldbank.org/country/IRQ  
**Date | التاريخ:** June 2025 | يونيو 2025

### Files Included | الملفات المرفقة
```
API_IRQ_DS2_en_csv_v2_16712/
├── API_IRQ_DS2_en_csv_v2_16712.csv          # Main data | البيانات الرئيسية
├── Metadata_Country_API_IRQ_DS2_en_csv_v2_16712.csv    # Country metadata | بيانات الدولة الوصفية
└── Metadata_Indicator_API_IRQ_DS2_en_csv_v2_16712.csv    # Indicator metadata | بيانات المؤشرات الوصفية
```

---

## 🔬 Methodology | المنهجية

The analysis follows a structured **6-step pipeline** | التحليل يتبع **خط أنابيب من 6 خطوات**:

```
┌─────────────────────────────────────────────────────────────────┐
│  1. Problem Definition (Ask)                                    │
│     └─ Define business problem & analytical objectives          │
├─────────────────────────────────────────────────────────────────┤
│  2. Data Collection (Prepare)                                   │
│     └─ Import, verify, and profile raw data                      │
├─────────────────────────────────────────────────────────────────┤
│  3. Data Cleaning (Process)                                   │
│     └─ Remove duplicates, handle missing values, standardize,    │
│        detect & cap outliers                                     │
├─────────────────────────────────────────────────────────────────┤
│  4. Data Analysis (Analyze)                                     │
│     └─ EDA, feature engineering, modeling, evaluation            │
├─────────────────────────────────────────────────────────────────┤
│  5. Data Visualization (Share)                                  │
│     └─ Document visualization strategy for stakeholders        │
├─────────────────────────────────────────────────────────────────┤
│  6. Reporting & Action (Act)                                    │
│     └─ Executive summary, recommendations, next steps          │
└─────────────────────────────────────────────────────────────────┘
```

### Analytical Techniques | التقنيات التحليلية

| Technique | التقنية | Purpose | الغرض |
|-----------|---------|---------|-------|
| **IQR Outlier Detection** | كشف القيم الشاذة | Identify and cap statistical outliers | تحديد وحصر القيم الشاذة إحصائياً |
| **Long-format Transformation** | التحويل للتنسيق الطويل | Enable time-series analysis | تمكين تحليل السلاسل الزمنية |
| **Feature Engineering** | هندسة المتغيرات | Create lag, growth, decade features | إنشاء متغيرات التأخر والنمو والعقد |
| **Linear Regression** | الانحدار الخطي | Model long-term trends | نمذجة الاتجاهات طويلة المدى |
| **Nearest-Centroid** | أقرب وسيط | Classify historical eras | تصنيف الفترات التاريخية |
| **Naive Forecasting** | التنبؤ البسيط | Baseline prediction | التنبؤ الأساسي |

---

## 🔍 Key Findings | النتائج الرئيسية

### 1. Demographic Resilience | الصمود الديموغرافي 🇮🇶

Despite **4 decades of conflict**, Iraq shows remarkable demographic resilience:

| Indicator | المؤشر | 1960 | 2024 | Growth | النمو | R² |
|-----------|--------|------|------|--------|-------|-----|
| **Population** | السكان | 7.0M | 46.0M | **+556%** | +598K/year | 0.955 |
| **Life Expectancy** | متوسط العمر | 51.5 yrs | 72.4 yrs | **+41%** | +0.24 yr/year | 0.806 |

> **Insight | رؤية:** Both indicators show highly predictable trends despite wars, suggesting strong demographic momentum.

### 2. Economic Volatility | التقلب الاقتصادي 📉📈

GDP and trade show extreme volatility tied to oil prices and conflicts:

| Indicator | المؤشر | 1960 | 2024 | Growth | MAPE |
|-----------|--------|------|------|--------|------|
| **GDP** | الناتج المحلي | $1.5B | $280B | +18,000% | 921% |
| **Exports** | الصادرات | $1.2B | $105B | +8,500% | 259,241% |

> **Insight | رؤية:** Linear models fail for economic indicators; regime-switching approaches required.

### 3. Historical Signatures in Data | التوقيعات التاريخية في البيانات 🔍

- **Era Classification Accuracy | دقة تصنيف الفترات:** 81.8%
- **Best Distinguished | الأفضل تمييزاً:** Pre-Iran War (100%), Iran-Iraq War (86%)
- **Most Confused | الأكثر تشابهاً:** Sanctions Era / Post-Invasion

> **Insight | رؤية:** Macroeconomic indicators alone can distinguish Iraq's historical periods with high accuracy.

### 4. Data Quality Progress | تطور جودة البيانات 📊

- **Data Coverage Improvement | تحسن التغطية:** 200 → 900+ indicators after 2000
- **Peak Year | أغنى سنة:** 2018 (903 indicators)
- **Completeness | الاكتمال:** 38.8% (typical for WDI datasets)

---

## 📁 Project Structure | هيكل المشروع

```
data_anlysis/
│
├── 📓 data_analysis.ipynb              # Main analysis notebook | دفتر التحليل الرئيسي
├── 📓 data_analysis_executed.ipynb     # Executed notebook with outputs | الدفتر المنفذ بالمخرجات
├── 📄 README.md                        # This file | هذا الملف
│
├── 📂 API_IRQ_DS2_en_csv_v2_16712/     # Raw data folder | مجلد البيانات الخام
│   ├── API_IRQ_DS2_en_csv_v2_16712.csv
│   ├── Metadata_Country_API_IRQ_DS2_en_csv_v2_16712.csv
│   └── Metadata_Indicator_API_IRQ_DS2_en_csv_v2_16712.csv
│
└── 📂 outputs/                         # Generated outputs | المخرجات المولدة
    ├── 📊 visualizations/              # Charts & plots | الرسوم البيانية
    ├── 📈 reports/                     # Analysis reports | تقارير التحليل
    └── 💾 processed_data/                # Cleaned datasets | مجموعات البيانات المنظفة
```

---

## 🚀 Installation & Usage | التثبيت والاستخدام

### Prerequisites | المتطلبات الأساسية
```bash
# Python 3.7+ required
python --version
```

### Dependencies | التبعيات
```bash
pip install pandas numpy jupyter
```

### Optional (for advanced modeling) | اختياري (للنمذجة المتقدمة)
```bash
pip install scikit-learn statsmodels matplotlib seaborn plotly
```

### Running the Analysis | تشغيل التحليل

```bash
# Clone the repository | استنساخ المستودع
git clone https://github.com/h19kod/data_anlysis_.git
cd data_anlysis_

# Launch Jupyter Notebook | تشغيل Jupyter Notebook
jupyter notebook data_analysis.ipynb

# Or run all cells and save output | أو تشغيل جميع الخلايا وحفظ المخرجات
jupyter nbconvert --to notebook --execute data_analysis.ipynb --output data_analysis_executed.ipynb
```

---

## 📊 Results & Deliverables | النتائج والمخرجات

### Cleaned Datasets | مجموعات البيانات المنظفة

| Dataset | الشكل | Description | الوصف |
|---------|-------|-------------|-------|
| `df` | (1,334, 71) | Wide-format cleaned data | بيانات منظفة بالتنسيق الواسع |
| `df_long` | (34,175, 22) | Long-format with engineered features | بالتنسيق الطويل مع المتغيرات المهندسة |

### Engineered Features | المتغيرات المهندسة

**Time-Based | الزمنية:**
- `decade` — Decade bucket (1960, 1970, ...)
- `period` — 6 historical bins
- `iraq_era` — 7 contextual periods (Pre-Iran War → Post-ISIS)

**Lag & Growth | التأخر والنمو:**
- `lag_1`, `lag_3`, `lag_5` — Previous values
- `yoy_growth` — Year-over-year % change
- `cagr_3yr`, `cagr_5yr` — Compound annual growth rates
- `rolling_5yr` — 5-year moving average

**Decade Aggregates | مجاميع العقد:**
- `decade_mean`, `decade_std` — Summary statistics
- `decade_count`, `decade_rank` — Positional features

### Model Performance | أداء النماذج

| Model | النموذج | Target | الهدف | Metric | المقياس | Value | القيمة |
|-------|---------|--------|-------|--------|---------|-------|--------|
| Linear Trend | الاتجاه الخطي | Population | السكان | R² | 0.955 |
| Linear Trend | الاتجاه الخطي | Life Expectancy | متوسط العمر | R² | 0.806 |
| Era Classifier | مصنف الفترات | Historical Era | الفترة التاريخية | Accuracy | الدقة | 81.8% |
| Naive Forecast | التنبؤ البسيط | Population | السكان | MAPE | 5.62% |

---

## 🔮 Future Work | العمل المستقبلي

1. **Advanced Modeling | نماذج متقدمة:**
   - ARIMA/Prophet for time-series forecasting
   - XGBoost/Random Forest for classification
   - Markov-Switching models for regime-aware GDP forecasting

2. **External Data Integration | دمج بيانات خارجية:**
   - Oil price data (Brent crude)
   - Conflict intensity indices (UCDP/PRIO)
   - Sanctions dummy variables

3. **Interactive Dashboard | لوحة تحكم تفاعلية:**
   - Plotly/Dash web application
   - Real-time indicator monitoring
   - Historical period comparison tool

4. **Regional Comparison | المقارنة الإقليمية:**
   - Extend analysis to other MENA countries
   - Cross-country correlation analysis
   - Regional development benchmarking

5. **Publication | النشر:**
   - Publish cleaned datasets
   - Academic paper submission
   - Policy brief for Iraqi government

---

## 👨‍💻 Author | المؤلف

**h19kod**

- GitHub: [@h19kod](https://github.com/h19kod)
- Repository: [data_anlysis_](https://github.com/h19kod/data_anlysis_)

---

## 📜 License | الترخيص

This project is available for educational and research purposes. The raw data is sourced from the World Bank Open Data Portal and is subject to their terms of use.

---

## 🙏 Acknowledgments | الشكر والتقدير

- **World Bank** for providing open access to development indicators
- **Jupyter Project** for the interactive computing environment
- **Pandas Team** for the powerful data manipulation library

---

<p align="center">
  <b>⭐ Star this repository if you found it useful!</b><br>
  <b>⭐ نجّم هذا المستودع إذا وجدته مفيداً!</b>
</p>

<p align="center">
  <i>Made with ❤️ for Iraq's development | صُنع بحبٍ من أجل تنمية العراق</i>
</p>
