"""
Tests for feature_engineer module | اختبارات وحدة هندسة المتغيرات
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.data_loader import DataLoader
from src.data_cleaner import DataCleaner
from src.feature_engineer import FeatureEngineer


class TestFeatureEngineer(unittest.TestCase):
    """Test cases for FeatureEngineer class."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        loader = DataLoader()
        df, _, _ = loader.load_all()
        
        cleaner = DataCleaner(df)
        df_clean = cleaner.clean_all()
        
        cls.engineer = FeatureEngineer(df_clean)
    
    def test_initialization(self):
        """Test FeatureEngineer initialization."""
        self.assertIsNotNone(self.engineer.df_wide)
        self.assertIsNotNone(self.engineer.year_cols)
        self.assertGreater(len(self.engineer.year_cols), 0)
    
    def test_reshape_to_long(self):
        """Test reshaping to long format."""
        self.engineer._reshape_to_long()
        
        self.assertIsNotNone(self.engineer.df_long)
        self.assertIn("year", self.engineer.df_long.columns)
        self.assertIn("value", self.engineer.df_long.columns)
    
    def test_create_time_features(self):
        """Test time feature creation."""
        self.engineer._reshape_to_long()
        self.engineer._create_time_features()
        
        # Check created columns
        self.assertIn("decade", self.engineer.df_long.columns)
        self.assertIn("period", self.engineer.df_long.columns)
        self.assertIn("iraq_era", self.engineer.df_long.columns)
        
        # Check decade values
        decades = self.engineer.df_long["decade"].unique()
        self.assertTrue(all(d % 10 == 0 for d in decades if not pd.isna(d)))
    
    def test_create_lag_growth_features(self):
        """Test lag and growth feature creation."""
        self.engineer._reshape_to_long()
        self.engineer._create_time_features()
        self.engineer._create_lag_growth_features()
        
        # Check created columns
        lag_cols = ["lag_1", "lag_3", "lag_5"]
        for col in lag_cols:
            self.assertIn(col, self.engineer.df_long.columns)
        
        self.assertIn("yoy_growth", self.engineer.df_long.columns)
        self.assertIn("cagr_3yr", self.engineer.df_long.columns)
        self.assertIn("rolling_5yr", self.engineer.df_long.columns)
    
    def test_create_decade_aggregates(self):
        """Test decade aggregate creation."""
        self.engineer._reshape_to_long()
        self.engineer._create_time_features()
        self.engineer._create_lag_growth_features()
        self.engineer._create_decade_aggregates()
        
        # Check created columns
        self.assertIn("decade_mean", self.engineer.df_long.columns)
        self.assertIn("decade_std", self.engineer.df_long.columns)
        self.assertIn("decade_count", self.engineer.df_long.columns)
        self.assertIn("decade_rank", self.engineer.df_long.columns)
    
    def test_engineer_all(self):
        """Test complete feature engineering pipeline."""
        df_long = self.engineer.engineer_all()
        
        self.assertIsNotNone(df_long)
        self.assertGreater(len(df_long), 0)
        
        # Get summary
        summary = self.engineer.get_feature_summary()
        self.assertIn("shape", summary)
        self.assertIn("feature_types", summary)


if __name__ == "__main__":
    # Need to import pandas for the test
    import pandas as pd
    unittest.main()
