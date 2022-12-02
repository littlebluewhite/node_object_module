import schemas.object_group
from app.SQL import models

name = "object_group"
redis_tables = [
    {"name": name, "key": "id"},
]
sql_model = models.ObjectGroup
main_schemas = schemas.object_group.ObjectGroup
create_schemas = schemas.object_group.ObjectGroupCreate
update_schemas = schemas.object_group.ObjectGroupUpdate
multiple_update_schemas = schemas.object_group.ObjectGroupMultipleUpdate

reload_related_redis_tables = {
    "self_field":
        [
        ],
    "outside_field":
        [],
}
