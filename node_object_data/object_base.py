import node_object_data.object
import node_object_data.object_template
import node_object_schemes.object_base
from node_object_SQL import models

name = "object_base"
redis_tables = [
    {"name": name, "key": "id"},
]
sql_model = models.ObjectBase
main_schemas = node_object_schemes.object_base.ObjectBase
create_schemas = node_object_schemes.object_base.ObjectBaseCreate
update_schemas = node_object_schemes.object_base.ObjectBaseUpdate
multiple_update_schemas = node_object_schemes.object_base.ObjectBaseMultipleUpdate

reload_related_redis_tables = {
    "outside_field":
        [
            {"module": node_object_data.object_template, "field": "object_base_id"},
            {"module": node_object_data.object, "field": "object_base_id"}
        ],
    "self_field":
        [
        ]
}
