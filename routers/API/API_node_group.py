import redis
from fastapi import APIRouter, Depends
from sqlalchemy.orm import sessionmaker, Session

from dependencies.db_dependencies import create_get_db
from function.API.API_node_group import APINodeGroupOperate


class APINodeGroupRouter(APINodeGroupOperate):
    def __init__(self, module, redis_db: redis.Redis, exc, db_session: sessionmaker):
        self.db_session = db_session
        self.simple_schemas = module.simple_schemas
        APINodeGroupOperate.__init__(self, module, redis_db, exc)

    def create(self):
        router = APIRouter(
            prefix="/api/node_group",
            tags=["API", "Node Group"],
            dependencies=[]
        )

        create_schemas = self.create_schemas
        update_schemas = self.update_schemas
        multiple_update_schemas = self.multiple_update_schemas

        @router.post("/", response_model=self.main_schemas)
        async def create_api_node(create_data: create_schemas,
                                  db: Session = Depends(create_get_db(self.db_session))):
            with db.begin():
                data = self.get_APINode_group()
                return data

        return router
