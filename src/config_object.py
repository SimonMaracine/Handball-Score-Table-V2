from dataclasses import dataclass
from typing import List
from PIL import Image


@dataclass
class Config:
    team1: str
    team2: str
    players1: List[str]
    players2: List[str]
    numbers1: List[str]
    numbers2: List[str]
    match: int
    timeout: int
    suspend: int
    logo1: Image
    logo2: Image
