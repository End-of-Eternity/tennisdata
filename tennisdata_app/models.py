from sqlalchemy import Date, Column, Integer, String, Float

from .database import Base


class Game(Base):
    """
    SQLAlchemy model for a tennis game.

    For a description of what each column represents, see `http://www.tennis-data.co.uk/notes.txt`.
    """

    __tablename__ = "games"

    id = Column(String, primary_key=True, index=True)
    ATP = Column(Integer, index=True)
    location = Column(String, index=True)
    tournament = Column(String, index=True)
    date = Column(Date, index=True)
    series = Column(String, index=True)
    court = Column(String, index=True)
    surface = Column(String, index=True)
    round = Column(String, index=True)
    best_of = Column(Integer)
    winner = Column(String, index=True)
    loser = Column(String, index=True)
    w_rank = Column(Integer)
    l_rank = Column(Integer)
    w_pts = Column(Integer)
    l_pts = Column(Integer)
    w1 = Column(Integer)
    l1 = Column(Integer)
    w2 = Column(Integer)
    l2 = Column(Integer)
    w3 = Column(Integer)
    l3 = Column(Integer)
    w4 = Column(Integer)
    l4 = Column(Integer)
    w5 = Column(Integer)
    l5 = Column(Integer)
    w_sets = Column(Integer)
    l_sets = Column(Integer)
    comment = Column(String)
    b365_w = Column(Float)
    b365_l = Column(Float)
    ex_w = Column(Float)
    ex_l = Column(Float)
    lb_w = Column(Float)
    lb_l = Column(Float)
    ps_w = Column(Float)
    ps_l = Column(Float)
    sj_w = Column(Float)
    sj_l = Column(Float)
    max_w = Column(Float)
    max_l = Column(Float)
    avg_w = Column(Float)
    avg_l = Column(Float)
