# DataLoader API Documentation
## وثائق API: محمل البيانات

## Class: DataLoader

### Description | الوصف
Handles loading and initial validation of Iraq WDI data from CSV files.

### Constructor | الباني

```python
DataLoader(data_dir: str = "API_IRQ_DS2_en_csv_v2_16712")
```

**Parameters:**
- `data_dir` (str): Path to directory containing data files. Default: "API_IRQ_DS2_en_csv_v2_16712"

### Methods

#### load_all()
Load all three data files (main data, country metadata, indicator metadata).

**Returns:**
- `Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]`: (main_data, country_meta, indicator_meta)

**Example:**
```python
loader = DataLoader()
df, df_country, df_indicator = loader.load_all()
```

#### _load_main_data()
Load the main WDI data file, skipping header rows and dropping empty columns.

**Returns:**
- `pd.DataFrame`: Main data dataframe

#### _load_country_meta()
Load country metadata file.

**Returns:**
- `pd.DataFrame`: Country metadata dataframe

#### _load_indicator_meta()
Load indicator metadata file.

**Returns:**
- `pd.DataFrame`: Indicator metadata dataframe

#### validate_data()
Validate loaded data structure.

**Returns:**
- `dict`: Dictionary with validation results including:
  - `main_shape`: Shape of main data
  - `country_shape`: Shape of country metadata
  - `indicator_shape`: Shape of indicator metadata
  - `has_indicator_code`: Boolean, if Indicator Code column exists
  - `has_year_columns`: Boolean, if year columns exist
  - `valid`: Boolean, overall validation status

**Example:**
```python
validation = loader.validate_data()
if validation["valid"]:
    print("Data is valid!")
```

## Usage Example

```python
from src.data_loader import DataLoader

# Initialize loader
loader = DataLoader()

# Load all data
df, df_country, df_indicator = loader.load_all()

# Validate
validation = loader.validate_data()
print(f"Main data shape: {validation['main_shape']}")
print(f"Valid: {validation['valid']}")
```
