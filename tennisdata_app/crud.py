from typing import Optional, Union, Any
from sqlalchemy.orm import Session

from . import models, database
from .models import Game

DEFAULT_LIMIT = 10

Filter = dict[str, Union[int, str, None]]


def get_game(db: Session, game_id: str) -> Optional[Game]:
    """
    Get game by id.
    """
    return db.query(models.Game).filter(models.Game.id == game_id).first()


def get_games_by_filter(db: Session, filter: Filter, skip: int = 0, limit: int = DEFAULT_LIMIT) -> list[Game]:
    """
    Get games by filter. Filter should be a dictionary with keys matching the column names in the database,
    and their expected values.
    """
    filter = {k: v for k, v in filter.items() if v is not None}
    return db.query(models.Game).filter_by(**filter).offset(skip).limit(limit).all()


# see comment on shortcut in database.py
# TODO: figure out a proper type hint for file
def update_games_from_file(db: Session, file: Any, replace: bool = True) -> int:
    return database.import_data(db.get_bind(), file, replace)
