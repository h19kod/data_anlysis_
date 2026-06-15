"""
Tests for data_loader module | اختبارات وحدة تحميل البيانات
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.data_loader import DataLoader


class TestDataLoader(unittest.TestCase):
    """Test cases for DataLoader class."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.loader = DataLoader()
    
    def test_initialization(self):
        """Test DataLoader initialization."""
        self.assertIsNotNone(self.loader)
        self.assertEqual(self.loader.data_dir, "API_IRQ_DS2_en_csv_v2_16712")
    
    def test_load_main_data(self):
        """Test loading main data file."""
        df = self.loader._load_main_data()
        self.assertIsNotNone(df)
        self.assertGreater(len(df), 0)
        self.assertIn("Indicator Code", df.columns)
    
    def test_load_country_meta(self):
        """Test loading country metadata."""
        df = self.loader._load_country_meta()
        self.assertIsNotNone(df)
        self.assertGreater(len(df), 0)
    
    def test_load_indicator_meta(self):
        """Test loading indicator metadata."""
        df = self.loader._load_indicator_meta()
        self.assertIsNotNone(df)
        self.assertGreater(len(df), 0)
    
    def test_load_all(self):
        """Test loading all data files."""
        df, df_country, df_indicator = self.loader.load_all()
        
        self.assertIsNotNone(df)
        self.assertIsNotNone(df_country)
        self.assertIsNotNone(df_indicator)
        
        # Check shapes
        self.assertGreater(df.shape[0], 1000)  # Should have many indicators
        self.assertGreater(df.shape[1], 50)   # Should have many year columns
    
    def test_validate_data(self):
        """Test data validation."""
        self.loader.load_all()
        validation = self.loader.validate_data()
        
        self.assertTrue(validation["valid"])
        self.assertTrue(validation["has_indicator_code"])
        self.assertTrue(validation["has_year_columns"])


if __name__ == "__main__":
    unittest.main()
