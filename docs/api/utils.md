# Utils API Documentation
## وثائق API: الأدوات المساعدة

## Functions

### get_project_root() -> Path
Get the project root directory.

**Returns:**
- `Path`: Path object pointing to project root

**Example:**
```python
from src.utils import get_project_root
root = get_project_root()
print(f"Project root: {root}")
```

---

### setup_logging(log_file: Optional[str] = None, level: int = logging.INFO) -> logging.Logger
Setup logging configuration.

**Parameters:**
- `log_file` (Optional[str]): Optional log file path
- `level` (int): Logging level (default: logging.INFO)

**Returns:**
- `logging.Logger`: Configured logger

**Example:**
```python
from src.utils import setup_logging
import logging

logger = setup_logging(level=logging.DEBUG)
logger.info("This is a log message")
```

---

### ensure_dir(path: str) -> str
Ensure directory exists, create if not.

**Parameters:**
- `path` (str): Directory path

**Returns:**
- `str`: Directory path

**Example:**
```python
from src.utils import ensure_dir
output_dir = ensure_dir("outputs/results")
```

---

### format_number(num: float, decimals: int = 2) -> str
Format number with commas and specified decimals.

**Parameters:**
- `num` (float): Number to format
- `decimals` (int): Number of decimal places

**Returns:**
- `str`: Formatted string

**Example:**
```python
from src.utils import format_number
print(format_number(1234567.89))  # "1,234,567.89"
```

---

### format_percentage(num: float, decimals: int = 1) -> str
Format number as percentage.

**Parameters:**
- `num` (float): Number to format (0.95 -> 95%)
- `decimals` (int): Number of decimal places

**Returns:**
- `str`: Formatted percentage string

**Example:**
```python
from src.utils import format_percentage
print(format_percentage(0.955))  # "95.5%"
```

---

### get_indicator_name(df, indicator_code: str) -> str
Get indicator name from code.

**Parameters:**
- `df` (pd.DataFrame): Dataframe with Indicator Code and Indicator Name columns
- `indicator_code` (str): Code to lookup

**Returns:**
- `str`: Indicator name or code if not found

**Example:**
```python
from src.utils import get_indicator_name
name = get_indicator_name(df, "SP.POP.TOTL")
print(name)  # "Population, total"
```

---

### save_results(df, filepath: str, formats: list = None) -> None
Save dataframe to multiple formats.

**Parameters:**
- `df` (pd.DataFrame): DataFrame to save
- `filepath` (str): Base filepath (without extension)
- `formats` (list): List of formats ('csv', 'excel', 'pickle')

**Example:**
```python
from src.utils import save_results
save_results(df, "outputs/results", formats=["csv", "excel"])
```

---

## Class: ProgressTracker

### Description | الوصف
Simple progress tracker for long-running operations.

### Constructor | الباني

```python
ProgressTracker(total: int, desc: str = "Progress")
```

**Parameters:**
- `total` (int): Total number of items
- `desc` (str): Description string

### Methods

#### update(n: int = 1)
Update progress by n items.

**Parameters:**
- `n` (int): Number of items completed

**Example:**
```python
from src.utils import ProgressTracker

with ProgressTracker(100, "Processing") as tracker:
    for i in range(100):
        # Do work
        tracker.update()
```

## Usage Example

```python
from src.utils import (
    get_project_root,
    setup_logging,
    ensure_dir,
    format_number,
    format_percentage,
    save_results,
    ProgressTracker
)

# Get project root
root = get_project_root()

# Setup logging
logger = setup_logging()
logger.info("Starting analysis")

# Ensure output directory
output_dir = ensure_dir(f"{root}/outputs")

# Format numbers
print(format_number(1234567.89))
print(format_percentage(0.955))

# Save results
save_results(df, f"{output_dir}/results", formats=["csv"])

# Track progress
with ProgressTracker(100, "Processing") as tracker:
    for i in range(100):
        tracker.update()
```
