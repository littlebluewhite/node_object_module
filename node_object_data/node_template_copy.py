import node_object_schemes.node_template
from node_object_SQL import models

name = "node_template"
redis_tables = [
    {"name": name, "key": "id"},
]
sql_model = models.NodeTemplate
main_schemas = node_object_schemes.node_template.NodeTemplate
create_schemas = node_object_schemes.node_template.NodeTemplateCreate
update_schemas = node_object_schemes.node_template.NodeTemplateUpdate
multiple_update_schemas = node_object_schemes.node_template.NodeTemplateMultipleUpdate

reload_related_redis_tables = {
}