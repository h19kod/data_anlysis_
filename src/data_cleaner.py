"""
Data Cleaner Module | وحدة تنظيف البيانات
===========================================

Handles all data cleaning operations: deduplication, missing values,
standardization, and outlier treatment.
"""

import pandas as pd
import numpy as np
from typing import List, Tuple


class DataCleaner:
    """
    Clean and preprocess Iraq WDI data.
    
    Pipeline:
        1. Remove duplicates
        2. Handle missing values (drop empty rows)
        3. Standardize data types and formats
        4. Detect and cap outliers
    """
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize DataCleaner.
        
        Args:
            df: Raw dataframe to clean
        """
        self.df = df.copy()
        self.year_cols = [c for c in df.columns if c.isdigit()]
        self.capped_count = 0
        
    def clean_all(self) -> pd.DataFrame:
        """
        Run complete cleaning pipeline.
        
        Returns:
            Cleaned dataframe
        """
        print("=" * 60)
        print("Starting Data Cleaning Pipeline | بدء خط أنابيب تنظيف البيانات")
        print("=" * 60)
        
        # Step 1: Remove duplicates
        self._remove_duplicates()
        
        # Step 2: Handle missing values
        self._handle_missing_values()
        
        # Step 3: Standardize formats
        self._standardize_formats()
        
        # Step 4: Address outliers
        self._cap_outliers()
        
        print("\n" + "=" * 60)
        print("Cleaning Complete | اكتمل التنظيف")
        print(f"Final shape: {self.df.shape}")
        print(f"Completeness: {self._calculate_completeness():.1f}%")
        print("=" * 60)
        
        return self.df
    
    def _remove_duplicates(self) -> None:
        """Remove duplicate rows and duplicate indicator codes."""
        before = len(self.df)
        
        # Remove fully duplicated rows
        self.df = self.df.drop_duplicates()
        
        # Remove duplicate indicator codes (keep first)
        self.df = self.df.drop_duplicates(
            subset=["Indicator Code"], 
            keep="first"
        ).reset_index(drop=True)
        
        removed = before - len(self.df)
        print(f"✓ Removed duplicates: {before} → {len(self.df)} (-{removed})")
    
    def _handle_missing_values(self) -> None:
        """Drop indicators with no data across all years."""
        before = len(self.df)
        
        # Find completely empty rows
        empty_mask = self.df[self.year_cols].isna().all(axis=1)
        empty_count = empty_mask.sum()
        
        # Remove empty rows
        self.df = self.df[~empty_mask].reset_index(drop=True)
        
        print(f"✓ Dropped empty indicators: {before} → {len(self.df)} (-{empty_count})")
        print(f"  (Removed {empty_count} indicators with zero data)")
    
    def _standardize_formats(self) -> None:
        """Standardize text and numeric columns."""
        # Standardize text columns
        text_cols = ["Country Name", "Country Code", "Indicator Name", "Indicator Code"]
        for col in text_cols:
            if col in self.df.columns:
                self.df[col] = self.df[col].str.strip()
                if col.endswith("Code"):
                    self.df[col] = self.df[col].str.upper()
        
        # Standardize year columns to numeric
        for col in self.year_cols:
            self.df[col] = pd.to_numeric(self.df[col], errors="coerce")
        
        print(f"✓ Standardized formats: {len(text_cols)} text columns, {len(self.year_cols)} numeric columns")
    
    def _detect_outliers_iqr(self, row: pd.Series) -> int:
        """Detect outliers using IQR method for a single row."""
        vals = row[self.year_cols].dropna()
        if len(vals) < 4:
            return 0
        
        q1, q3 = vals.quantile([0.25, 0.75])
        iqr = q3 - q1
        
        if iqr == 0:
            return 0
        
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        return ((vals < lower) | (vals > upper)).sum()
    
    def _cap_outliers(self) -> None:
        """Detect and cap outliers using IQR method."""
        # Count outliers
        outlier_counts = self.df.apply(
            lambda row: self._detect_outliers_iqr(row), 
            axis=1
        )
        
        indicators_with_outliers = (outlier_counts > 0).sum()
        total_outliers = outlier_counts.sum()
        
        self.df["outlier_count"] = outlier_counts
        
        # Cap outliers
        capped = 0
        for idx in self.df.index:
            vals = self.df.loc[idx, self.year_cols]
            valid = vals.dropna()
            
            if len(valid) < 4:
                continue
            
            q1, q3 = valid.quantile([0.25, 0.75])
            iqr = q3 - q1
            
            if iqr == 0:
                continue
            
            lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
            cap_mask = (vals < lower) | (vals > upper)
            capped += cap_mask.sum()
            
            self.df.loc[idx, self.year_cols] = vals.clip(lower, upper)
        
        self.capped_count = capped
        print(f"✓ Capped outliers: {indicators_with_outliers} indicators, {capped} values")
    
    def _calculate_completeness(self) -> float:
        """Calculate overall data completeness percentage."""
        total = self.df[self.year_cols].size
        filled = self.df[self.year_cols].notna().sum().sum()
        return (filled / total) * 100 if total > 0 else 0
    
    def get_cleaning_summary(self) -> dict:
        """Return summary of cleaning operations."""
        return {
            "final_shape": self.df.shape,
            "year_columns": len(self.year_cols),
            "completeness_pct": round(self._calculate_completeness(), 1),
            "indicators_count": len(self.df),
            "outliers_capped": self.capped_count,
        }


if __name__ == "__main__":
    # Test with sample data
    from data_loader import DataLoader
    
    loader = DataLoader()
    df, _, _ = loader.load_all()
    
    cleaner = DataCleaner(df)
    df_clean = cleaner.clean_all()
    
    print("\nCleaning Summary:")
    print(cleaner.get_cleaning_summary())
