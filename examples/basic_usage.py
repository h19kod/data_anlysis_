"""
Basic Usage Example | مثال الاستخدام الأساسي
=============================================

This example demonstrates the basic usage of the Iraq WDI Analysis package.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.data_loader import DataLoader
from src.data_cleaner import DataCleaner
from src.feature_engineer import FeatureEngineer
from src.models import TrendModel, EraClassifier


def main():
    """Run basic analysis example."""
    print("=" * 60)
    print("Iraq WDI Analysis - Basic Usage Example")
    print("=" * 60)
    print()
    
    # Step 1: Load data
    print("Step 1: Loading data...")
    loader = DataLoader()
    df, df_country, df_indicator = loader.load_all()
    print(f"✓ Loaded {df.shape[0]} indicators")
    print()
    
    # Step 2: Clean data
    print("Step 2: Cleaning data...")
    cleaner = DataCleaner(df)
    df_clean = cleaner.clean_all()
    print(f"✓ Cleaned data: {df_clean.shape}")
    print()
    
    # Step 3: Engineer features
    print("Step 3: Engineering features...")
    engineer = FeatureEngineer(df_clean)
    df_long = engineer.engineer_all()
    print(f"✓ Engineered data: {df_long.shape}")
    print()
    
    # Step 4: Run trend model
    print("Step 4: Running trend model...")
    trend_model = TrendModel()
    key_indicators = ["SP.POP.TOTL", "SP.DYN.LE00.IN"]
    results = trend_model.fit(df_long, key_indicators)
    
    print("\nTrend Results:")
    for result in results:
        print(f"  {result.indicator_code}: R²={result.r_squared:.3f}")
    print()
    
    # Step 5: Run era classifier
    print("Step 5: Running era classifier...")
    classifier = EraClassifier()
    accuracy = classifier.fit(df_long)
    print(f"✓ Era classification accuracy: {accuracy:.1%}")
    print()
    
    print("=" * 60)
    print("Analysis complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
