"""
Setup script for Iraq WDI Analysis package
============================================

Install with: pip install -e .
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    with open(requirements_file, encoding="utf-8") as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="iraq-wdi-analysis",
    version="1.0.0",
    author="h19kod",
    author_email="h19kod@github.com",
    description="Professional data analysis of Iraq's World Development Indicators",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/h19kod/data_anlysis_",
    project_urls={
        "Bug Reports": "https://github.com/h19kod/data_anlysis_/issues",
        "Source": "https://github.com/h19kod/data_anlysis_",
        "Documentation": "https://github.com/h19kod/data_anlysis_/blob/main/docs/PROJECT_OVERVIEW.md",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
        ],
        "viz": [
            "matplotlib>=3.4.0",
            "seaborn>=0.11.0",
            "plotly>=5.0.0",
        ],
        "ml": [
            "scikit-learn>=1.0.0",
            "statsmodels>=0.13.0",
            "prophet>=1.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "iraq-wdi=scripts.run_analysis:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
