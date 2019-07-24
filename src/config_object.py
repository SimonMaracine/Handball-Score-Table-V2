from dataclasses import dataclass


@dataclass
class Config:
    team1: str
    team2: str
    players1: list
    players2: list
    numbers1: list
    numbers2: list
    match: int
    timeout: int
    suspend: int
