# FeatureEngineer API Documentation
## وثائق API: مهندس المتغيرات

## Class: FeatureEngineer

### Description | الوصف
Creates time-based, lag, growth, and decade aggregate features for modeling.

### Constructor | الباني

```python
FeatureEngineer(df: pd.DataFrame)
```

**Parameters:**
- `df` (pd.DataFrame): Cleaned wide-format dataframe

### Attributes
- `df_wide` (pd.DataFrame): Copy of wide-format dataframe
- `year_cols` (List[str]): List of year column names
- `df_long` (Optional[pd.DataFrame]): Long-format dataframe with features

### Methods

#### engineer_all()
Run complete feature engineering pipeline:
1. Reshape to long format
2. Create time-based features
3. Create lag and growth features
4. Create decade aggregates

**Returns:**
- `pd.DataFrame`: Long-format dataframe with all engineered features

**Example:**
```python
engineer = FeatureEngineer(df_clean)
df_long = engineer.engineer_all()
```

#### _reshape_to_long()
Convert wide format (years as columns) to long format (year as a column).

**Features created:**
- `year`: Integer year column
- `value`: Indicator value
- `topic`: Indicator topic category

#### _create_time_features()
Create time-based features:
- `decade`: Decade bucket (1960, 1970, ...)
- `period`: 6 historical bins (1960-1979, 1980-1989, etc.)
- `iraq_era`: 7 contextual historical periods (Pre-Iran War, Iran-Iraq War, etc.)

#### _classify_topic(code: str) -> str
Classify indicator by topic from code prefix.

**Parameters:**
- `code` (str): Indicator code

**Returns:**
- `str`: Topic category (Population & Health, Economy & Growth, etc.)

#### _classify_era(year: int) -> str
Classify historical era for Iraq based on year.

**Parameters:**
- `year` (int): Year

**Returns:**
- `str`: Era name (Pre-Iran War, Iran-Iraq War, Sanctions Era, etc.)

#### _create_lag_growth_features()
Create lag and growth rate features:
- `lag_1`, `lag_3`, `lag_5`: Previous 1, 3, 5 year values
- `yoy_growth`: Year-over-year percentage change
- `cagr_3yr`, `cagr_5yr`: Compound annual growth rates
- `rolling_5yr`: 5-year moving average

#### _create_decade_aggregates()
Create decade-level aggregate features:
- `decade_mean`: Average per indicator per decade
- `decade_std`: Standard deviation per indicator per decade
- `decade_count`: Number of observations per decade
- `decade_rank`: Year position within decade

#### get_feature_summary() -> dict
Return summary of engineered features.

**Returns:**
- `dict`: Dictionary containing:
  - `shape`: Shape of long-format dataframe
  - `total_features`: Total number of features
  - `feature_types`: Dictionary of feature categories
  - `indicators`: Number of unique indicators
  - `year_range`: Tuple of (min_year, max_year)

## Usage Example

```python
from src.data_loader import DataLoader
from src.data_cleaner import DataCleaner
from src.feature_engineer import FeatureEngineer

# Load and clean
loader = DataLoader()
df, _, _ = loader.load_all()
df_clean = DataCleaner(df).clean_all()

# Engineer features
engineer = FeatureEngineer(df_clean)
df_long = engineer.engineer_all()

# Get summary
summary = engineer.get_feature_summary()
print(f"Shape: {summary['shape']}")
print(f"Features: {summary['total_features']}")
```
