## Configure DB Engine to manage SQLite DB and Connection to DB

# SQLA, Pandas
from sqlalchemy import create_engine
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
import pandas as pd

# Script Function Imports
import db_config
from db_outline import ETF_OHLCV_Daily


def init_db_engine (* , echo: bool = False):
    ##              ^                                               ??
    ## Uses db url from db_config and is passed behavior params
    return create_engine(db_config.SQLA_DB_URL, echo = echo, future = True)

def _to_db_rows (df: pd.DataFrame, symbol: str) -> list[dict]:
    if df is None or df.empty:
        return []
    
    frame = df.copy()

    if "Date" in frame.columns:
        dt = pd.to_datatime(frame["Date"], utc = True, errors = "coerce")
    else:
        dt = pd.to_datatime(frame.index, utc = True , errors = "coerce")

    # Normalize timezone-aware timestaps
    index_date = dt.tz_localize(None).date

    rows = pd.DataFrame (
        {        
            "ETF_ticker": symbol.upper(),
            "Index_date": index_date,
            "open_price": pd.to_numeric(frame.get("Open"), errors="coerce"),
            "high": pd.to_numeric(frame.get("High"), errors="coerce"),
            "low": pd.to_numeric(frame.get("Low"), errors="coerce"),
            "close_price": pd.to_numeric(frame.get("Close"), errors="coerce"),
            "volume": pd.to_numeric(frame.get("Volume"), errors="coerce"),
            "dividends": pd.to_numeric(frame.get("Dividends"), errors="coerce"),
            "stock_splits": pd.to_numeric(frame.get("Stock Splits"), errors="coerce"),
            "rsi": pd.to_numeric(frame.get("RSI"), errors="coerce"),
            "macd_line": pd.to_numeric(frame.get("MACD_Line"), errors="coerce"),
            "macd_signal": pd.to_numeric(frame.get("MACD_Signal"), errors="coerce"),
            "macd_histogram": pd.to_numeric(frame.get("MACD_Histogram"), errors="coerce"),
        }
    )

    rows = rows.dropna(subset = ["Index_date"])
    rows = rows.where(pd.notna(rows) , None)
    return rows.to_dict(orient = "records")

def upsert_daily_OHLCV (df: pd.DataFrame, symbol: str, *, echo: bool = False) -> int:
    rows = _to_db_rows(df, symbol)
    if not rows:                                                    # Exit if passed in table is empty
        return 0
    
    engine = init_db_engine(echo = echo)                            # ???
    table = ETF_OHLCV_Daily.__table__                               # ???

    insert_entities = sqlite_insert(table).values(rows)             # ???
    update_columns = {
        col.name: insert_entities.excluded[col.name]
        for col in table.columns
        if col.name not in {"ETF_ticker" , "Index_date"}
    }

    upsert_entities = insert_entities.on_conflict_do_update(        # ???
        index_elements= ["ETF_ticker" , "Index_date"],
        set_ = update_columns,
    )

    with engine.begin() as conn:
        conn.execute(upsert_entities)
    
    return len(rows)




        