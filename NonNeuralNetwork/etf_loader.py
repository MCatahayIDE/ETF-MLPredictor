## Load ETF Data for Regression  analysis using yfinance API

#Principal Library, yfinance
import yfinance as yfi

import pandas as pd
import os

from datetime import datetime
from typing import Optional, Iterable

def get_hist_over_range (
    symbol : str,        # Indicate ETF by symbol
    period : str = "1y",  # Indicate Duration/Range of data; Defaults to 1 year
    interval : str = "1d",
    start: Optional[str] = None,
    end: Optional[str] = None,
    auto_adjust : bool = True,
    prepost : bool = False,
) -> pd.DataFrame:  # DataFrame return type
    "Fetches historical data"

    ticker = yfi.Ticker(symbol)

    dframe = ticker.history (
        period = period,
        interval = interval,
        auto_adjust = auto_adjust,
        prepost = prepost
    )

    # Temporary implementation; saves generated history to CSV denoted with symbol name
    dframe.to_csv (r'C:\Users\merc1\OneDrive\Stock_Pred_ML\NonNeuralNetwork\etf_historical' + '\\' + symbol + '_hist.csv')

    return dframe 

def get_quote (symbol : str) -> pd.DataFrame:
    "Fetches quote information"

    ticker = yfi.Ticker(symbol)

def get_bulk_hist (
        symbol : Iterable[str],        # Indicate ETF by symbol
        period : str = "10y",           # Indicate Duration/Range of data; Defaults to 1 year
        interval : str = "1d",         # Interaval of data sample
        auto_adjust : bool = True
) -> dict[str, pd.DataFrame]: 
    "Fetches historical data in bulk for multiple symbols"
    pass

def save_hist_csv ( dframe : pd.DataFrame, filepath : str ) -> None:
    pass

# Example/Debug Method Calls
if __name__ == "__main__":
    # Test for history extraction method (get_hist_over_range)
    etf_symbol = "AAPL"
    hist = get_hist_over_range (etf_symbol, period = "10y" , interval = "1d")
    print ("Historial Data for Symbol: " + etf_symbol)
    print(hist)