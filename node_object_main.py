import argparse
import configparser

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from node_object_SQL import models
from node_object_SQL.database import SQLDB
from node_object_exception import NodeObjectException
from node_object_redis.redis import NodeRedis

node_object_app = FastAPI(title="node_object_app")

node_object_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# deal arg parser
parser = argparse.ArgumentParser()
parser.add_argument("-rh", "--redis_host", help="Redis host", type=str)
parser.add_argument("-rp", "--redis_port", help="Redis port", type=str)
parser.add_argument("-dh", "--db_host", help="SQL DB host", type=str)
parser.add_argument("-dp", "--db_port", help="SQL DB port", type=str)
args = parser.parse_args()
check_list = [
    {"arg": "redis_host", "cfg": ["Redis", "host"]},
    {"arg": "redis_port", "cfg": ["Redis", "port"]},
    {"arg": "db_host", "cfg": ["SQLDB", "host"]},
    {"arg": "db_port", "cfg": ["SQLDB", "port"]},
]

# deal config
config = configparser.ConfigParser()
config.read('config.ini')
for item in check_list:
    value = args.__getattribute__(item["arg"])
    if value:
        config.read_dict({item["cfg"][0]: {item["cfg"][1]: value}})

# redis
redis = NodeRedis(config["Redis"]).new_redis()


# SQL DB
db = SQLDB(config["SQLDB"])
#   create SQL models
models.Base.metadata.create_all(bind=db.get_engine())

#   create SQL session
db_session = db.new_db_session()


# router
@node_object_app.exception_handler(NodeObjectException)
async def unicorn_exception_handler(request: Request, exc: NodeObjectException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": f"{exc.detail}"},
    )


@node_object_app.get("/exception")
async def test_exception():
    raise NodeObjectException(status_code=423, detail="test exception")


if __name__ == "__main__":
    uvicorn.run(node_object_app, host='0.0.0.0', port=9330,
                log_level="info", limit_concurrency=400)
