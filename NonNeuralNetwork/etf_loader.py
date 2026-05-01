## Load ETF Data for Regression  analysis using yfinance API

# Principal API, DS Libraries, yfinance
import yfinance as yfi
import pandas as pd

import os

# DB Imports
from db_utils import upsert_daily_OHLCV

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

def input_derived_technicals (df: pd.DataFrame,
                              symbol: str,
                              *,
                              write_to_csv = True,
                              write_to_db = True) -> pd.DataFrame:
    """
    Derives and inserts technicals for each index into df: RSI, MACD
    """

    """
    Relative Strength Index (RSI): Oscillator value indicating the acceleration of the stock price's movement 
    - Uses delta between current index's closing price and previous closing price
    - Delta(P_i) = P_i - P_i-1      (st. P_i is the closing Price of closing for stock @ index i)
    - RSI is moving average of deltas over a window size, N
    - Moving average derived as Average Gain
    """

    derived_df = df.copy()              # utilize clean copy of data frame 
    N = 14                      # Window Size (N): Set Number of Indices/Periods used to calculate RSI (default is 14)

    delta = derived_df['Close'].diff()  # Use difference in values in 'close' column as delta
    
    gain = delta.clip(lower = 0)        # ??
    loss = -1 * delta.clip(upper = 0)   # ??

    # Derive Moving Average
    avg_gain = gain.ewm(com = N - 1, adjust = False).mean()
    avg_loss = loss.ewm(com = N - 1, adjust = False).mean()

    # Derive Relative Strenth (RS) as Ratio of Averages between gain and less
    rs = avg_gain / avg_loss

    # Normalize Relative Strength (RS) to achieve RSI
    derived_df['RSI'] = 100 - (100 / (1 + rs))


    """
    Moving Average Convergence Divergence (MACD)
    - Compares short-term average with longer-term average
    - Indicates whether stock is trending faster or slower relative to its usual movement 
    """

    # Standard MACD Params
    k_fast = 12
    k_slow = 26
    k_signal = 9

    # Derive Fast and Slow (Small and Large Windows) Moving Average
    ex_moving_avg_fast = derived_df['Close'].ewm(span = k_fast, adjust = False).mean()
    ex_moving_avg_slow = derived_df['Close'].ewm(span = k_slow, adjust = False).mean()    

    # Define MACD Delta (Difference between Fast and Slow EMAs)
    derived_df['MACD_Line'] = ex_moving_avg_fast - ex_moving_avg_slow

    # Define Signal Line
    derived_df['MACD_Signal'] = derived_df['MACD_Line'].ewm(span = k_signal, adjust = False).mean()

    # Define Histogram via delta of MACD and Signal Lines
    derived_df['MACD_Histogram'] = derived_df['MACD_Line'] - derived_df['MACD_Signal']      # Key feature for NN

    
    ## ADD TECHNICALS 


    # Temporary Dual-Writing Implementation
    # Save updated dataframe to directory as CSV, as well as a set of entities to SQL Database

    if write_to_csv:                                                # Write to CSV if coressponding boolean set to true
        derived_df.to_csv (r'C:\Users\merc1\OneDrive\Stock_Pred_ML\NonNeuralNetwork\history_technicals' + '\\' + symbol + 'hist_w_features.csv')
    
    if write_to_db:                                                 # Write to DB if coressponding boolean set to true
        rows_written = upsert_daily_OHLCV(derived_df, symbol)
        print (f"SQLite upsert complete fror {symbol}: {rows_written} rows written.")

    return derived_df

# Example/Debug Method Calls
if __name__ == "__main__":
    # Test for history extraction method (get_hist_over_range)
    etf_symbol = "MU"
    hist = get_hist_over_range (etf_symbol, period = "10y" , interval = "1d")
    history_with_technicals = input_derived_technicals(hist, etf_symbol)
    print ("Historial Data and Technicals for Symbol: " + etf_symbol)
    print(history_with_technicals)

    #TODO: Parameterize ETF symbol