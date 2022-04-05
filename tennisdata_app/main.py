from typing import Generator, NoReturn, Optional, Any
from fastapi import Depends, FastAPI, HTTPException, File
from sqlalchemy.orm import Session
from sqlalchemy.exc import StatementError

from . import crud, models, schema
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)  # type: ignore[attr-defined]

# TODO: Title, description, version, ect.
app = FastAPI()


def get_db() -> Generator[Any, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", include_in_schema=False)
def read_root() -> NoReturn:
    raise HTTPException(status_code=418, detail="I'm a Teapot. Looking for docs? See /docs.")


@app.get("/games/{game_id}", response_model=schema.Game, summary="Get game by id")
def read_game(game_id: str, db: Session = Depends(get_db)) -> models.Game:
    """
    Read game by id.

    - **game_id**: The id of the game to read.
    """
    game = crud.get_game(db, game_id=game_id)
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return game


@app.get("/games/", response_model=list[schema.Game], summary="Get games by filter")
def read_games(
    skip: int = 0,
    limit: int = crud.DEFAULT_LIMIT,
    id: Optional[int] = None,
    ATP: Optional[int] = None,
    location: Optional[str] = None,
    tournament: Optional[str] = None,
    date: Optional[str] = None,
    series: Optional[str] = None,
    court: Optional[str] = None,
    surface: Optional[str] = None,
    round: Optional[str] = None,
    winner: Optional[str] = None,
    loser: Optional[str] = None,
    db: Session = Depends(get_db),
) -> list[models.Game]:
    """
    Read multiple games by filter.

    - **skip**: The number of indexes to skip.
    - **limit**: The maximum number of games to return.
    - **id**: Exact ID of a game to read.
    - **ATP**: Tournament number.
    - **location**: Venue of tournament.
    - **tournament**: Name of tournament.
    - **date**: Date of tournament. Formatted as YYYY-MM-DD.
    - **series**: Series of tournament.
    - **court**: Type of court (indoor, outdoor).
    - **surface**: Type of surface (hard, clay, carpet or grass).
    - **round**: Round of tournament.
    - **winner**: Name of game winner.
    - **loser**: Name of game loser.
    """
    filter = {
        "id": id,
        "ATP": ATP,
        "location": location,
        "tournament": tournament,
        "date": date,
        "series": series,
        "court": court,
        "surface": surface,
        "round": round,
        "winner": winner,
        "loser": loser,
    }
    games = crud.get_games_by_filter(db, filter=filter, skip=skip, limit=limit)
    return games


@app.post("/games/upload/", response_model=schema.UploadResponse, summary="Upload games from file")
async def upload_data(file: bytes = File(...), replace: bool = True, db: Session = Depends(get_db)) -> dict[str, int]:
    """
    Upload games to database from Excel file.

    - **file**: The Excel file to upload.
    - **replace**: If True, replace existing database, else, append to it.
    """
    try:
        updated_rows = crud.update_games_from_file(db, file, replace)
        return {"affected_rows": updated_rows}
    except StatementError as statement_error:
        if type(statement_error.orig) is TypeError:
            raise HTTPException(status_code=422, detail="Invalid data in file")
        else:
            # TODO: handle properly
            raise HTTPException(status_code=500, detail="Internal server error")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=e.args[0])
