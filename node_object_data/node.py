import node_object_data.node_copy
import node_object_schemes.node
from node_object_SQL import models

name = "node"
redis_tables = [
    {"name": name, "key": "id"},
    {"name": "node_by_node_id", "key": "node_id"},
]
sql_model = models.Node
main_schemas = node_object_schemes.node.Node
create_schemas = node_object_schemes.node.NodeCreate
update_schemas = node_object_schemes.node.NodeUpdate
multiple_update_schemas = node_object_schemes.node.NodeMultipleUpdate

reload_related_redis_tables = {
    "self_field":
        [
            {"module": node_object_data.node_copy, "field": "parent_node_id"},
        ],
}