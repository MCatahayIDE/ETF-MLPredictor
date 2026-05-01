# Schema for Database

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Date, Float, BigInteger, PrimaryKeyConstraint

Base = declarative_base()

class ETF_OHLCV_Daily(Base):
    __tablename__ = "ETF_data_daily"

    # Define Feature Columns

    ETF_ticker = Column(String(16), nullable = False)               # ETF symbol required, can't be null val
    Index_date = Column(Date, nullable = False)                     # Date of indexed data must be valid, not null

    # Fundamental Data, OHLV
    open_price = Column(Float, nullable = True)
    high = Column(Float, nullable = True)
    low = Column(Float, nullable = True)
    close_price = Column(Float, nullable = True)
    volume = Column(BigInteger, nullable = True)                   # Big Integer better for volume measured in millions or billions

    # Dividends, Splits
    dividends = Column(Float, nullable = True)
    stock_splits = Column (Float, nullable = True)

    # Derived Technicals
    rsi = Column(Float, nullable = True)
    macd_line = Column(Float, nullable = True)
    macd_signal = Column(Float, nullable = True)
    macd_histogram = Column(Float, nullable = True)

    __table_args__ = (
        PrimaryKeyConstraint("ETF_ticker" , "Index_date" , name = "pk_ETF_data_daily"),
    )
