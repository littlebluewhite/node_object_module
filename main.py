import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import data.API.API_node
import data.API.API_object
import data.API.API_control_href_group
import data.control_href_group
import data.control_href_group_template
import data.control_href_item
import data.control_href_item_template
import data.device_info
import data.fake_data_config
import data.fake_data_config_base
import data.fake_data_config_template
import data.node
import data.node_base
import data.node_group
import data.node_template
import data.object
import data.object_base
import data.object_group
import data.object_template
import data.third_dimension_instance
from general_operator.app.SQL.database import SQLDB
from app.SQL import models
from general_util.config_manager import ConfigManager
from general_operator.function.exception import GeneralOperatorException
from general_operator.app.influxdb.influxdb import InfluxDB
from general_operator.app.redis_db.redis_db import RedisDB
from routers.API.API_control_href_group import APIControlHrefGroup
from routers.API.API_node import APINodeRouter
from routers.API.API_object import APIObjectRouter
from general_operator.routers.General_table_router import GeneralRouter
from general_operator.routers.all_table import AllTableRouter

ConfigManager.read_yaml("config/config.yaml")
app = FastAPI(title="node_object_app")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# redis_db
redis_db = RedisDB(ConfigManager.redis.to_dict()).redis_client()

# SQL DB
db = SQLDB(ConfigManager.sql.to_dict(), True)
#   create SQL models
models.Base.metadata.create_all(bind=db.get_engine())

# Influx DB
influxdb = InfluxDB(ConfigManager.influxdb.to_dict())

#   create SQL session
db_session = db.new_db_session()
# router
app.include_router(APINodeRouter(data.API.API_node, redis_db, influxdb,
                                 GeneralOperatorException, db_session).create())
app.include_router(APIObjectRouter(data.API.API_object, redis_db, influxdb,
                                   GeneralOperatorException,
                                   db_session).create())
app.include_router(APIControlHrefGroup(data.API.API_control_href_group, redis_db, influxdb,
                                       GeneralOperatorException, db_session).create())
app.include_router(GeneralRouter(data.node, redis_db, influxdb,
                                 GeneralOperatorException, db_session).create())
app.include_router(GeneralRouter(data.node_base, redis_db, influxdb,
                                 GeneralOperatorException, db_session).create())
app.include_router(GeneralRouter(data.device_info, redis_db, influxdb,
                                 GeneralOperatorException, db_session).create())
app.include_router(GeneralRouter(data.third_dimension_instance, redis_db, influxdb,
                                 GeneralOperatorException, db_session).create())
app.include_router(GeneralRouter(data.node_group, redis_db, influxdb,
                                 GeneralOperatorException, db_session).create())
app.include_router(GeneralRouter(data.node_node_group, redis_db, influxdb,
                                 GeneralOperatorException, db_session).create())
app.include_router(GeneralRouter(data.object, redis_db, influxdb,
                                 GeneralOperatorException, db_session).create())
app.include_router(GeneralRouter(data.object_base, redis_db, influxdb,
                                 GeneralOperatorException, db_session).create())
app.include_router(GeneralRouter(data.object_group, redis_db, influxdb,
                                 GeneralOperatorException, db_session).create())
app.include_router(GeneralRouter(data.object_object_group, redis_db, influxdb,
                                 GeneralOperatorException, db_session).create())
app.include_router(GeneralRouter(data.control_href_group, redis_db, influxdb,
                                 GeneralOperatorException, db_session).create())
app.include_router(GeneralRouter(data.control_href_item, redis_db, influxdb,
                                 GeneralOperatorException, db_session).create())
app.include_router(GeneralRouter(data.fake_data_config, redis_db, influxdb,
                                 GeneralOperatorException, db_session).create())
app.include_router(GeneralRouter(data.fake_data_config_base, redis_db, influxdb,
                                 GeneralOperatorException, db_session).create())
app.include_router(GeneralRouter(data.node_template, redis_db, influxdb,
                                 GeneralOperatorException, db_session).create())
app.include_router(GeneralRouter(data.object_template, redis_db, influxdb,
                                 GeneralOperatorException, db_session).create())
app.include_router(GeneralRouter(data.control_href_group_template, redis_db, influxdb,
                                 GeneralOperatorException, db_session).create())
app.include_router(GeneralRouter(data.control_href_item_template, redis_db, influxdb,
                                 GeneralOperatorException, db_session).create())
app.include_router(GeneralRouter(data.fake_data_config_template, redis_db, influxdb,
                                 GeneralOperatorException, db_session).create())

app.include_router(AllTableRouter(module=data, redis_db=redis_db, influxdb=influxdb,
                                  exc=GeneralOperatorException, db_session=db_session,
                                  is_initial=ConfigManager.server.is_initial).create())


@app.exception_handler(GeneralOperatorException)
async def unicorn_exception_handler(request: Request, exc: GeneralOperatorException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": f"{exc.message}", "message_code": f"{exc.message_code}"},
        headers={"message": f"{exc.message}", "message_code": f"{exc.message_code}"}
    )


@app.get("/exception")
async def test_exception():
    raise GeneralOperatorException(status_code=423, message="test exception", message_code=2)



if __name__ == "__main__":
    uvicorn.run(app="main:app", host='0.0.0.0', port=ConfigManager.server.port, workers=4, reload=True, loop="asyncio",
                log_level="info", limit_concurrency=1000)
