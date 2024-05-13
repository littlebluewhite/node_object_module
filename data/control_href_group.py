import schemas.control_href_group
from app.SQL import models

name = "control_href_group"
redis_tables = [
    {"name": name, "key": "id"},
]
sql_model = models.ControlHrefGroup
main_schemas = schemas.control_href_group.ControlHrefGroup
create_schemas = schemas.control_href_group.ControlHrefGroupCreate
update_schemas = schemas.control_href_group.ControlHrefGroupUpdate
multiple_update_schemas = schemas.control_href_group.ControlHrefGroupMultipleUpdate

reload_related_redis_tables = {
    "outside_field":
        [
            # {"module": data.object, "field": "control_href_group_id"}
        ],
    "self_field":
        []
}
