# DataCleaner API Documentation
## وثائق API: منظف البيانات

## Class: DataCleaner

### Description | الوصف
Handles all data cleaning operations: deduplication, missing values, standardization, and outlier treatment.

### Constructor | الباني

```python
DataCleaner(df: pd.DataFrame)
```

**Parameters:**
- `df` (pd.DataFrame): Raw dataframe to clean

### Attributes
- `df` (pd.DataFrame): Copy of the dataframe being cleaned
- `year_cols` (List[str]): List of year column names
- `capped_count` (int): Number of outlier values capped

### Methods

#### clean_all()
Run complete cleaning pipeline:
1. Remove duplicates
2. Handle missing values
3. Standardize formats
4. Cap outliers

**Returns:**
- `pd.DataFrame`: Cleaned dataframe

**Example:**
```python
cleaner = DataCleaner(df)
df_clean = cleaner.clean_all()
```

#### _remove_duplicates()
Remove duplicate rows and duplicate indicator codes.

#### _handle_missing_values()
Drop indicators with no data across all years.

#### _standardize_formats()
Standardize text and numeric columns:
- Strip whitespace from text columns
- Convert codes to uppercase
- Coerce year columns to numeric

#### _cap_outliers()
Detect and cap outliers using IQR method:
- Lower bound = Q1 - 1.5 × IQR
- Upper bound = Q3 + 1.5 × IQR
- Values outside bounds are clipped to bounds

#### _detect_outliers_iqr(row: pd.Series) -> int
Detect outliers for a single row using IQR method.

**Parameters:**
- `row` (pd.Series): Row of data

**Returns:**
- `int`: Number of outliers detected

#### _calculate_completeness() -> float
Calculate overall data completeness percentage.

**Returns:**
- `float`: Percentage of filled cells

#### get_cleaning_summary() -> dict
Return summary of cleaning operations.

**Returns:**
- `dict`: Dictionary containing:
  - `final_shape`: Shape of cleaned dataframe
  - `year_columns`: Number of year columns
  - `completeness_pct`: Data completeness percentage
  - `indicators_count`: Number of indicators
  - `outliers_capped`: Number of outlier values capped

## Usage Example

```python
from src.data_loader import DataLoader
from src.data_cleaner import DataCleaner

# Load data
loader = DataLoader()
df, _, _ = loader.load_all()

# Clean data
cleaner = DataCleaner(df)
df_clean = cleaner.clean_all()

# Get summary
summary = cleaner.get_cleaning_summary()
print(f"Final shape: {summary['final_shape']}")
print(f"Completeness: {summary['completeness_pct']:.1f}%")
```
