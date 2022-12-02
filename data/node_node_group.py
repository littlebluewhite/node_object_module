import data.node
import data.node_group
import schemas.node_node_group
from app.SQL import models

name = "node_node_group"
redis_tables = [
    {"name": name, "key": "id"},
    {"name": f"{name}_by_node_id", "key": "node_id"},
    {"name": f"{name}_by_node_group_id", "key": "node_group_id"},
]
sql_model = models.NodeNodeGroup
main_schemas = schemas.node_node_group.NodeNodeGroup
create_schemas = schemas.node_node_group.NodeNodeGroupCreate
update_schemas = schemas.node_node_group.NodeNodeGroupUpdate
multiple_update_schemas = schemas.node_node_group.NodeNodeGroupMultipleUpdate

reload_related_redis_tables = {
    "self_field":
        [
            {"module": data.node, "field": "node_id"},
            {"module": data.node_group, "field": "node_group_id"}
        ]
}
