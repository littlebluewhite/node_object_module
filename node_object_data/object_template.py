import node_object_data.node_template
import node_object_schemes.object_template
from node_object_SQL import models

name = "object_template"
redis_tables = [
    {"name": name, "key": "id"},
]
sql_model = models.ObjectTemplate
main_schemas = node_object_schemes.object_template.ObjectTemplate
create_schemas = node_object_schemes.object_template.ObjectTemplateCreate
update_schemas = node_object_schemes.object_template.ObjectTemplateUpdate
multiple_update_schemas = node_object_schemes.object_template.ObjectTemplateMultipleUpdate

reload_related_redis_tables = {
    "outside_field":
        [
        ],
    "self_field":
        [
            {"module": node_object_data.node_template, "field": "node_template_id"}
        ]
}
