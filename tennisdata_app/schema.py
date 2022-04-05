from typing import Optional
from datetime import date

from pydantic import BaseModel


class Game(BaseModel):
    """
    Pydantic model for a tennis game.
    """

    id: int
    ATP: int
    location: str
    tournament: str
    date: date
    series: str
    court: str
    surface: str
    round: str
    best_of: int
    winner: str
    loser: str
    w_rank: int
    l_rank: Optional[int]
    w_pts: int
    l_pts: Optional[int]
    w1: Optional[int]
    l1: Optional[int]
    w2: Optional[int]
    l2: Optional[int]
    w3: Optional[int]
    l3: Optional[int]
    w4: Optional[int]
    l4: Optional[int]
    w5: Optional[int]
    l5: Optional[int]
    w_sets: Optional[int]
    l_sets: Optional[int]
    comment: str
    b365_w: Optional[float]
    b365_l: Optional[float]
    ex_w: Optional[float]
    ex_l: Optional[float]
    lb_w: Optional[float]
    lb_l: Optional[float]
    ps_w: Optional[float]
    ps_l: Optional[float]
    sj_w: Optional[float]
    sj_l: Optional[float]
    max_w: Optional[float]
    max_l: Optional[float]
    avg_w: Optional[float]
    avg_l: Optional[float]

    # for sqlalchemy
    class Config:
        orm_mode = True


class UploadResponse(BaseModel):
    """
    Pydantic model for file upload response.
    """

    affected_rows: int
