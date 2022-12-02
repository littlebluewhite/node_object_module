import data.control_href_group_template
import schemas.control_href_item_template
from app.SQL import models

name = "control_href_item_template"
redis_tables = [
    {"name": name, "key": "id"},
]
sql_model = models.ControlHrefItemTemplate
main_schemas = schemas.control_href_item_template.ControlHrefItemTemplate
create_schemas = schemas.control_href_item_template.ControlHrefItemTemplateCreate
update_schemas = schemas.control_href_item_template.ControlHrefItemTemplateUpdate
multiple_update_schemas = schemas.control_href_item_template.ControlHrefItemTemplateMultipleUpdate

reload_related_redis_tables = {
    "outside_field":
        [
        ],
    "self_field":
        [
            {"module": data.control_href_group_template, "field": "control_href_group_template_id"}
        ]
}
