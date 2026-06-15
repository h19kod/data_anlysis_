# Project Overview | نظرة عامة على المشروع

## Project Structure | هيكل المشروع

```
iraq-wdi-analysis/
│
├── 📁 src/                          # Source code | شيفرة المصدر
│   ├── __init__.py                  # Package initialization
│   ├── data_loader.py               # Load raw data | تحميل البيانات الخام
│   ├── data_cleaner.py              # Clean and preprocess | التنظيف والمعالجة
│   ├── feature_engineer.py          # Feature engineering | هندسة المتغيرات
│   ├── models.py                    # Baseline models | النماذج الأساسية
│   └── utils.py                     # Utility functions | الأدوات المساعدة
│
├── 📁 tests/                        # Unit tests | الاختبارات
│   ├── __init__.py
│   ├── test_data_loader.py
│   ├── test_data_cleaner.py
│   └── test_feature_engineer.py
│
├── 📁 docs/                         # Documentation | الوثائق
│   └── PROJECT_OVERVIEW.md          # This file | هذا الملف
│
├── 📁 outputs/                      # Generated outputs | المخرجات
│   ├── visualizations/              # Charts and plots | الرسوم البيانية
│   ├── reports/                     # Analysis reports | التقارير
│   └── processed_data/              # Cleaned datasets | البيانات المنظفة
│
├── 📁 API_IRQ_DS2_en_csv_v2_16712/  # Raw data | البيانات الخام
│   ├── API_IRQ_DS2_en_csv_v2_16712.csv
│   ├── Metadata_Country_API_IRQ_DS2_en_csv_v2_16712.csv
│   └── Metadata_Indicator_API_IRQ_DS2_en_csv_v2_16712.csv
│
├── 📓 data_analysis.ipynb           # Main notebook (EN) | الدفتر الرئيسي (إنجليزي)
├── 📓 data_analysis_executed.ipynb  # Executed notebook | الدفتر المنفذ
├── 📄 README.md                     # Main documentation | الوثائق الرئيسية
├── 📄 requirements.txt              # Dependencies | التبعيات
├── 📄 .gitignore                    # Git ignore rules | قواعد تجاهل Git
└── 📄 LICENSE                       # License file | ملف الترخيص (إذا وجد)
```

## Module Descriptions | وصف الوحدات

### 1. data_loader.py | محمل البيانات
**Purpose:** Load raw CSV files from the World Bank  
**Class:** `DataLoader`  
**Key Methods:**
- `load_all()` - Load all three data files
- `_load_main_data()` - Load main indicators data
- `_load_country_meta()` - Load country metadata
- `_load_indicator_meta()` - Load indicator metadata
- `validate_data()` - Validate loaded data structure

### 2. data_cleaner.py | منظف البيانات
**Purpose:** Clean and preprocess raw data  
**Class:** `DataCleaner`  
**Pipeline:**
1. Remove duplicates
2. Drop empty indicators
3. Standardize formats
4. Cap outliers (IQR method)

**Key Methods:**
- `clean_all()` - Run full cleaning pipeline
- `_remove_duplicates()` - Remove duplicate rows
- `_handle_missing_values()` - Drop empty indicators
- `_standardize_formats()` - Clean text and numeric columns
- `_cap_outliers()` - Detect and cap outliers

### 3. feature_engineer.py | مهندس المتغيرات
**Purpose:** Create engineered features for modeling  
**Class:** `FeatureEngineer`  
**Features Created:**

**Time-Based | الزمنية:**
- `decade` - Decade bucket (1960, 1970, ...)
- `period` - 6 historical bins
- `iraq_era` - 7 contextual periods

**Lag & Growth | التأخر والنمو:**
- `lag_1`, `lag_3`, `lag_5` - Previous values
- `yoy_growth` - Year-over-year % change
- `cagr_3yr`, `cagr_5yr` - Compound growth rates
- `rolling_5yr` - 5-year moving average

**Decade Aggregates | مجاميع العقد:**
- `decade_mean`, `decade_std` - Summary statistics
- `decade_count`, `decade_rank` - Positional features

### 4. models.py | النماذج
**Purpose:** Baseline modeling and evaluation  
**Classes:**

