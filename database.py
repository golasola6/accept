import motor.motor_asyncio
from os import environ as env
DB_URL = env.get('DB_URL')
DB_NAME = env.get('DB_NAME', 'Cluster0')

class Database:

    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.user


    def new_user(self, id):
        return dict(
            _id=int(id),                                   
            file_id=None,
            caption=None
        )
    
    async def add_user(self, id):
        user = self.new_user(id)
        await self.col.insert_one(user)

    async def is_user_exist(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return bool(user)

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users

    async def delete_user(self, user_id):
        await self.col.delete_many({'_id': int(user_id)})

db = Database(DB_URL, DB_NAME)
