"""
Tests for data_cleaner module | اختبارات وحدة تنظيف البيانات
"""

import unittest
import sys
import os
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.data_loader import DataLoader
from src.data_cleaner import DataCleaner


class TestDataCleaner(unittest.TestCase):
    """Test cases for DataCleaner class."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        loader = DataLoader()
        df, _, _ = loader.load_all()
        cls.cleaner = DataCleaner(df)
    
    def test_initialization(self):
        """Test DataCleaner initialization."""
        self.assertIsNotNone(self.cleaner.df)
        self.assertIsNotNone(self.cleaner.year_cols)
        self.assertGreater(len(self.cleaner.year_cols), 0)
    
    def test_remove_duplicates(self):
        """Test duplicate removal."""
        initial_count = len(self.cleaner.df)
        self.cleaner._remove_duplicates()
        
        # Should not increase
        self.assertLessEqual(len(self.cleaner.df), initial_count)
        
        # Should have no duplicate indicator codes
        codes = self.cleaner.df["Indicator Code"]
        self.assertEqual(len(codes), len(codes.unique()))
    
    def test_handle_missing_values(self):
        """Test handling missing values."""
        self.cleaner._remove_duplicates()
        initial_count = len(self.cleaner.df)
        
        self.cleaner._handle_missing_values()
        
        # Should have no completely empty rows
        empty_mask = self.cleaner.df[self.cleaner.year_cols].isna().all(axis=1)
        self.assertEqual(empty_mask.sum(), 0)
    
    def test_standardize_formats(self):
        """Test format standardization."""
        self.cleaner._standardize_formats()
        
        # Country code should be uppercase
        if "Country Code" in self.cleaner.df.columns:
            codes = self.cleaner.df["Country Code"].dropna()
            if len(codes) > 0:
                self.assertEqual(codes.iloc[0], codes.iloc[0].upper())
    
    def test_cap_outliers(self):
        """Test outlier capping."""
        self.cleaner._cap_outliers()
        
        # Should have outlier_count column
        self.assertIn("outlier_count", self.cleaner.df.columns)
    
    def test_clean_all(self):
        """Test complete cleaning pipeline."""
        df_clean = self.cleaner.clean_all()
        
        self.assertIsNotNone(df_clean)
        self.assertGreater(len(df_clean), 0)
        
        # Get summary
        summary = self.cleaner.get_cleaning_summary()
        self.assertIn("final_shape", summary)
        self.assertIn("completeness_pct", summary)
        
        # Completeness should be reasonable
        self.assertGreater(summary["completeness_pct"], 0)


if __name__ == "__main__":
    unittest.main()
