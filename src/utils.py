"""
Utils Module | وحدة الأدوات المساعدة
====================================

Utility functions and helpers for the analysis.
"""

import os
import sys
import logging
from pathlib import Path
from typing import Optional


def get_project_root() -> Path:
    """
    Get the project root directory.
    
    Returns:
        Path object pointing to project root
    """
    # Get the directory of the current file
    current_file = Path(__file__).resolve()
    # Go up two levels: src/utils.py -> src/ -> project root
    return current_file.parent.parent


def setup_logging(log_file: Optional[str] = None, level: int = logging.INFO) -> logging.Logger:
    """
    Setup logging configuration.
    
    Args:
        log_file: Optional log file path
        level: Logging level
        
    Returns:
        Configured logger
    """
    logger = logging.getLogger("iraq_wdi")
    logger.setLevel(level)
    
    # Clear existing handlers
    logger.handlers = []
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def ensure_dir(path: str) -> str:
    """
    Ensure directory exists, create if not.
    
    Args:
        path: Directory path
        
    Returns:
        Directory path
    """
    Path(path).mkdir(parents=True, exist_ok=True)
    return path


def format_number(num: float, decimals: int = 2) -> str:
    """
    Format number with commas and specified decimals.
    
    Args:
        num: Number to format
        decimals: Number of decimal places
        
    Returns:
        Formatted string
    """
    if num is None:
        return "N/A"
    return f"{num:,.{decimals}f}"


def format_percentage(num: float, decimals: int = 1) -> str:
    """
    Format number as percentage.
    
    Args:
        num: Number to format (0.95 -> 95%)
        decimals: Number of decimal places
        
    Returns:
        Formatted percentage string
    """
    if num is None:
        return "N/A"
    return f"{num * 100:.{decimals}f}%"


def get_indicator_name(df, indicator_code: str) -> str:
    """
    Get indicator name from code.
    
    Args:
        df: Dataframe with Indicator Code and Indicator Name columns
        indicator_code: Code to lookup
        
    Returns:
        Indicator name or code if not found
    """
    matches = df[df["Indicator Code"] == indicator_code]["Indicator Name"]
    if len(matches) > 0:
        return matches.iloc[0]
    return indicator_code


def save_results(df, filepath: str, formats: list = None) -> None:
    """
    Save dataframe to multiple formats.
    
    Args:
        df: DataFrame to save
        filepath: Base filepath (without extension)
        formats: List of formats ('csv', 'excel', 'pickle')
    """
    if formats is None:
        formats = ['csv']
    
    for fmt in formats:
        if fmt == 'csv':
            df.to_csv(f"{filepath}.csv", index=False, encoding='utf-8-sig')
            print(f"✓ Saved CSV: {filepath}.csv")
        elif fmt == 'excel':
            df.to_excel(f"{filepath}.xlsx", index=False)
            print(f"✓ Saved Excel: {filepath}.xlsx")
        elif fmt == 'pickle':
            df.to_pickle(f"{filepath}.pkl")
            print(f"✓ Saved Pickle: {filepath}.pkl")


class ProgressTracker:
    """
    Simple progress tracker for long-running operations.
    """
    
    def __init__(self, total: int, desc: str = "Progress"):
        self.total = total
        self.current = 0
        self.desc = desc
    
    def update(self, n: int = 1):
        """Update progress."""
        self.current += n
        pct = (self.current / self.total) * 100
        print(f"\r{self.desc}: {self.current}/{self.total} ({pct:.1f}%)", end="")
        if self.current >= self.total:
            print()  # New line at end
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        if self.current < self.total:
            print()


if __name__ == "__main__":
    # Test utilities
    print("Testing Utils | اختبار الأدوات المساعدة")
    print("=" * 50)
    
    # Test get_project_root
    root = get_project_root()
    print(f"✓ Project root: {root}")
    
    # Test ensure_dir
    test_dir = ensure_dir(os.path.join(root, "test_output"))
    print(f"✓ Ensured directory: {test_dir}")
    
    # Test formatting
    print(f"✓ Format number: {format_number(1234567.89)}")
    print(f"✓ Format percentage: {format_percentage(0.955)}")
    
    # Test logger
    logger = setup_logging()
    logger.info("Test log message | رسالة اختبار")
    
    print("\nAll utilities working! | جميع الأدوات تعمل!")
