"""
Models Module | وحدة النماذج
==============================

Baseline models for trend analysis and era classification.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class TrendResult:
    """Result container for trend model."""
    indicator_code: str
    indicator_name: str
    n_observations: int
    slope: float
    intercept: float
    r_squared: float
    mape: Optional[float] = None
    direction: str = ""


class TrendModel:
    """
    Simple linear trend model using least squares.
    
    Formula: value = slope * year + intercept
    """
    
    def __init__(self):
        self.results: List[TrendResult] = []
    
    def fit(self, df_long: pd.DataFrame, indicator_codes: List[str]) -> List[TrendResult]:
        """
        Fit linear trends for specified indicators.
        
        Args:
            df_long: Long-format dataframe
            indicator_codes: List of indicator codes to model
            
        Returns:
            List of TrendResult objects
        """
        print("=" * 60)
        print("Fitting Linear Trend Models | تركيب نماذج الاتجاه الخطي")
        print("=" * 60)
        
        self.results = []
        
        for code in indicator_codes:
            result = self._fit_single(df_long, code)
            if result:
                self.results.append(result)
                print(f"✓ {code}: R²={result.r_squared:.3f}, slope={result.slope:,.2f}")
        
        print(f"\nFitted {len(self.results)} models")
        return self.results
    
    def _fit_single(self, df_long: pd.DataFrame, indicator_code: str) -> Optional[TrendResult]:
        """Fit trend for a single indicator."""
        data = df_long[
            (df_long["Indicator Code"] == indicator_code) & 
            (df_long["value"].notna())
        ].copy()
        
        if len(data) < 5:
            return None
        
        x = data["year"].values
        y = data["value"].values
        
        # Least squares estimation
        n = len(x)
        x_mean, y_mean = x.mean(), y.mean()
        
        numerator = ((x - x_mean) * (y - y_mean)).sum()
        denominator = ((x - x_mean) ** 2).sum()
        
        if denominator == 0:
            return None
        
        slope = numerator / denominator
        intercept = y_mean - slope * x_mean
        
        # R-squared
        y_pred = slope * x + intercept
        ss_res = ((y - y_pred) ** 2).sum()
        ss_tot = ((y - y_mean) ** 2).sum()
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
        
        # MAPE
        mape = np.mean(np.abs((y - y_pred) / y)) * 100 if np.all(y != 0) else None
        
        name = data["Indicator Name"].iloc[0]
        
        return TrendResult(
            indicator_code=indicator_code,
            indicator_name=name,
            n_observations=n,
            slope=slope,
            intercept=intercept,
            r_squared=r2,
            mape=mape,
            direction="UP" if slope > 0 else "DOWN"
        )
    
    def get_summary_df(self) -> pd.DataFrame:
        """Return results as DataFrame."""
        if not self.results:
            return pd.DataFrame()
        
        return pd.DataFrame([
            {
                "Indicator": r.indicator_code,
                "Name": r.indicator_name[:50],
                "N": r.n_observations,
                "Slope": r.slope,
                "R²": r.r_squared,
                "MAPE": r.mape,
                "Direction": r.direction
            }
            for r in self.results
        ])


class EraClassifier:
    """
    Nearest-centroid classifier for historical era classification.
    
    Uses GDP, Exports, Imports, and Population to classify Iraq's historical periods.
    """
    
    def __init__(self):
        self.centroids: Dict[str, np.ndarray] = {}
        self.accuracy: float = 0.0
        self.class_accuracy: Dict[str, float] = {}
    
    def fit(self, df_long: pd.DataFrame) -> float:
        """
        Fit era classifier and calculate accuracy.
        
        Args:
            df_long: Long-format dataframe with era labels
            
        Returns:
            Overall classification accuracy
        """
        print("=" * 60)
        print("Era Classification | تصنيف الفترات التاريخية")
        print("=" * 60)
        
        # Key indicators for classification
        indicators = ["NY.GDP.MKTP.CD", "NE.EXP.GNFS.CD", "NE.IMP.GNFS.CD", "SP.POP.TOTL"]
        
        # Prepare data
        df_wide = self._prepare_features(df_long, indicators)
        
        if df_wide.empty:
            print("⚠ Insufficient data for classification")
            return 0.0
        
        # Calculate centroids per era
        self.centroids = self._calculate_centroids(df_wide)
        
        # Classify and evaluate
        predictions = df_wide.apply(
            lambda row: self._nearest_centroid(row[indicators].values), 
            axis=1
        )
        
        actual = df_wide["iraq_era"]
        
        # Overall accuracy
        correct = (predictions == actual).sum()
        total = len(actual)
        self.accuracy = correct / total if total > 0 else 0
        
        # Per-class accuracy
        for era in actual.unique():
            mask = actual == era
            era_correct = (predictions[mask] == era).sum()
            era_total = mask.sum()
            self.class_accuracy[era] = era_correct / era_total if era_total > 0 else 0
        
        print(f"✓ Overall Accuracy: {self.accuracy:.1%}")
        print(f"\nPer-Class Accuracy:")
        for era, acc in sorted(self.class_accuracy.items()):
            print(f"  {era}: {acc:.1%}")
        
        return self.accuracy
    
    def _prepare_features(self, df_long: pd.DataFrame, indicators: List[str]) -> pd.DataFrame:
        """Prepare feature matrix for classification."""
        # Filter to key indicators
        df_filtered = df_long[df_long["Indicator Code"].isin(indicators)].copy()
        
        if df_filtered.empty:
            return pd.DataFrame()
        
        # Pivot to wide format
        df_pivot = df_filtered.pivot_table(
            index="year",
            columns="Indicator Code",
            values="value",
            aggfunc="first"
        ).reset_index()
        
        # Add era labels
        era_map = df_filtered.groupby("year")["iraq_era"].first().to_dict()
        df_pivot["iraq_era"] = df_pivot["year"].map(era_map)
        
        # Drop rows with missing features
        df_pivot = df_pivot.dropna(subset=indicators)
        
        # Normalize features
        for col in indicators:
            if col in df_pivot.columns:
                mean = df_pivot[col].mean()
                std = df_pivot[col].std()
                if std > 0:
                    df_pivot[col] = (df_pivot[col] - mean) / std
        
        return df_pivot
    
    def _calculate_centroids(self, df_wide: pd.DataFrame) -> Dict[str, np.ndarray]:
        """Calculate centroids for each era."""
        centroids = {}
        indicators = ["NY.GDP.MKTP.CD", "NE.EXP.GNFS.CD", "NE.IMP.GNFS.CD", "SP.POP.TOTL"]
        
        for era in df_wide["iraq_era"].unique():
            era_data = df_wide[df_wide["iraq_era"] == era]
            if len(era_data) > 0:
                centroid = era_data[indicators].mean().values
                centroids[era] = centroid
        
        return centroids
    
    def _nearest_centroid(self, features: np.ndarray) -> str:
        """Find nearest centroid for given features."""
        min_dist = float("inf")
        nearest = None
        
        for era, centroid in self.centroids.items():
            dist = np.linalg.norm(features - centroid)
            if dist < min_dist:
                min_dist = dist
                nearest = era
        
        return nearest


class NaiveForecaster:
    """
    Naive forecasting using moving average.
    """
    
    def __init__(self, window: int = 3):
        self.window = window
        self.mape: Optional[float] = None
        self.rmse: Optional[float] = None
    
    def evaluate(self, df_long: pd.DataFrame, indicator_code: str) -> Dict:
        """
        Evaluate naive forecast for an indicator.
        
        Args:
            df_long: Long-format dataframe
            indicator_code: Indicator to forecast
            
        Returns:
            Dictionary with MAPE and RMSE
        """
        data = df_long[df_long["Indicator Code"] == indicator_code].copy()
        data = data.sort_values("year").reset_index(drop=True)
        
        # Create moving average forecast
        data["forecast"] = data["value"].rolling(window=self.window, min_periods=1).mean().shift(1)
        
        # Drop first row (no forecast)
        data = data.dropna(subset=["forecast"])
        
        if len(data) == 0:
            return {"mape": None, "rmse": None}
        
        actual = data["value"].values
        forecast = data["forecast"].values
        
        # Calculate metrics
        mape = np.mean(np.abs((actual - forecast) / actual)) * 100
        rmse = np.sqrt(np.mean((actual - forecast) ** 2))
        
        self.mape = mape
        self.rmse = rmse
        
        print(f"✓ Naive Forecast ({indicator_code}): MAPE={mape:.2f}%, RMSE={rmse:,.0f}")
        
        return {"mape": mape, "rmse": rmse}


if __name__ == "__main__":
    # Test models
    from data_loader import DataLoader
    from data_cleaner import DataCleaner
    from feature_engineer import FeatureEngineer
    
    print("\n" + "=" * 60)
    print("Testing Models | اختبار النماذج")
    print("=" * 60)
    
    # Load and prepare data
    loader = DataLoader()
    df, _, _ = loader.load_all()
    
    cleaner = DataCleaner(df)
    df_clean = cleaner.clean_all()
    
    engineer = FeatureEngineer(df_clean)
    df_long = engineer.engineer_all()
    
    # Test trend model
    trend_model = TrendModel()
    key_indicators = ["SP.POP.TOTL", "SP.DYN.LE00.IN", "NY.GDP.MKTP.CD"]
    results = trend_model.fit(df_long, key_indicators)
    
    print("\nTrend Model Summary:")
    print(trend_model.get_summary_df().to_string())
    
    # Test era classifier
    classifier = EraClassifier()
    accuracy = classifier.fit(df_long)
    
    # Test forecaster
    forecaster = NaiveForecaster(window=3)
    metrics = forecaster.evaluate(df_long, "SP.POP.TOTL")
