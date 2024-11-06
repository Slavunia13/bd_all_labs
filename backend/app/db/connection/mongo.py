from motor.motor_asyncio import AsyncIOMotorClient
from app.config import getSettings

class MongoManager:
    def __init__(self, mongo_url: str) -> None:
        self.mongo_url = mongo_url
        self.client = None
        self.db = None

    async def connect(self) -> None:
        """Connect to MongoDB and select the database."""
        self.client = AsyncIOMotorClient(self.mongo_url)
        self.db = self.client[settings.MONGO_NAME]

        # Создание пользователя, если он не существует
        await self.create_user()

    async def create_user(self):
        """Create a user for the database if it does not exist."""
        try:
            # Проверяем, существует ли пользователь
            await self.client[settings.MONGO_NAME].command("usersInfo", settings.MONGO_USER)
            print(f"Пользователь {settings.MONGO_USER} уже существует.")
        except Exception as e:
            if e.code == 13:  # Код ошибки 13 означает, что у вас нет прав доступа
                print("Нет прав доступа для проверки пользователя.")
            else:
                # Если пользователь не существует, создаем его
                await self.client[settings.MONGO_NAME].command("createUser", settings.MONGO_USER,
                    pwd=settings.MONGO_PASSWORD,
                    roles=[{"role": "readWrite", "db": settings.MONGO_NAME}]
                )
                print(f"Пользователь {settings.MONGO_USER} создан.")

    async def disconnect(self) -> None:
        """Disconnect from MongoDB."""
        if self.client:
            self.client.close()

    def get_db(self):
        """Get the MongoDB database client."""
        return self.db

# Пример использования
settings = getSettings()
mongo_manager = MongoManager(mongo_url=f"mongodb://{settings.MONGO_USER}:{settings.MONGO_PASSWORD}@{settings.MONGO_HOST}:{settings.MONGO_PORT}/")
