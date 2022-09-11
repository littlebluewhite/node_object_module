import node_object_data.node_base
import node_object_schemes.device_info
from node_object_SQL import models

name = "device_info"
redis_tables = [
    {"name": name, "key": "id"},
]
sql_model = models.DeviceInfo
main_schemas = node_object_schemes.device_info.DeviceInfo
create_schemas = node_object_schemes.device_info.DeviceInfoCreate
update_schemas = node_object_schemes.device_info.DeviceInfoUpdate
multiple_update_schemas = node_object_schemes.device_info.DeviceInfoMultipleUpdate

reload_related_redis_tables = {
    "self_field":
        [
        ],
    "outside_field":
        [
            {"module": node_object_data.node_base, "field": "device_info_id"}
        ]
}
