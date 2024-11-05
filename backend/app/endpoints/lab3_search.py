from fastapi import APIRouter, HTTPException, Query
from typing import List, Union
from app.db.connection import mongo_manager
from app.models.lab3 import Match, Player, Team
from bson import ObjectId
import re

apiRouter = APIRouter(tags=["Lab3"])

mongo_operators = {
    ">": "$gt",
    ">=": "$gte",
    "=": "$eq",
    "<=": "$lte",
    "<": "$lt"
}

@apiRouter.get("/search/players", response_model=List[Player])
async def search_players(field: str = Query(...), operator: str = Query(...), value: Union[int, float, str] = Query(...)):
    if operator not in mongo_operators:
        raise HTTPException(status_code=400, detail="Invalid operator")
    
    collection = mongo_manager.get_db()["players"]
    mongo_operator = mongo_operators[operator]

    try:
        value = int(value)
    except:
        pass
    
    query = {field: {mongo_operator: value}}
    players = await collection.find(query).to_list(100)
    return [Player(**player) for player in players]

@apiRouter.get("/search/teams", response_model=List[Team])
async def search_teamss(field: str = Query(...), operator: str = Query(...), value: Union[int, float, str] = Query(...)):
    if operator not in mongo_operators:
        raise HTTPException(status_code=400, detail="Invalid operator")
    
    collection = mongo_manager.get_db()["teams"]
    mongo_operator = mongo_operators[operator]

    try:
        value = int(value)
    except:
        pass
    
    query = {field: {mongo_operator: value}}
    teams = await collection.find(query).to_list(100)
    return [Team(**team) for team in teams]

@apiRouter.get("/search/matches", response_model=List[Match])
async def search_matches(field: str = Query(...), operator: str = Query(...), value: Union[int, float, str] = Query(...)):
    if operator not in mongo_operators:
        raise HTTPException(status_code=400, detail="Invalid operator")
    
    collection = mongo_manager.get_db()["matches"]
    mongo_operator = mongo_operators[operator]

    try:
        value = int(value)
    except:
        pass
    
    query = {field: {mongo_operator: value}}
    matches = await collection.find(query).to_list(100)
    return [Match(**match) for match in matches]

# Я НЕ ХОЧУ ЭТО ПИСАТЬ, НЕ ХОЧУ !!!! пусть останется эта пустышка
@apiRouter.get("/search", response_model=list)
async def parse_and_search(query: str):
    match = re.match(r"Получить количество футболистов, забивших (более|менее|ровно) (\d+) голов", query)
    
    if not match:
        raise HTTPException(status_code=400, detail="Неверный формат запроса")
    
    operator_word = match.group(1)
    goals_threshold = int(match.group(2))
    
    if operator_word == "более":
        operator = ">"
    elif operator_word == "менее":
        operator = "<"
    elif operator_word == "ровно":
        operator = "="
    else:
        raise HTTPException(status_code=400, detail="Неверный оператор")
    
    players = await search_players(field="goals", operator=operator, value=goals_threshold)
    
    return players
