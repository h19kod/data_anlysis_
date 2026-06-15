#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main Analysis Script | سكريبت التحليل الرئيسي
==============================================

Run complete analysis pipeline from command line.

Usage | الاستخدام:
    python scripts/run_analysis.py [--output-dir OUTPUT_DIR]

Example | مثال:
    python scripts/run_analysis.py --output-dir outputs/
"""

import sys
import os
import argparse
from pathlib import Path

# Add parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data_loader import DataLoader
from src.data_cleaner import DataCleaner
from src.feature_engineer import FeatureEngineer
from src.models import TrendModel, EraClassifier, NaiveForecaster
from src.utils import ensure_dir, save_results, setup_logging


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Iraq WDI Analysis Pipeline | خط أنابيب تحليل مؤشرات العراق"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="outputs",
        help="Directory for output files | دليل ملفات الإخراج"
    )
    parser.add_argument(
        "--save-formats",
        nargs="+",
        default=["csv"],
        choices=["csv", "excel", "pickle"],
        help="Output formats | صيغ الإخراج"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging | تفعيل التسجيل المفصل"
    )
    
    return parser.parse_args()


def main():
    """Run complete analysis pipeline."""
    # Parse arguments
    args = parse_arguments()
    
    # Setup logging
    log_level = "INFO" if args.verbose else "WARNING"
    logger = setup_logging(level=getattr(__import__("logging"), log_level))
    
    print("=" * 70)
    print("  Iraq WDI Analysis Pipeline | خط أنابيب تحليل مؤشرات العراق")
    print("=" * 70)
    print()
    
    # Ensure output directories
    output_dir = ensure_dir(args.output_dir)
    data_output_dir = ensure_dir(os.path.join(output_dir, "processed_data"))
    reports_dir = ensure_dir(os.path.join(output_dir, "reports"))
    
    # ================================
    # Step 1: Load Data
    # ================================
    print("📥 Step 1: Loading Data | تحميل البيانات")
    print("-" * 50)
    
    loader = DataLoader()
    df, df_country, df_indicator = loader.load_all()
    
    validation = loader.validate_data()
    if not validation["valid"]:
        print("❌ Data validation failed! | فشل التحقق من البيانات!")
        return 1
    
    print("✅ Data loaded successfully | تم تحميل البيانات بنجاح")
    print(f"   Main data: {df.shape}")
    print()
    
    # ================================
    # Step 2: Clean Data
    # ================================
    print("🧹 Step 2: Cleaning Data | تنظيف البيانات")
    print("-" * 50)
    
    cleaner = DataCleaner(df)
    df_clean = cleaner.clean_all()
    
    cleaning_summary = cleaner.get_cleaning_summary()
    print(f"✅ Data cleaned | تم تنظيف البيانات")
    print(f"   Final shape: {cleaning_summary['final_shape']}")
    print(f"   Completeness: {cleaning_summary['completeness_pct']:.1f}%")
    print()
    
    # Save cleaned data
    save_results(
        df_clean,
        os.path.join(data_output_dir, "iraq_wdi_cleaned"),
        formats=args.save_formats
    )
    print()
    
    # ================================
    # Step 3: Engineer Features
    # ================================
    print("⚙️  Step 3: Engineering Features | هندسة المتغيرات")
    print("-" * 50)
    
    engineer = FeatureEngineer(df_clean)
    df_long = engineer.engineer_all()
    
    feature_summary = engineer.get_feature_summary()
    print(f"✅ Features engineered | تم هندسة المتغيرات")
    print(f"   Final shape: {feature_summary['shape']}")
    print(f"   Total features: {feature_summary['total_features']}")
    print()
    
    # Save engineered data
    save_results(
        df_long,
        os.path.join(data_output_dir, "iraq_wdi_engineered"),
        formats=args.save_formats
    )
    print()
    
    # ================================
    # Step 4: Model Trends
    # ================================
    print("📈 Step 4: Modeling Trends | نمذجة الاتجاهات")
    print("-" * 50)
    
    key_indicators = [
        "SP.POP.TOTL",       # Population
        "SP.DYN.LE00.IN",    # Life Expectancy
        "NY.GDP.MKTP.CD",    # GDP
        "NE.EXP.GNFS.CD",    # Exports
    ]
    
    trend_model = TrendModel()
    trend_results = trend_model.fit(df_long, key_indicators)
    
    # Save trend results
    trend_df = trend_model.get_summary_df()
    if not trend_df.empty:
        save_results(
            trend_df,
            os.path.join(reports_dir, "trend_model_results"),
            formats=args.save_formats
        )
    print()
    
    # ================================
    # Step 5: Classify Eras
    # ================================
    print("🏛️  Step 5: Classifying Historical Eras | تصنيف الفترات التاريخية")
    print("-" * 50)
    
    classifier = EraClassifier()
    accuracy = classifier.fit(df_long)
    
    print(f"✅ Era classification complete | اكتمل تصنيف الفترات")
    print(f"   Overall accuracy: {accuracy:.1%}")
    print()
    
    # ================================
    # Step 6: Forecast Evaluation
    # ================================
    print("🔮 Step 6: Evaluating Forecasts | تقييم التنبؤات")
    print("-" * 50)
    
    forecaster = NaiveForecaster(window=3)
    forecast_metrics = forecaster.evaluate(df_long, "SP.POP.TOTL")
    
    print(f"✅ Forecast evaluation complete | اكتمل تقييم التنبؤ")
    print(f"   MAPE: {forecast_metrics.get('mape', 0):.2f}%")
    print()
    
    # ================================
    # Summary
    # ================================
    print("=" * 70)
    print("  Analysis Complete! | اكتمل التحليل!")
    print("=" * 70)
    print()
    print("📁 Output Files | ملفات الإخراج:")
    print(f"   • Cleaned data: {data_output_dir}")
    print(f"   • Engineered data: {data_output_dir}")
    print(f"   • Reports: {reports_dir}")
    print()
    print("✨ Done! | تم!")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