**TrendModel | نموذج الاتجاه:**
- Simple linear regression using least squares
- Formula: `value = slope * year + intercept`
- Returns: R², slope, intercept, MAPE, direction

**EraClassifier | مصنف الفترات:**
- Nearest-centroid classification
- Features: GDP, Exports, Imports, Population
- Target: Iraq's 7 historical eras
- Returns: Overall and per-class accuracy

**NaiveForecaster | المتنبئ البسيط:**
- Moving average forecast
- Evaluates: MAPE, RMSE
- Suitable for stable indicators

### 5. utils.py | الأدوات المساعدة
**Purpose:** Utility functions  
**Functions:**
- `get_project_root()` - Get project root path
- `setup_logging()` - Configure logging
- `ensure_dir()` - Create directories
- `format_number()` - Format numbers with commas
- `format_percentage()` - Format as percentage
- `save_results()` - Save to multiple formats
- `ProgressTracker` - Track long operations

## Usage Examples | أمثلة الاستخدام

### Basic Pipeline | خط الأنابيب الأساسي

```python
from src.data_loader import DataLoader
from src.data_cleaner import DataCleaner
from src.feature_engineer import FeatureEngineer
from src.models import TrendModel, EraClassifier

# 1. Load data
loader = DataLoader()
df, df_country, df_indicator = loader.load_all()

# 2. Clean data
cleaner = DataCleaner(df)
df_clean = cleaner.clean_all()

# 3. Engineer features
engineer = FeatureEngineer(df_clean)
df_long = engineer.engineer_all()

# 4. Model trends
trend_model = TrendModel()
key_indicators = ["SP.POP.TOTL", "SP.DYN.LE00.IN", "NY.GDP.MKTP.CD"]
results = trend_model.fit(df_long, key_indicators)

# 5. Classify eras
classifier = EraClassifier()
accuracy = classifier.fit(df_long)
```

### Running Tests | تشغيل الاختبارات

```bash
# Run all tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_data_loader.py

# Run with verbose output
python -m pytest tests/ -v
```

### Using the Notebook | استخدام الدفتر

```bash
# Launch Jupyter
jupyter notebook data_analysis.ipynb

# Run all cells
jupyter nbconvert --to notebook --execute data_analysis.ipynb
```

## Data Flow | تدفق البيانات

```
Raw CSV Files (1,486 indicators)
        ↓
DataLoader.load_all()
        ↓
Wide DataFrame (1,486 × 71)
        ↓
DataCleaner.clean_all()
        ↓
Cleaned DataFrame (1,334 × 71)
        ↓
FeatureEngineer.engineer_all()
        ↓
Long DataFrame (34,175 × 22)
        ↓
Models.fit() / predict()
        ↓
Results & Evaluation
```

## Development Guidelines | إرشادات التطوير

### Adding New Features | إضافة متغيرات جديدة

1. Edit `src/feature_engineer.py`
2. Add method: `_create_new_feature()`
3. Call it in `engineer_all()`
4. Update `get_feature_summary()`
5. Add test in `tests/test_feature_engineer.py`

### Adding New Models | إضافة نماذج جديدة

1. Create class in `src/models.py`
2. Implement `fit()` and `predict()` methods
3. Add evaluation metrics
4. Add test in `tests/`
5. Document in README.md

### Code Style | أسلوب الكود

- Follow PEP 8
- Use type hints
- Write docstrings for all public methods
- Add comments in Arabic for key sections
- Keep functions focused and small

## Troubleshooting | حل المشكلات

### Issue: ModuleNotFoundError
**Solution:** Ensure `src/` is in Python path
```python
import sys
sys.path.insert(0, 'src')
```

### Issue: Data file not found
**Solution:** Check data directory structure
```python
from src.utils import get_project_root
print(get_project_root())
```

### Issue: Memory error on large datasets
**Solution:** Process in chunks or use sampling
```python
df_sample = df.sample(n=1000, random_state=42)
```

## References | المراجع

- World Bank WDI Documentation: https://data.worldbank.org/indicator
- Pandas Documentation: https://pandas.pydata.org/docs/
- Scikit-learn Documentation: https://scikit-learn.org/stable/

---

**Last Updated | آخر تحديث:** June 2025  
**Version | الإصدار:** 1.0.0
