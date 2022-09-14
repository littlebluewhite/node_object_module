import node_object_data.node
import node_object_data.node_group
import node_object_schemes.node_node_group
from node_object_SQL import models

name = "node_node_group"
redis_tables = [
    # {"name": name, "key": "id"},
]
sql_model = models.NodeNodeGroup
main_schemas = node_object_schemes.node_node_group.NodeNodeGroup
create_schemas = node_object_schemes.node_node_group.NodeNodeGroupCreate
update_schemas = node_object_schemes.node_node_group.NodeNodeGroupUpdate
multiple_update_schemas = node_object_schemes.node_node_group.NodeNodeGroupMultipleUpdate

reload_related_redis_tables = {
    "self_field":
        [
            {"module": node_object_data.node, "field": "node_id"},
            {"module": node_object_data.node_group, "field": "node_group_id"}
        ]
}
