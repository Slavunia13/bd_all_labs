from pydantic import BaseModel

class Athlete(BaseModel):
    name: str

class Judge(BaseModel):
    name: str

class ScoreUpdate(BaseModel):
    judge: str
    athlete: str
    score: int

class AthleteScore(BaseModel):
    name: str
    score: int
