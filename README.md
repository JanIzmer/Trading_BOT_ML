# Bybit_trading_bot
Bybit_trading_bot
Trading Bot with Machine Learning

This repository contains a trading bot based on a two-stage machine learning model. It is designed to generate BUY, SELL, or HOLD signals using historical market data and technical indicators.

## 📁 Project Structure

# Bybit_trading_bot
Bybit_trading_bot
Trading Bot with Machine Learning

This repository contains a trading bot based on a two-stage machine learning model. It is designed to generate BUY, SELL, or HOLD signals using historical market data and technical indicators.

## 📁 Project Structure

├── core/ # Contains all logic for strategy and data preprocessing
├── static/ # Stores CSV files with historical asset prices and generated reports with plots
├── tests/ # Backtesting and testing logic
├── .gitignore # Files and folders excluded from version control
├── README.md # Project overview (you are here)
├── main.py # Main execution script for generating reports
├── polling_bot.py # Script for generating live trading signals using trained models
├── requirements.txt # Python dependencies
├── stage1_model.pkl # Trained model for stage 1 (Trade vs Hold)
├── stage2_model.pkl # Trained model for stage 2 (Buy vs Sell)
├── users.json # Sample user data (for access control or signal delivery) ```


## 🔍 Description

- **Core module (`core/`)**: Contains all strategy logic and data preparation functions. It handles technical indicators and formatting for model input.
- **Static directory (`static/`)**: Includes:
  - `data/`: CSV files with historical market prices
  - `reports/`: Output plots from backtesting
- **Models**:
  - `stage1_model.pkl`: Decides whether to enter a trade
  - `stage2_model.pkl`: Determines trade direction (BUY or SELL)

## 🚀 Usage

To run backtests and generate reports:

```bash
pytest -s tests/

## 🔍 Description

- **Core module (`core/`)**: Contains all strategy logic and data preparation functions. It handles technical indicators and formatting for model input.
- **Static directory (`static/`)**: Includes:
  - `data/`: CSV files with historical market prices
  - `reports/`: Output plots from backtesting
- **Models**:
  - `stage1_model.pkl`: Decides whether to enter a trade
  - `stage2_model.pkl`: Determines trade direction (BUY or SELL)

## 🚀 Usage

To run backtests and generate reports:

```bash
pytest -s tests/
