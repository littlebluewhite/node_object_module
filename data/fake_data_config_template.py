import data.object_template
import schemas.fake_data_config_template
from app.SQL import models

name = "fake_data_config_template"
redis_tables = [
    {"name": name, "key": "id"},
]
sql_model = models.FakeDataConfigTemplate
main_schemas = schemas.fake_data_config_template.FakeDataConfigTemplate
create_schemas = schemas.fake_data_config_template.FakeDataConfigTemplateCreate
update_schemas = schemas.fake_data_config_template.FakeDataConfigTemplateUpdate
multiple_update_schemas = schemas.fake_data_config_template.FakeDataConfigTemplateMultipleUpdate

reload_related_redis_tables = {
    "outside_field":
        [
        ],
    "self_field":
        [
            {"module": data.object_template, "field": "object_template_id"}
        ]
}
