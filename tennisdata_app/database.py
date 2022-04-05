from typing import Any, Type, Union
import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine, Connection
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# TODO: get some decent stubs for pandas so I dont need all these type ignores

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
data_types: dict[str, Union[str, Type[str], Type[float]]] = {
    "ATP": int,
    "Location": str,
    "Tournament": str,
    "Date": "datetime64[ns]",
    "Series": str,
    "Court": str,
    "Surface": str,
    "Round": str,
    "Best of": int,
    "Winner": str,
    "Loser": str,
    "WRank": int,
    "LRank": int,
    "WPts": int,
    "LPts": int,
    "W1": int,
    "L1": int,
    "W2": int,
    "L2": int,
    "W3": int,
    "L3": int,
    "W4": int,
    "L4": int,
    "W5": int,
    "L5": int,
    "Wsets": int,
    "Lsets": int,
    "Comment": str,
    "B365W": float,
    "B365L": float,
    "EXW": float,
    "EXL": float,
    "LBW": float,
    "LBL": float,
    "PSW": float,
    "PSL": float,
    "SJW": float,
    "SJL": float,
    "MaxW": float,
    "MaxL": float,
    "AvgW": float,
    "AvgL": float,
}

# endregion: maps


# ideally this should be handled entirely in crud.py, and I don't like how hacky this method of insertion is.
def import_data(con: Union[Engine, Connection], data: Any, replace: bool = True) -> int:
    """
    Import data from an excel file into the database.

    :param con: database connection.
    :param data: excel file.
    :param replace: whether to drop existing database.
    """
    try:
        df: pd.DataFrame = pd.read_excel(data)  # type: ignore[attr-defined]
    except ValueError:
        raise ValueError("Invalid Excel file.")
    df = sanitise_data(df)
    # generate unique id for each row. type ignore because bad stubs
    df.insert(0, "id", df.apply(generate_id_from_row, axis=1))  # type: ignore[arg-type]
    # I have absolutely no idea what mypy is complaining about for these two.
    df = df.rename(name_map, axis="columns")  # type: ignore[call-overload]
    rows_affected = df.to_sql(  # type: ignore[operator]
        "games", con, if_exists="replace" if replace else "append", index=False
    )
    return rows_affected or 0


def sanitise_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Check column names, and ensure all data types are correct.

    :param df: dataframe to sanitise.
    :return: sanitised dataframe.
    """
    if set(df.columns) != set(name_map.keys()):
        raise ValueError(f"{list(df.columns)}\n{name_map.keys()}")
    # fill missing values with 0
    dtype_int = [col for col, dtype in data_types.items() if dtype == int]
    df[dtype_int] = df[dtype_int].fillna(0)
    df = df.astype(data_types)  # type: ignore[arg-type]
    return df


# mypy wants type params for row, but giving them causes a type error at runtime.
def generate_id_from_row(row: pd.Series) -> str:  # type: ignore[type-arg]
    """
    Generate a unique id from a single game row.

    :param row: row of data.
    :return: unique id.
    """
    datestr = row["Date"].strftime("%Y%m%d")
    # theoretically this could fail if two players play each other twice on the same day with the same winner.
    # I doubt that this would actually happen in a tournament.
    return f"{datestr}_{row['Winner']}_{row['Loser']}".replace(" ", "").replace(".", "")
