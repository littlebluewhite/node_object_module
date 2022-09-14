import node_object_data.node
import node_object_data.node_template
import node_object_schemes.node_base
from node_object_SQL import models

name = "node_base"
redis_tables = [
    {"name": name, "key": "id"},
]
sql_model = models.NodeBase
main_schemas = node_object_schemes.node_base.NodeBase
create_schemas = node_object_schemes.node_base.NodeBaseCreate
update_schemas = node_object_schemes.node_base.NodeBaseUpdate
multiple_update_schemas = node_object_schemes.node_base.NodeBaseMultipleUpdate

reload_related_redis_tables = {
    "self_field":
        [
        ],
    "outside_field":
        [
            {"module": node_object_data.node, "field": "node_base_id"},
            {"module": node_object_data.node_template, "field": "node_template_id"},
        ]
}
