from neo4j import GraphDatabase
import asyncio
from concurrent.futures import ThreadPoolExecutor
from app.config import getSettings

settings = getSettings()

class Neo4jManager:
    def __init__(self):
        self.driver = None
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.uri = f"bolt://{settings.NEO4J_HOST}:{settings.NEO4J_PORT_BOLT}" 
        self.user = settings.NEO4J_AUTH.split("/")[0]
        self.password = settings.NEO4J_AUTH.split("/")[1]

    async def connect(self):
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))

    async def disconnect(self):
        if self.driver:
            self.driver.close()

    def run_query(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return [record for record in result]

    async def run_query_async(self, query, parameters=None):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, self.run_query, query, parameters)

uri = f"bolt://{settings.NEO4J_HOST}:{settings.NEO4J_PORT_BOLT}" 
user = settings.NEO4J_AUTH.split("/")[0]
password = settings.NEO4J_AUTH.split("/")[1]

neo4j_manager = Neo4jManager()
