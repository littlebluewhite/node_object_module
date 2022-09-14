import node_object_data.object
import node_object_schemes.control_href_group
from node_object_SQL import models

name = "control_href_group"
redis_tables = [
    {"name": name, "key": "id"},
]
sql_model = models.ControlHrefGroup
main_schemas = node_object_schemes.control_href_group.ControlHrefGroup
create_schemas = node_object_schemes.control_href_group.ControlHrefGroupCreate
update_schemas = node_object_schemes.control_href_group.ControlHrefGroupUpdate
multiple_update_schemas = node_object_schemes.control_href_group.ControlHrefGroupMultipleUpdate

reload_related_redis_tables = {
    "outside_field":
        [
            {"module": node_object_data.object, "field": "control_href_group_id"}
        ],
    "self_field":
        []
}
