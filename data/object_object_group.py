import data.object
import data.object_group
import schemas.object_object_group
from app.SQL import models

name = "object_object_group"
redis_tables = [
    {"name": name, "key": "id"},
    {"name": f"{name}_by_object_id", "key": "object_id"},
    {"name": f"{name}_by_object_group_id", "key": "object_group_id"},
]
sql_model = models.ObjectObjectGroup
main_schemas = schemas.object_object_group.ObjectObjectGroup
create_schemas = schemas.object_object_group.ObjectObjectGroupCreate
update_schemas = schemas.object_object_group.ObjectObjectGroupUpdate
multiple_update_schemas = schemas.object_object_group.ObjectObjectGroupMultipleUpdate

reload_related_redis_tables = {
    "self_field":
        [
            {"module": data.object, "field": "object_id"},
            {"module": data.object_group, "field": "object_group_id"},
        ]
}
