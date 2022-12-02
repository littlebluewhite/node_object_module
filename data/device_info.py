import data.node_base
import schemas.device_info
from app.SQL import models

name = "device_info"
redis_tables = [
    {"name": name, "key": "id"},
]
sql_model = models.DeviceInfo
main_schemas = schemas.device_info.DeviceInfo
create_schemas = schemas.device_info.DeviceInfoCreate
update_schemas = schemas.device_info.DeviceInfoUpdate
multiple_update_schemas = schemas.device_info.DeviceInfoMultipleUpdate

reload_related_redis_tables = {
    "outside_field":
        [
        ],
    "self_field":
        [
            {"module": data.node_base, "field": "node_base_id"}
        ]
}
