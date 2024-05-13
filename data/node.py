import data.node_copy
import schemas.node
from app.SQL import models

name = "node"
redis_tables = [
    {"name": name, "key": "id"},
    {"name": "node_by_uid", "key": "uid"},
]
sql_model = models.Node
main_schemas = schemas.node.Node
create_schemas = schemas.node.NodeCreate
update_schemas = schemas.node.NodeUpdate
multiple_update_schemas = schemas.node.NodeMultipleUpdate

reload_related_redis_tables = {
    "self_field":
        [
            {"module": data.node_copy, "field": "parent_node_id"},
        ],
}
