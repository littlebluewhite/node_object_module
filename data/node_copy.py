import schemas.node
from app.SQL import models

name = "node"
redis_tables = [
    {"name": name, "key": "id"},
    {"name": "node_by_node_id", "key": "node_id"},
]
sql_model = models.Node
main_schemas = schemas.node.Node
create_schemas = schemas.node.NodeCreate
update_schemas = schemas.node.NodeUpdate
multiple_update_schemas = schemas.node.NodeMultipleUpdate
reload_related_redis_tables = {
}
