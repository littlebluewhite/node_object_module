import schemas.node_group
from app.SQL import models

name = "node_group"
redis_tables = [
    {"name": name, "key": "id"},
]
sql_model = models.NodeGroup
main_schemas = schemas.node_group.NodeGroup
create_schemas = schemas.node_group.NodeGroupCreate
update_schemas = schemas.node_group.NodeGroupUpdate
multiple_update_schemas = schemas.node_group.NodeGroupMultipleUpdate

reload_related_redis_tables = {
    "outside_field":
        [],
    "self_field":
        []
}
