import node_object_data.control_href_group
import node_object_schemes.control_href_item
from node_object_SQL import models

name = "control_href_item"
redis_tables = [
    {"name": name, "key": "id"},
]
sql_model = models.ControlHrefItem
main_schemas = node_object_schemes.control_href_item.ControlHrefItem
create_schemas = node_object_schemes.control_href_item.ControlHrefItemCreate
update_schemas = node_object_schemes.control_href_item.ControlHrefItemUpdate
multiple_update_schemas = node_object_schemes.control_href_item.ControlHrefItemMultipleUpdate

reload_related_redis_tables = {
    "outside_field":
        [
        ],
    "self_field":
        [
            {"module": node_object_data.control_href_group, "field": "control_href_group_id"}
        ]
}
