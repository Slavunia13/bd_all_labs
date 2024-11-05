from pydantic import BaseModel

class Team(BaseModel):
    id: str | None = None
    name: str
    city: str
    coach: str
    starting_lineup: list[str] # ids of players
    substitutes: list[str] # ids of players

class Player(BaseModel):
    id: str | None = None
    full_name: str
    position: str
    goals: int = 0

class Goal(BaseModel):
    author_id: str
    position: str
    minute: int
    assist_id: str | None = None

class Match(BaseModel):
    id: str | None = None
    date: str
    team_ids: list[str] # [team1, team2]
    score: str
    goals: list[Goal]
