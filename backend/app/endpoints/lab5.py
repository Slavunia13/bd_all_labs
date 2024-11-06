from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.db.connection import neo4j_manager
from app.utils.teat_data_lab5 import create_test_data_queries
from app.utils.queries_for_lab5 import queries_for_lab5

apiRouter = APIRouter(tags=["Lab5"])


@apiRouter.post("/test-neo4j")
async def send_query(query: str):
    result = await neo4j_manager.run_query_async(query)
    return result

@apiRouter.post("/neo4j/test-data")
async def create_test_data():
    for query in create_test_data_queries:
        await neo4j_manager.run_query_async(query)
    return {"detail": "Test data created"}

@apiRouter.get("/neo4j/labs_queries")
async def get_labs_queries():
    for item in queries_for_lab5.items():
        queries_for_lab5[item[0]] = item[1].replace('\n    ', '')
    return queries_for_lab5

class SendQuery(BaseModel):
    query: str
    param1: str | None = None
    param2: str | None = None
    param3: str | None = None

@apiRouter.post("/neo4j/labs_queries")
async def send_query_for_lab5(data: SendQuery):
    correct_query = queries_for_lab5[data.query].replace('\n', '').replace('__1', data.param1).replace('__2', data.param2).replace('__3', data.param3)
    
    result = await neo4j_manager.run_query_async(correct_query)
    return result