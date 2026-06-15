"""
Feature Engineer Module | وحدة هندسة المتغيرات
=================================================

Creates time-based, lag, growth, and decade aggregate features for modeling.
"""

import pandas as pd
import numpy as np
from typing import List, Optional


class FeatureEngineer:
    """
    Engineer features for time-series and panel analysis.
    
    Features Created:
        - Time-based: decade, period, iraq_era
        - Lag & Growth: lag_1, lag_3, lag_5, yoy_growth, cagr_3yr, cagr_5yr
        - Decade Aggregates: decade_mean, decade_std, decade_count, decade_rank
    """
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize FeatureEngineer.
        
        Args:
            df: Cleaned wide-format dataframe
        """
        self.df_wide = df.copy()
        self.year_cols = [c for c in df.columns if c.isdigit()]
        self.df_long: Optional[pd.DataFrame] = None
        
    def engineer_all(self) -> pd.DataFrame:
        """
        Run complete feature engineering pipeline.
        
        Returns:
            Long-format dataframe with all engineered features
        """
        print("=" * 60)
        print("Feature Engineering Pipeline | خط أنابيب هندسة المتغيرات")
        print("=" * 60)
        
        # Step 1: Reshape to long format
        self._reshape_to_long()
        
        # Step 2: Create time-based features
        self._create_time_features()
        
        # Step 3: Create lag and growth features
        self._create_lag_growth_features()
        
        # Step 4: Create decade aggregates
        self._create_decade_aggregates()
        
        print("\n" + "=" * 60)
        print("Feature Engineering Complete | اكتملت هندسة المتغيرات")
        print(f"Final shape: {self.df_long.shape}")
        print(f"Features: {len(self.df_long.columns)}")
        print("=" * 60)
        
        return self.df_long
    
    def _reshape_to_long(self) -> None:
        """Convert wide format to long format."""
        id_cols = [
            "Country Name", "Country Code", "Indicator Name", 
            "Indicator Code", "outlier_count"
        ]
        
        # Add topic column if not present
        if "topic" not in self.df_wide.columns:
            self.df_wide["topic"] = self.df_wide["Indicator Code"].apply(
                self._classify_topic
            )
            id_cols.append("topic")
        
        # Reshape
        self.df_long = self.df_wide[id_cols + self.year_cols].melt(
            id_vars=id_cols,
            value_vars=self.year_cols,
            var_name="year",
            value_name="value"
        )
        
        # Convert types
        self.df_long["year"] = self.df_long["year"].astype(int)
        self.df_long = self.df_long.dropna(subset=["value"]).reset_index(drop=True)
        
        print(f"✓ Reshaped to long format: {self.df_long.shape}")
    
    def _classify_topic(self, code: str) -> str:
        """Classify indicator by topic from code prefix."""
        topics = {
            "SP.": "Population & Health",
            "NY.": "Economy & Growth",
            "NE.": "Trade & External",
            "TX.": "Exports",
            "TM.": "Imports",
            "EN.": "Environment",
            "SE.": "Education",
            "SI.": "Social Protection",
            "IC.": "Business & Private Sector",
            "DT.": "External Debt",
            "VC.": "Violence & Conflict",
            "MS.": "Military",
        }
        
        for prefix, topic in topics.items():
            if code.startswith(prefix):
                return topic
        return "Other"
    
    def _create_time_features(self) -> None:
        """Create decade, period, and era features."""
        # Decade
        self.df_long["decade"] = (self.df_long["year"] // 10) * 10
        
        # Period bins
        self.df_long["period"] = pd.cut(
            self.df_long["year"],
            bins=[1959, 1979, 1989, 1999, 2009, 2019, 2025],
            labels=["1960-1979", "1980-1989", "1990-1999", "2000-2009", "2010-2019", "2020-2025"]
        )
        
        # Iraq historical era
        self.df_long["iraq_era"] = self.df_long["year"].apply(self._classify_era)
        
        print("✓ Created time features: decade, period, iraq_era")
    
    def _classify_era(self, year: int) -> str:
        """Classify historical era for Iraq."""
        if year < 1980:
            return "Pre-Iran War"
        elif year < 1989:
            return "Iran-Iraq War"
        elif year < 2003:
            return "Sanctions Era"
        elif year < 2011:
            return "Post-Invasion"
        elif year < 2014:
            return "US Withdrawal"
        elif year < 2017:
            return "ISIS Conflict"
        else:
            return "Post-ISIS"
    
    def _create_lag_growth_features(self) -> None:
        """Create lag and growth rate features."""
        # Sort for time-series calculations
        self.df_long = self.df_long.sort_values(
            ["Indicator Code", "year"]
        ).reset_index(drop=True)
        
        # Lag features
        self.df_long["lag_1"] = self.df_long.groupby("Indicator Code")["value"].shift(1)
        self.df_long["lag_3"] = self.df_long.groupby("Indicator Code")["value"].shift(3)
        self.df_long["lag_5"] = self.df_long.groupby("Indicator Code")["value"].shift(5)
        
        # Growth rates
        self.df_long["yoy_growth"] = self.df_long.groupby("Indicator Code")["value"].pct_change() * 100
        
        # CAGR
        self.df_long["cagr_3yr"] = ((
            self.df_long["value"] / self.df_long["lag_3"]
        ) ** (1/3) - 1) * 100
        
        self.df_long["cagr_5yr"] = ((
            self.df_long["value"] / self.df_long["lag_5"]
        ) ** (1/5) - 1) * 100
        
        # Rolling average
        self.df_long["rolling_5yr"] = self.df_long.groupby("Indicator Code")["value"].rolling(
            5, min_periods=1
        ).mean().reset_index(level=0, drop=True)
        
        print("✓ Created lag & growth features: lag_1/3/5, yoy_growth, cagr_3/5yr, rolling_5yr")
    
    def _create_decade_aggregates(self) -> None:
        """Create decade-level aggregate features."""
        # Calculate decade statistics
        decade_stats = self.df_long.groupby(["Indicator Code", "decade"])["value"].agg([
            ("decade_mean", "mean"),
            ("decade_std", "std"),
            ("decade_count", "count")
        ]).reset_index()
        
        # Merge back
        self.df_long = self.df_long.merge(
            decade_stats, 
            on=["Indicator Code", "decade"], 
            how="left"
        )
        
        # Decade rank
        self.df_long["decade_rank"] = self.df_long.groupby(
            ["Indicator Code", "decade"]
        )["year"].rank()
        
        print("✓ Created decade aggregates: decade_mean, decade_std, decade_count, decade_rank")
    
    def get_feature_summary(self) -> dict:
        """Return summary of engineered features."""
        if self.df_long is None:
            return {"error": "Features not yet engineered"}
        
        feature_types = {
            "time_based": ["decade", "period", "iraq_era"],
            "lag_growth": ["lag_1", "lag_3", "lag_5", "yoy_growth", "cagr_3yr", "cagr_5yr", "rolling_5yr"],
            "decade_aggregates": ["decade_mean", "decade_std", "decade_count", "decade_rank"]
        }
        
        return {
            "shape": self.df_long.shape,
            "total_features": len(self.df_long.columns),
            "feature_types": feature_types,
            "indicators": self.df_long["Indicator Code"].nunique(),
            "year_range": (self.df_long["year"].min(), self.df_long["year"].max())
        }


if __name__ == "__main__":
    # Test feature engineering
    from data_loader import DataLoader
    from data_cleaner import DataCleaner
    
    loader = DataLoader()
    df, _, _ = loader.load_all()
    
    cleaner = DataCleaner(df)
    df_clean = cleaner.clean_all()
    
    engineer = FeatureEngineer(df_clean)
    df_long = engineer.engineer_all()
    
    print("\nFeature Summary:")
    print(engineer.get_feature_summary())
