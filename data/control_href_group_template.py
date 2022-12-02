import data.object_template
import schemas.control_href_group_template
from app.SQL import models

name = "control_href_group_template"
redis_tables = [
    {"name": name, "key": "id"},
]
sql_model = models.ControlHrefGroupTemplate
main_schemas = schemas.control_href_group_template.ControlHrefGroupTemplate
create_schemas = schemas.control_href_group_template.ControlHrefGroupTemplateCreate
update_schemas = schemas.control_href_group_template.ControlHrefGroupTemplateUpdate
multiple_update_schemas = schemas.control_href_group_template.ControlHrefGroupTemplateMultipleUpdate

reload_related_redis_tables = {
    "outside_field":
        [
        ],
    "self_field":
        [
            {"module": data.object_template, "field": "object_template_id"}
        ]
}
