import data.node
import schemas.object
from app.SQL import models

name = "object"
redis_tables = [
    {"name": name, "key": "id"},
    {"name": "object_by_uid", "key": "uid"},
]
sql_model = models.Object
main_schemas = schemas.object.Object
create_schemas = schemas.object.ObjectCreate
update_schemas = schemas.object.ObjectUpdate
multiple_update_schemas = schemas.object.ObjectMultipleUpdate

reload_related_redis_tables = {
    "self_field":
        [
            {"module": data.node, "field": "node_id"}
        ],
    "outside_field":
        [
        ]
}
