import json
from fastapi import APIRouter, HTTPException
from fastapi import WebSocket, WebSocketDisconnect
from starlette import status

from app.db.connection import redis_manager
from app.models.lab2 import Athlete, Judge, ScoreUpdate, AthleteScore

apiRouter = APIRouter(tags=["Lab2"])

@apiRouter.post("/athletes")
async def add_athlete(athlete: Athlete):
    redis = redis_manager.get_redis()
    await redis.hset(f"athlete:{athlete.name}", mapping=athlete.dict())
    await update_rankings()
    return {"message": "Athlete added successfully"}

@apiRouter.post("/judges")
async def add_judge(judge: Judge):
    redis = redis_manager.get_redis()
    await redis.hset(f"judge:{judge.name}", mapping=judge.dict())
    await update_rankings()
    return {"message": "Judge added successfully"}

@apiRouter.post("/scores")
async def update_score(score_update: ScoreUpdate):
    redis = redis_manager.get_redis()
    key = f"score:{score_update.judge}:{score_update.athlete}"
    
    current_score = await redis.hget(key, "total_score")
    current_score = int(current_score) if current_score else 0
    
    new_score = score_update.score
    await redis.hset(key, "total_score", new_score)
    await update_rankings()
    print("Score updated, notifying rankings")
    return {"message": "Score updated successfully"}

async def update_rankings():
    redis = redis_manager.get_redis()
    athlete_scores = {}
    
    # Получаем все ключи с баллами
    score_keys = await redis.keys('score:*')
    
    # Суммируем баллы для каждого спортсмена
    for score_key in score_keys:
        athlete_name = score_key.decode('utf-8').split(':')[2]  # Измените индекс на 2
        score = await redis.hget(score_key, "total_score")
        score = int(score) if score else 0
        
        if athlete_name in athlete_scores:
            athlete_scores[athlete_name] += score
        else:
            athlete_scores[athlete_name] = score

    rankings = [AthleteScore(name=name, score=score) for name, score in athlete_scores.items()]

    # Добавляем спортсменов, которые еще не имеют баллов
    for athlete in await get_athletes():
        if athlete not in athlete_scores:
            rankings.append(AthleteScore(name=athlete, score=0))

    rankings.sort(key=lambda x: x.score, reverse=True)
    
    await redis.set("rankings", json.dumps([r.dict() for r in rankings]))
    await notify_rankings()


@apiRouter.get("/rankings", response_model=list[AthleteScore])
async def get_rankings():
    redis = redis_manager.get_redis()
    rankings = await redis.get("rankings")
    if not rankings:
        raise HTTPException(status_code=404, detail="No rankings found")
    return json.loads(rankings)  

@apiRouter.get("/athletes", response_model=list[str])
async def get_athletes():
    redis = redis_manager.get_redis()
    keys = await redis.keys('athlete:*')
    athletes = [key.decode('utf-8').split(':')[1] for key in keys]
    return athletes

@apiRouter.get("/judges", response_model=list[str])
async def get_judges():
    redis = redis_manager.get_redis()
    keys = await redis.keys('judge:*')
    judges = [key.decode('utf-8').split(':')[1] for key in keys]
    return judges

active_connections: list[WebSocket] = []

@apiRouter.websocket("/ws/rankings")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    print("New client connected")
    await notify_rankings()
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        print("Client disconnected")

async def notify_rankings():
    try:
        rankings = await get_rankings()
    except Exception as e:
        rankings = []
    message = [{"name": r['name'], "score": r['score']} for r in rankings]
    print("Sending rankings:", message)  # Отладочное сообщение
    for connection in active_connections:
        await connection.send_json(message)
