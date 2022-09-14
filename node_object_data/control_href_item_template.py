import node_object_data.control_href_group_template
import node_object_schemes.control_href_item_template
from node_object_SQL import models

name = "control_href_item_template"
redis_tables = [
    {"name": name, "key": "id"},
]
sql_model = models.ControlHrefItemTemplate
main_schemas = node_object_schemes.control_href_item_template.ControlHrefItemTemplate
create_schemas = node_object_schemes.control_href_item_template.ControlHrefItemTemplateCreate
update_schemas = node_object_schemes.control_href_item_template.ControlHrefItemTemplateUpdate
multiple_update_schemas = node_object_schemes.control_href_item_template.ControlHrefItemTemplateMultipleUpdate

reload_related_redis_tables = {
    "outside_field":
        [
        ],
    "self_field":
        [
            {"module": node_object_data.control_href_group_template, "field": "control_href_group_template_id"}
        ]
}
