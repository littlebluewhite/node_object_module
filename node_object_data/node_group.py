import node_object_schemes.node_group
from node_object_SQL import models

name = "node_group"
redis_tables = [
    {"name": name, "key": "id"},
]
sql_model = models.NodeGroup
main_schemas = node_object_schemes.node_group.NodeGroup
create_schemas = node_object_schemes.node_group.NodeGroupCreate
update_schemas = node_object_schemes.node_group.NodeGroupUpdate
multiple_update_schemas = node_object_schemes.node_group.NodeGroupMultipleUpdate

reload_related_redis_tables = {
    "outside_field":
        [],
    "self_field":
        []
}