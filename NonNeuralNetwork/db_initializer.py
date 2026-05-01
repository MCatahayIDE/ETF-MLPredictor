# Script for instantiating database instance and creating tables

# imports
from sqlalchemy import inspect
from db_utils import init_db_engine
from db_outline import Base                                         # Reference db_outline to create database using schema
import db_config

def init_db (* , echo: bool = False) -> None:
    ##       ^                           ^
    engine = init_db_engine(echo = echo)
    Base.metadata.create_all(engine)
    
    inspector = inspect(engine)
    print(f"SQLite file: {db_config.DB_PATH}")                      # Echo path to db
    print("Tables: " , inspector.get_table_names())                 # Echo db table name(s)


if __name__ == "__main__":
    init_db(echo = False)                                           # In main, instantiate init_db