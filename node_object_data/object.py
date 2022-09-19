import node_object_data.node
import node_object_schemes.object
from node_object_SQL import models

name = "object"
redis_tables = [
    {"name": name, "key": "id"},
]
sql_model = models.Object
main_schemas = node_object_schemes.object.Object
create_schemas = node_object_schemes.object.ObjectCreate
update_schemas = node_object_schemes.object.ObjectUpdate
multiple_update_schemas = node_object_schemes.object.ObjectMultipleUpdate

reload_related_redis_tables = {
    "self_field":
        [
            {"module": node_object_data.node, "field": "node_id"}
        ],
    "outside_field":
        [
        ]
}
