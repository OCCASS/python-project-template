import datetime
from typing import List

from pydantic import BaseModel


class League(BaseModel):
    id: int
    name: str


class Market(BaseModel):
    type: str
    type_name: str
    line: str
    odds: float


class Match(BaseModel):
    id: int
    name: str
    url: str
    league: League
    sport: str
    start_time: datetime.datetime
    markets: List[Market] = []


class PinnacleEvent(BaseModel):
    match_id: int
    match: Match
    market: Market
