#TODO НЕ ДОДЕЛАННО
 
from fastapi import APIRouter, HTTPException
from typing import List

# Импортируем MongoManager
from app.db.connection import mongo_manager
from app.models.test_mongo import Item

apiRouter = APIRouter(tags=["Test MongoDB"])
collection_name = "collection_name"

@apiRouter.post("/items/", response_model=Item)
async def create_item(item: Item):
    collection = mongo_manager.get_db()[collection_name]
    result = await collection.insert_one(item.dict())
    item.id = str(result.inserted_id)
    return item

@apiRouter.get("/items/", response_model=List[Item])
async def read_items():
    collection = mongo_manager.get_db()[collection_name]
    items = await collection.find().to_list(100)
    return [Item(id=str(item['_id']), name=item['name'], description=item.get('description')) for item in items]

@apiRouter.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    collection = mongo_manager.get_db()[collection_name]
    item = await collection.find_one({"_id": item_id})
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return Item(id=str(item['_id']), name=item['name'], description=item.get('description'))

@apiRouter.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    collection = mongo_manager.get_db()[collection_name]
    result = await collection.update_one({"_id": item_id}, {"$set": item.dict()})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@apiRouter.delete("/items/{item_id}", response_model=dict)
async def delete_item(item_id: str):
    collection = mongo_manager.get_db()[collection_name]
    result = await collection.delete_one({"_id": item_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"detail": "Item deleted"}
