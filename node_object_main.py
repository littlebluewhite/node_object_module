import argparse
import configparser

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import node_object_data.API.API_node
import node_object_data.API.API_object

import node_object_data.node
import node_object_data.node_base
import node_object_data.device_info
import node_object_data.third_dimension_instance
import node_object_data.node_group
import node_object_data.node_node_group
import node_object_data.object
import node_object_data.object_group
import node_object_data.object_object_group
import node_object_data.object_base
import node_object_data.control_href_group
import node_object_data.control_href_item
import node_object_data.fake_data_config
import node_object_data.fake_data_config_base
import node_object_data.node_template
import node_object_data.object_template
import node_object_data.control_href_group_template
import node_object_data.control_href_item_template
import node_object_data.fake_data_config_template
from app.value_trace import ValueQueue

from node_object_SQL import models
from node_object_SQL.database import SQLDB
from node_object_exception import NodeObjectException
from node_object_influxdb.influxdb import InfluxDB
from node_object_redis.redis import NodeRedis
from routers.API.API_object import APIObjectRouter
from routers.General_table_router import GeneralRouter
from routers.API.API_node import APINodeRouter
from routers.websockets import WebsocketsRouter

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
parser.add_argument("-ih", "--influx_host", help="InfluxDB host", type=str)
parser.add_argument("-ip", "--influx_port", help="InfluxDB port", type=str)
args = parser.parse_args()
check_list = [
    {"arg": "redis_host", "cfg": ["Redis", "host"]},
    {"arg": "redis_port", "cfg": ["Redis", "port"]},
    {"arg": "db_host", "cfg": ["SQLDB", "host"]},
    {"arg": "db_port", "cfg": ["SQLDB", "port"]},
    {"arg": "influx_host", "cfg": ["InfluxDB", "host"]},
    {"arg": "influx_port", "cfg": ["InfluxDB", "port"]},
]

# deal config
config = configparser.ConfigParser()
config.read('config.ini')
for item in check_list:
    value = args.__getattribute__(item["arg"])
    if value:
        config.read_dict({item["cfg"][0]: {item["cfg"][1]: value}})

# redis
redis_db = NodeRedis(config["Redis"]).new_redis()

# SQL DB
db = SQLDB(config["SQLDB"])
#   create SQL models
models.Base.metadata.create_all(bind=db.get_engine())

# Influx DB
influxdb = InfluxDB(config["InfluxDB"])

#   create SQL session
db_session = db.new_db_session()
q = ValueQueue()
# router
node_object_app.include_router(WebsocketsRouter(q).create())
node_object_app.include_router(APINodeRouter(node_object_data.API.API_node, redis_db,
                                             NodeObjectException, db_session).create())
node_object_app.include_router(APIObjectRouter(node_object_data.API.API_object, redis_db,
                                               influxdb, NodeObjectException,
                                               db_session, q).create())
node_object_app.include_router(GeneralRouter(node_object_data.node, redis_db,
                                             NodeObjectException, db_session).create())
node_object_app.include_router(GeneralRouter(node_object_data.node_base, redis_db,
                                             NodeObjectException, db_session).create())
node_object_app.include_router(GeneralRouter(node_object_data.device_info, redis_db,
                                             NodeObjectException, db_session).create())
node_object_app.include_router(GeneralRouter(node_object_data.third_dimension_instance, redis_db,
                                             NodeObjectException, db_session).create())
node_object_app.include_router(GeneralRouter(node_object_data.node_group, redis_db,
                                             NodeObjectException, db_session).create())
node_object_app.include_router(GeneralRouter(node_object_data.node_node_group, redis_db,
                                             NodeObjectException, db_session).create())
node_object_app.include_router(GeneralRouter(node_object_data.object, redis_db,
                                             NodeObjectException, db_session).create())
node_object_app.include_router(GeneralRouter(node_object_data.object_base, redis_db,
                                             NodeObjectException, db_session).create())
node_object_app.include_router(GeneralRouter(node_object_data.object_group, redis_db,
                                             NodeObjectException, db_session).create())
node_object_app.include_router(GeneralRouter(node_object_data.object_object_group, redis_db,
                                             NodeObjectException, db_session).create())
node_object_app.include_router(GeneralRouter(node_object_data.control_href_group, redis_db,
                                             NodeObjectException, db_session).create())
node_object_app.include_router(GeneralRouter(node_object_data.control_href_item, redis_db,
                                             NodeObjectException, db_session).create())
node_object_app.include_router(GeneralRouter(node_object_data.fake_data_config, redis_db,
                                             NodeObjectException, db_session).create())
node_object_app.include_router(GeneralRouter(node_object_data.fake_data_config_base, redis_db,
                                             NodeObjectException, db_session).create())
node_object_app.include_router(GeneralRouter(node_object_data.node_template, redis_db,
                                             NodeObjectException, db_session).create())
node_object_app.include_router(GeneralRouter(node_object_data.object_template, redis_db,
                                             NodeObjectException, db_session).create())
node_object_app.include_router(GeneralRouter(node_object_data.control_href_group_template, redis_db,
                                             NodeObjectException, db_session).create())
node_object_app.include_router(GeneralRouter(node_object_data.control_href_item_template, redis_db,
                                             NodeObjectException, db_session).create())
node_object_app.include_router(GeneralRouter(node_object_data.fake_data_config_template, redis_db,
                                             NodeObjectException, db_session).create())


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
