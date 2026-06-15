"""
Data Loader Module | وحدة تحميل البيانات
=============================================

Handles loading and initial validation of Iraq WDI data.
"""

import os
import pandas as pd
from typing import Tuple, Optional


class DataLoader:
    """
    Load and validate Iraq WDI data from CSV files.
    
    Attributes:
        data_dir (str): Directory containing data files
    """
    
    def __init__(self, data_dir: str = "API_IRQ_DS2_en_csv_v2_16712"):
        """
        Initialize DataLoader.
        
        Args:
            data_dir: Path to data directory
        """
        self.data_dir = data_dir
        self.df: Optional[pd.DataFrame] = None
        self.df_country: Optional[pd.DataFrame] = None
        self.df_indicator: Optional[pd.DataFrame] = None
        
    def load_all(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Load all three data files.
        
        Returns:
            Tuple of (main_data, country_meta, indicator_meta)
        """
        self.df = self._load_main_data()
        self.df_country = self._load_country_meta()
        self.df_indicator = self._load_indicator_meta()
        
        return self.df, self.df_country, self.df_indicator
    
    def _load_main_data(self) -> pd.DataFrame:
        """Load main WDI data file."""
        file_path = os.path.join(self.data_dir, "API_IRQ_DS2_en_csv_v2_16712.csv")
        
        # Skip first 4 header rows
        df = pd.read_csv(file_path, skiprows=4)
        
        # Drop empty columns from trailing commas
        df = df.drop(columns=[c for c in df.columns if c.startswith("Unnamed")])
        
        print(f"✓ Loaded main data: {df.shape}")
        return df
    
    def _load_country_meta(self) -> pd.DataFrame:
        """Load country metadata."""
        file_path = os.path.join(
            self.data_dir, 
            "Metadata_Country_API_IRQ_DS2_en_csv_v2_16712.csv"
        )
        
        df = pd.read_csv(file_path)
        df = df.drop(columns=[c for c in df.columns if c.startswith("Unnamed")])
        
        print(f"✓ Loaded country metadata: {df.shape}")
        return df
    
    def _load_indicator_meta(self) -> pd.DataFrame:
        """Load indicator metadata."""
        file_path = os.path.join(
            self.data_dir,
            "Metadata_Indicator_API_IRQ_DS2_en_csv_v2_16712.csv"
        )
        
        df = pd.read_csv(file_path)
        df = df.drop(columns=[c for c in df.columns if c.startswith("Unnamed")])
        
        print(f"✓ Loaded indicator metadata: {df.shape}")
        return df
    
    def validate_data(self) -> dict:
        """
        Validate loaded data structure.
        
        Returns:
            Dictionary with validation results
        """
        results = {
            "main_shape": self.df.shape if self.df is not None else None,
            "country_shape": self.df_country.shape if self.df_country is not None else None,
            "indicator_shape": self.df_indicator.shape if self.df_indicator is not None else None,
            "has_indicator_code": "Indicator Code" in self.df.columns if self.df is not None else False,
            "has_year_columns": any(c.isdigit() for c in self.df.columns) if self.df is not None else False,
        }
        
        results["valid"] = all([
            results["main_shape"] is not None,
            results["has_indicator_code"],
            results["has_year_columns"]
        ])
        
        return results


if __name__ == "__main__":
    # Test the loader
    loader = DataLoader()
    df, df_country, df_indicator = loader.load_all()
    validation = loader.validate_data()
    print("\nValidation Results:", validation)
