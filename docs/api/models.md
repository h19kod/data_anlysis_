# Models API Documentation
## وثائق API: النماذج

## Class: TrendModel

### Description | الوصف
Simple linear trend model using least squares regression.

### Constructor | الباني

```python
TrendModel()
```

### Attributes
- `results` (List[TrendResult]): List of fitted trend results

### Methods

#### fit(df_long: pd.DataFrame, indicator_codes: List[str]) -> List[TrendResult]
Fit linear trends for specified indicators.

**Parameters:**
- `df_long` (pd.DataFrame): Long-format dataframe
- `indicator_codes` (List[str]): List of indicator codes to model

**Returns:**
- `List[TrendResult]`: List of trend results

**Example:**
```python
trend_model = TrendModel()
results = trend_model.fit(df_long, ["SP.POP.TOTL", "NY.GDP.MKTP.CD"])
```

#### _fit_single(df_long: pd.DataFrame, indicator_code: str) -> Optional[TrendResult]
Fit trend for a single indicator.

**Parameters:**
- `df_long` (pd.DataFrame): Long-format dataframe
- `indicator_code` (str): Indicator code to model

**Returns:**
- `Optional[TrendResult]`: Trend result or None if insufficient data

#### get_summary_df() -> pd.DataFrame
Return results as DataFrame.

**Returns:**
- `pd.DataFrame`: DataFrame with columns: Indicator, Name, N, Slope, R², MAPE, Direction

## Dataclass: TrendResult

### Fields
- `indicator_code` (str): Indicator code
- `indicator_name` (str): Indicator name
- `n_observations` (int): Number of observations
- `slope` (float): Slope coefficient
- `intercept` (float): Intercept coefficient
- `r_squared` (float): R-squared value
- `mape` (Optional[float]): Mean Absolute Percentage Error
- `direction` (str): "UP" or "DOWN"

---

## Class: EraClassifier

### Description | الوصف
Nearest-centroid classifier for historical era classification.

### Constructor | الباني

```python
EraClassifier()
```

### Attributes
- `centroids` (Dict[str, np.ndarray]): Centroids for each era
- `accuracy` (float): Overall classification accuracy
- `class_accuracy` (Dict[str, float]): Per-class accuracy

### Methods

#### fit(df_long: pd.DataFrame) -> float
Fit era classifier and calculate accuracy.

**Parameters:**
- `df_long` (pd.DataFrame): Long-format dataframe with era labels

**Returns:**
- `float`: Overall classification accuracy

**Example:**
```python
classifier = EraClassifier()
accuracy = classifier.fit(df_long)
print(f"Accuracy: {accuracy:.1%}")
```

#### _prepare_features(df_long: pd.DataFrame, indicators: List[str]) -> pd.DataFrame
Prepare feature matrix for classification.

**Parameters:**
- `df_long` (pd.DataFrame): Long-format dataframe
- `indicators` (List[str]): List of indicator codes to use as features

**Returns:**
- `pd.DataFrame`: Feature matrix with normalized features

#### _calculate_centroids(df_wide: pd.DataFrame) -> Dict[str, np.ndarray]
Calculate centroids for each era.

**Parameters:**
- `df_wide` (pd.DataFrame): Wide-format feature matrix

**Returns:**
- `Dict[str, np.ndarray]`: Dictionary mapping era names to centroids

#### _nearest_centroid(features: np.ndarray) -> str
Find nearest centroid for given features.

**Parameters:**
- `features` (np.ndarray): Feature vector

**Returns:**
- `str`: Era name of nearest centroid

---

## Class: NaiveForecaster

### Description | الوصف
Naive forecasting using moving average.

### Constructor | الباني

```python
NaiveForecaster(window: int = 3)
```

**Parameters:**
- `window` (int): Window size for moving average. Default: 3

### Attributes
- `window` (int): Window size
- `mape` (Optional[float]): Mean Absolute Percentage Error
- `rmse` (Optional[float]): Root Mean Squared Error

### Methods

#### evaluate(df_long: pd.DataFrame, indicator_code: str) -> Dict
Evaluate naive forecast for an indicator.

**Parameters:**
- `df_long` (pd.DataFrame): Long-format dataframe
- `indicator_code` (str): Indicator to forecast

**Returns:**
- `dict`: Dictionary with `mape` and `rmse` keys

**Example:**
```python
forecaster = NaiveForecaster(window=3)
metrics = forecaster.evaluate(df_long, "SP.POP.TOTL")
print(f"MAPE: {metrics['mape']:.2f}%")
```

## Usage Example

```python
from src.models import TrendModel, EraClassifier, NaiveForecaster

# Trend model
trend_model = TrendModel()
results = trend_model.fit(df_long, ["SP.POP.TOTL", "NY.GDP.MKTP.CD"])
print(trend_model.get_summary_df())

# Era classifier
classifier = EraClassifier()
accuracy = classifier.fit(df_long)
print(f"Accuracy: {accuracy:.1%}")

# Naive forecaster
forecaster = NaiveForecaster(window=3)
metrics = forecaster.evaluate(df_long, "SP.POP.TOTL")
print(f"MAPE: {metrics['mape']:.2f}%")
```
