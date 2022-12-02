import data.object
import data.object_template
import schemas.object_base
from app.SQL import models

name = "object_base"
redis_tables = [
    {"name": name, "key": "id"},
]
sql_model = models.ObjectBase
main_schemas = schemas.object_base.ObjectBase
create_schemas = schemas.object_base.ObjectBaseCreate
update_schemas = schemas.object_base.ObjectBaseUpdate
multiple_update_schemas = schemas.object_base.ObjectBaseMultipleUpdate

reload_related_redis_tables = {
    "outside_field":
        [
            {"module": data.object_template, "field": "object_base_id"},
            {"module": data.object, "field": "object_base_id"}
        ],
    "self_field":
        [
        ]
}
