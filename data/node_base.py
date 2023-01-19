import data.node
import data.node_template
import schemas.node_base
from app.SQL import models

name = "node_base"
redis_tables = [
    {"name": name, "key": "id"},
]
sql_model = models.NodeBase
main_schemas = schemas.node_base.NodeBase
create_schemas = schemas.node_base.NodeBaseCreate
update_schemas = schemas.node_base.NodeBaseUpdate
multiple_update_schemas = schemas.node_base.NodeBaseMultipleUpdate

reload_related_redis_tables = {
    "self_field":
        [
        ],
    "outside_field":
        [
            {"module": data.node, "field": "node_base_id"},
            {"module": data.node_template, "field": "node_base_id"},
        ]
}
