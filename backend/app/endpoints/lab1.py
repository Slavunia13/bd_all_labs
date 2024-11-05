from fastapi import APIRouter, HTTPException
from starlette import status

from app.db.connection import redis_manager
from app.models.lab1 import UserSettings, TextRequest
from app.utils.fonts import fonts

apiRouter = APIRouter(tags=["Lab1"])

@apiRouter.post("/users/{username}/settings")
async def save_user_settings(username: str, settings: UserSettings):
    redis = redis_manager.get_redis()
    await redis.hset(f"user:{username}", mapping=settings.dict())
    return {"message": "Settings saved successfully"}

@apiRouter.get("/users/{username}/settings", response_model=UserSettings)
async def get_user_settings(username: str):
    redis = redis_manager.get_redis()
    settings = await redis.hgetall(f"user:{username}")
    if not settings:
        raise HTTPException(status_code=404, detail="User not found")
    return {k.decode('utf-8'): v.decode('utf-8') for k, v in settings.items()}

@apiRouter.get("/users", response_model=list[str])
async def get_users():
    redis = redis_manager.get_redis()
    keys = await redis.keys('user:*')
    users = [key.decode('utf-8').split(':')[1] for key in keys]
    return users

@apiRouter.post("/users/{username}/text")
async def format_text_for_user(username: str, text_request: TextRequest):
    redis = redis_manager.get_redis()
    settings = await redis.hgetall(f"user:{username}")
    if not settings:
        raise HTTPException(status_code=404, detail="User not found")

    font_name = settings.get(b'font_name').decode('utf-8')
    font_size = settings.get(b'font_size').decode('utf-8')
    font_color = settings.get(b'font_color').decode('utf-8')
    font_style = settings.get(b'font_style').decode('utf-8')

    formatted_text = f"<span style='font-family: {font_name}; font-size: {font_size}px; color: {font_color}; font-style: {font_style};'>{text_request.text}</span>"
    return {"formatted_text": formatted_text}

@apiRouter.get("/fonts")
async def get_fonts():
    return {"fonts": fonts}