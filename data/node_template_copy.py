import schemas.node_template
from app.SQL import models

name = "node_template"
redis_tables = [
    {"name": name, "key": "id"},
]
sql_model = models.NodeTemplate
main_schemas = schemas.node_template.NodeTemplate
create_schemas = schemas.node_template.NodeTemplateCreate
update_schemas = schemas.node_template.NodeTemplateUpdate
multiple_update_schemas = schemas.node_template.NodeTemplateMultipleUpdate

reload_related_redis_tables = {
}