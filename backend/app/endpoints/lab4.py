from fastapi import APIRouter, HTTPException, Query
from typing import Union
from app.db.connection import mongo_manager

from app.models.lab4 import Product, Specifications

apiRouter = APIRouter(tags=["Lab4"])

# Ручка для добавления нескольких товаров
@apiRouter.post("/products/")
async def add_products(products: list[Product]):
    collection = mongo_manager.get_db()["products"]
    product_docs = [product.dict() for product in products]
    result = await collection.insert_many(product_docs)
    return {"inserted_ids": [str(id) for id in result.inserted_ids]}

# 1. Получить список названий товаров, относящихся к заданной категории
@apiRouter.get("/products/by-category/{category}", response_model=list[str])
async def get_product_names_by_category(category: str):
    collection = mongo_manager.get_db()["products"]
    products = await collection.find({"category": category}, {"name": 1, "_id": 0}).to_list(100)
    return [product["name"] for product in products]

# 2. Получить список характеристик товаров заданной категории
@apiRouter.get("/products/characteristics/{category}", response_model=list[Specifications])
async def get_product_characteristics_by_category(category: str):
    collection = mongo_manager.get_db()["products"]
    products = await collection.find({"category": category}, {"specifications": 1, "_id": 0}).to_list(100)
    return [Specifications(**product["specifications"]) for product in products]

# 3. Получить список названий и стоимости товаров, купленных заданным покупателем
@apiRouter.get("/products/by-buyer/{buyer_name}", response_model=list[dict[str, Union[str, float]]])
async def get_products_by_buyer(buyer_name: str):
    collection = mongo_manager.get_db()["products"]
    products = await collection.find({"purchases.buyer_name": buyer_name}, {"name": 1, "price": 1, "_id": 0}).to_list(100)
    return [{"name": product["name"], "price": product["price"]} for product in products]

# 4. Получить список названий, производителей и цен на товары, имеющие заданный цвет
@apiRouter.get("/products/by-color/{color}", response_model=list[dict[str, Union[str, float]]])
async def get_products_by_color(color: str):
    collection = mongo_manager.get_db()["products"]
    products = await collection.find({"specifications.color": color}, {"name": 1, "manufacturer": 1, "price": 1, "_id": 0}).to_list(100)
    return [{"name": product["name"], "manufacturer": product["manufacturer"], "price": product["price"]} for product in products]

# 5. Получить общую сумму проданных товаров
@apiRouter.get("/products/sales/total", response_model=float)
async def get_total_sales():
    collection = mongo_manager.get_db()["products"]
    pipeline = [
        {"$unwind": "$purchases"},
        {"$group": {"_id": None, "total_sales": {"$sum": "$price"}}}
    ]
    result = await collection.aggregate(pipeline).to_list(1)
    return result[0]["total_sales"] if result else 0.0

# 6. Получить количество товаров в каждой категории
@apiRouter.get("/products/category-counts", response_model=dict[str, int])
async def get_product_count_by_category():
    collection = mongo_manager.get_db()["products"]
    pipeline = [
        {"$group": {"_id": "$category", "count": {"$sum": 1}}}
    ]
    result = await collection.aggregate(pipeline).to_list(100)
    return {item["_id"]: item["count"] for item in result}

# 7. Получить список имен покупателей заданного товара
@apiRouter.get("/products/{product_name}/buyers", response_model=list[str])
async def get_buyers_by_product_name(product_name: str):
    collection = mongo_manager.get_db()["products"]
    product = await collection.find_one({"name": product_name}, {"purchases.buyer_name": 1, "_id": 0})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return [purchase["buyer_name"] for purchase in product.get("purchases", [])]

# 8. Получить список имен покупателей заданного товара, с доставкой фирмы с заданным названием
@apiRouter.get("/products/{product_name}/buyers-by-delivery", response_model=list[str])
async def get_buyers_by_product_and_delivery(product_name: str, delivery_service: str):
    collection = mongo_manager.get_db()["products"]
    product = await collection.find_one({"name": product_name}, {"purchases": 1, "_id": 0})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    buyers = [
        purchase["buyer_name"] for purchase in product.get("purchases", [])
        if purchase["delivery_service"] == delivery_service
    ]
    return buyers
