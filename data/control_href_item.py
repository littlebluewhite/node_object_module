import data.control_href_group
import schemas.control_href_item
from app.SQL import models

name = "control_href_item"
redis_tables = [
    {"name": name, "key": "id"},
]
sql_model = models.ControlHrefItem
main_schemas = schemas.control_href_item.ControlHrefItem
create_schemas = schemas.control_href_item.ControlHrefItemCreate
update_schemas = schemas.control_href_item.ControlHrefItemUpdate
multiple_update_schemas = schemas.control_href_item.ControlHrefItemMultipleUpdate

reload_related_redis_tables = {
    "outside_field":
        [
        ],
    "self_field":
        [
            {"module": data.control_href_group, "field": "control_href_group_id"}
        ]
}
