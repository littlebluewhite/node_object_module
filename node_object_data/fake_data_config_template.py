import node_object_data.object_template
import node_object_schemes.fake_data_config_template
from node_object_SQL import models

name = "fake_data_config_template"
redis_tables = [
    {"name": name, "key": "id"},
]
sql_model = models.FakeDataConfigTemplate
main_schemas = node_object_schemes.fake_data_config_template.FakeDataConfigTemplate
create_schemas = node_object_schemes.fake_data_config_template.FakeDataConfigTemplateCreate
update_schemas = node_object_schemes.fake_data_config_template.FakeDataConfigTemplateUpdate
multiple_update_schemas = node_object_schemes.fake_data_config_template.FakeDataConfigTemplateMultipleUpdate

reload_related_redis_tables = {
    "outside_field":
        [
        ],
    "self_field":
        [
            {"module": node_object_data.object_template, "field": "object_template_id"}
        ]
}
