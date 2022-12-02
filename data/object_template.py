import data.node_template
import schemas.object_template
from app.SQL import models

name = "object_template"
redis_tables = [
    {"name": name, "key": "id"},
]
sql_model = models.ObjectTemplate
main_schemas = schemas.object_template.ObjectTemplate
create_schemas = schemas.object_template.ObjectTemplateCreate
update_schemas = schemas.object_template.ObjectTemplateUpdate
multiple_update_schemas = schemas.object_template.ObjectTemplateMultipleUpdate

reload_related_redis_tables = {
    "outside_field":
        [
        ],
    "self_field":
        [
            {"module": data.node_template, "field": "node_template_id"}
        ]
}
