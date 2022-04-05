from typing import IO, Union
import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine, Connection
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import Integer, String, Float, Date

# Perhaps this should be set in a dotenv?
SQLALCHEMY_DATABASE_URL = "sqlite:///./tennisdata_app.db"
DEBUG = False

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=DEBUG)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# region: maps

# map from tennis-data.co.uk names to more pythonic names
name_map = {
    "ATP": "ATP",
    "Location": "location",
    "Tournament": "tournament",
    "Date": "date",
    "Series": "series",
    "Court": "court",
    "Surface": "surface",
    "Round": "round",
    "Best of": "best_of",
    "Winner": "winner",
    "Loser": "loser",
    "WRank": "w_rank",
    "LRank": "l_rank",
    "WPts": "w_pts",
    "LPts": "l_pts",
    "W1": "w1",
    "L1": "l1",
    "W2": "w2",
    "L2": "l2",
    "W3": "w3",
    "L3": "l3",
    "W4": "w4",
    "L4": "l4",
    "W5": "w5",
    "L5": "l5",
    "Wsets": "w_sets",
    "Lsets": "l_sets",
    "Comment": "comment",
    "B365W": "b365_w",
    "B365L": "b365_l",
    "EXW": "ex_w",
    "EXL": "ex_l",
    "LBW": "lb_w",
    "LBL": "lb_l",
    "PSW": "ps_w",
    "PSL": "ps_l",
    "SJW": "sj_w",
    "SJL": "sj_l",
    "MaxW": "max_w",
    "MaxL": "max_l",
    "AvgW": "avg_w",
    "AvgL": "avg_l",
}

# enforce column data types
data_types = {
    "id": Integer(),
    "ATP": Integer(),
    "location": String(),
    "tournament": String(),
    "date": Date(),
    "series": String(),
    "court": String(),
    "surface": String(),
    "round": String(),
    "best_of": Integer(),
    "winner": String(),
    "loser": String(),
    "w_rank": Integer(),
    "l_rank": Integer(),
    "w_pts": Integer(),
    "l_pts": Integer(),
    "w1": Integer(),
    "l1": Integer(),
    "w2": Integer(),
    "l2": Integer(),
    "w3": Integer(),
    "l3": Integer(),
    "w4": Integer(),
    "l4": Integer(),
    "w5": Integer(),
    "l5": Integer(),
    "w_sets": Integer(),
    "l_sets": Integer(),
    "comment": String(),
    "b365_w": Float(),
    "b365_l": Float(),
    "ex_w": Float(),
    "ex_l": Float(),
    "lb_w": Float(),
    "lb_l": Float(),
    "ps_w": Float(),
    "ps_l": Float(),
    "sj_w": Float(),
    "sj_l": Float(),
    "max_w": Float(),
    "max_l": Float(),
    "avg_w": Float(),
    "avg_l": Float(),
}

# endregion: maps


# ideally I would validate imported data instead of copying it into the database, as currently it is
# possible for some of the input to be invalid, which causes an error upon a get request for that row.
# bit annoying that pandas doesn't do this for me even with dtype=data_types :/
# it would also be better for this to be handled entirely in crud.py, and ideally without the extra
# pandas dependancy

# BUG: Data is not sanity checked before being imported, which can corrupt the database.
# BUG: Since pandas indexes always start from 0, if there is already data present in the database,
# appending will fail due to duplicate primary keys.
def import_data(con: Union[Engine, Connection], data: IO, replace: bool = True) -> int:
    """
    Import data from an excel file into the database.

    :param con: database connection.
    :param data: excel file.
    :param replace: whether to drop existing database.
    """
    # import from excel data
    df: pd.DataFrame = pd.read_excel(data)
    # rename columns
    df = df.rename(name_map, axis="columns")
    # use dataframe row index as id
    rows_affected = df.to_sql(
        "games",
        con,
        if_exists="replace" if replace else "append",
        index_label="id",
        dtype=data_types,
    )
    return rows_affected or 0
