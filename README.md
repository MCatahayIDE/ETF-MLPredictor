# Automated E2E ML Pipeline Stock/ETF Forecasting and Predictive Modeling


This pipeline is designed to automate the full lifecycle of financial data including safe ingestion via API, feature engineering, and safe database storage to use as high-signal training data for well-tuned machine learning models. With this robust pipeline, the program possesses a robust framework primed for automated, systematic financial inference and accurate predictive modeling. 
## Primary Features

**Modularized ETL (Extract, Transform, Load) Pipeline:** Safely orchestrates the flow of market data from ingestion via **yfinance** into CSV format for smoothly append derived technical indicators and additional feature engineering. The CSV data is then transferred to a structured, queryable SQLite database currently using a dual-write and utility implementation. 

**Feature Engineering Market Technical Indicators:** Captures hidden trends by implementing important mathematical indicators such as rolling averages like RSI, and price movement acceleration via MACD (Line, Signal, and Histogram). Combined, these metrics provide the core machine learning models with an important context field to capture underlying momentum and trend signals.  

**Leak-Proof Labeling Strategy:** Targets the percentage change of the closing price (`pct_change`) rather than raw price values, mitigating the risks of non-stationarity and data leakage inherent in financial time-series.

**Multi-Model Experimentation Framework:** Supports a pluggable modeling architecture featuring LightGBM, Random Forest, and Linear Regression implementations for comparative performance analysis. More models intended to be implemented in future.



## Pipeline Architecture

Text goes here.

## Installation, Setup Configuration

Text goes here.
## On The Horizon

- **Near Future**
	- EdgeML Deployment onto Pi 5
	- **State Space Model (SSM) Implementation**
 
- **Future**
	- Cloud Deployment and Updating Via Azure/AWS

