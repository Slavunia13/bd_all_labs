from bson import ObjectId
from fastapi import APIRouter, HTTPException

# Импортируем MongoManager
from app.db.connection import mongo_manager
from app.models.lab3 import Team, Match, Player

apiRouter = APIRouter(tags=["Lab3"])

@apiRouter.post("/players/", response_model=Player)
async def create_player(player: Player):
    collection = mongo_manager.get_db()["players"]
    result = await collection.insert_one(player.dict())
    player.id = str(result.inserted_id)
    return player

@apiRouter.get("/players/", response_model=list[Player])
async def read_players():
    collection = mongo_manager.get_db()["players"]
    players = await collection.find().to_list(100)
    answer = []
    for player in players:
        player['id'] = str(player['_id'])
        answer.append(Player(**player))
    return answer

@apiRouter.delete("/players/{player_id}", response_model=dict)
async def delete_player(player_id: str):
    collection = mongo_manager.get_db()["players"]
    result = await collection.delete_one({"_id": ObjectId(player_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Player not found")
    return {"detail": "Player deleted"}

@apiRouter.post("/teams/", response_model=Team)
async def create_team(team: Team):
    db = mongo_manager.get_db()
    players_collection = db["players"]
    
    # Проверка существования игроков в стартовом составе и на замене
    player_ids = set(team.starting_lineup + team.substitutes)
    if player_ids:
        found_players = await players_collection.count_documents({"_id": {"$in": [ObjectId(pid) for pid in player_ids]}})
        if found_players != len(player_ids):
            raise HTTPException(status_code=400, detail="One or more players not found")

    teams_collection = db["teams"]
    result = await teams_collection.insert_one(team.dict())
    team.id = str(result.inserted_id)
    return team

@apiRouter.get("/teams/", response_model=list[Team])
async def read_teams():
    collection = mongo_manager.get_db()["teams"]
    teams = await collection.find().to_list(100)
    answer = []
    for team in teams:
        team['id'] = str(team['_id'])
        answer.append(Team(**team))
    return answer

@apiRouter.get("/teams/{team_id}", response_model=Team)
async def read_team(team_id: str):
    collection = mongo_manager.get_db()["teams"]
    team = await collection.find_one({"_id": ObjectId(team_id)})
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    team['id'] = str(team['_id'])
    return Team(**team)

@apiRouter.delete("/teams/{team_id}", response_model=dict)
async def delete_team(team_id: str):
    collection = mongo_manager.get_db()["teams"]
    result = await collection.delete_one({"_id": ObjectId(team_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Team not found")
    return {"detail": "Team deleted"}



@apiRouter.post("/matches/", response_model=Match)
async def create_match(match: Match):
    db = mongo_manager.get_db()
    teams_collection = db["teams"]

    # Проверка, что команды существуют
    if match.team_ids:
        found_teams = await teams_collection.count_documents({"_id": {"$in": [ObjectId(tid) for tid in match.team_ids]}})
        if found_teams != len(match.team_ids):
            raise HTTPException(status_code=400, detail="One or more teams not found")

    # Проверка авторов голов и увеличение их счетчика голов
    players_collection = db["players"]
    for goal in match.goals:
        # Проверка наличия автора гола
        author = await players_collection.find_one({"_id": ObjectId(goal.author_id)})
        if not author:
            raise HTTPException(status_code=400, detail=f"Author with id {goal.author_id} not found")

        # Проверка наличия ассистента, если указан
        if goal.assist_id:
            assist_exists = await players_collection.find_one({"_id": ObjectId(goal.assist_id)})
            if not assist_exists:
                raise HTTPException(status_code=400, detail=f"Assist with id {goal.assist_id} not found")
        
        # Увеличение счетчика голов у автора
        await players_collection.update_one(
            {"_id": ObjectId(goal.author_id)},
            {"$inc": {"goals": 1}}
        )

    # Добавление матча в коллекцию
    matches_collection = db["matches"]
    result = await matches_collection.insert_one(match.dict())
    match.id = str(result.inserted_id)
    return match

@apiRouter.get("/matches/", response_model=list[Match])
async def read_matches():
    collection = mongo_manager.get_db()["matches"]
    matches = await collection.find().to_list(100)
    answer = []
    for match in matches:
        match['id'] = str(match['_id'])
        answer.append(Match(**match))
    return answer

@apiRouter.get("/matches/{match_id}", response_model=Match)
async def read_match(match_id: str):
    collection = mongo_manager.get_db()["matches"]
    match = await collection.find_one({"_id": ObjectId(match_id)})
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    match['id'] = str(match['_id'])
    return Match(**match)

@apiRouter.delete("/matches/{match_id}", response_model=dict)
async def delete_match(match_id: str):
    collection = mongo_manager.get_db()["matches"]
    result = await collection.delete_one({"_id": ObjectId(match_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Match not found")
    return {"detail": "Match deleted"}
