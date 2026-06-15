"""
Custom Analysis Example | مثال تحليل مخصص
==========================================

This example shows how to customize the analysis for specific needs.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.data_loader import DataLoader
from src.data_cleaner import DataCleaner
from src.feature_engineer import FeatureEngineer
from src.models import TrendModel


def analyze_specific_indicators(indicator_codes):
    """
    Analyze specific indicators of interest.
    
    Args:
        indicator_codes: List of indicator codes to analyze
    """
    print(f"Analyzing {len(indicator_codes)} specific indicators...")
    
    # Load and clean
    loader = DataLoader()
    df, _, _ = loader.load_all()
    df_clean = DataCleaner(df).clean_all()
    df_long = FeatureEngineer(df_clean).engineer_all()
    
    # Run trend model
    trend_model = TrendModel()
    results = trend_model.fit(df_long, indicator_codes)
    
    # Print results
    print("\n" + "=" * 60)
    print("Trend Analysis Results")
    print("=" * 60)
    for result in results:
        print(f"\n{result.indicator_name}")
        print(f"  Code: {result.indicator_code}")
        print(f"  R²: {result.r_squared:.3f}")
        print(f"  Slope: {result.slope:,.2f} per year")
        print(f"  Direction: {result.direction}")
        if result.mape:
            print(f"  MAPE: {result.mape:.2f}%")
    
    return results


def analyze_specific_era(df_long, era_name):
    """
    Analyze data for a specific historical era.
    
    Args:
        df_long: Long-format dataframe
        era_name: Name of era to analyze
    """
    era_data = df_long[df_long["iraq_era"] == era_name]
    
    print(f"\nAnalyzing {era_name} era:")
    print(f"  Observations: {len(era_data)}")
    print(f"  Years: {era_data['year'].min()} - {era_data['year'].max()}")
    print(f"  Indicators: {era_data['Indicator Code'].nunique()}")
    
    return era_data


if __name__ == "__main__":
    # Example: Analyze specific indicators
    indicators = [
        "SP.POP.TOTL",      # Population
        "NY.GDP.MKTP.CD",    # GDP
        "SE.XPD.TOTL.GD.ZS", # Education expenditure
    ]
    
    results = analyze_specific_indicators(indicators)
    
    # Example: Analyze specific era
    from src.data_loader import DataLoader
    from src.data_cleaner import DataCleaner
    from src.feature_engineer import FeatureEngineer
    
    loader = DataLoader()
    df, _, _ = loader.load_all()
    df_clean = DataCleaner(df).clean_all()
    df_long = FeatureEngineer(df_clean).engineer_all()
    
    era_data = analyze_specific_era(df_long, "Iran-Iraq War")
