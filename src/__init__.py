"""
Iraq WDI Analysis Package
===========================

Professional data analysis package for Iraq's World Development Indicators.

Modules:
    - data_loader: Load and validate raw data
    - data_cleaner: Clean and preprocess data
    - feature_engineer: Create engineered features
    - models: Baseline modeling and evaluation
    - utils: Utility functions and helpers
    - visualization: Plotting and charting functions

Author: h19kod
Date: June 2025
"""

__version__ = "1.0.0"
__author__ = "h19kod"

from .data_loader import DataLoader
from .data_cleaner import DataCleaner
from .feature_engineer import FeatureEngineer
from .models import TrendModel, EraClassifier
from .utils import get_project_root, setup_logging

__all__ = [
    "DataLoader",
    "DataCleaner", 
    "FeatureEngineer",
    "TrendModel",
    "EraClassifier",
    "get_project_root",
    "setup_logging",
]
