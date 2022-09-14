import node_object_data.fake_data_config
import node_object_data.fake_data_config_template
import node_object_schemes.fake_data_config_base
from node_object_SQL import models

name = "fake_data_config_base"
redis_tables = [
    {"name": name, "key": "id"},
]
sql_model = models.FakeDataConfigBase
main_schemas = node_object_schemes.fake_data_config_base.FakeDataConfigBase
create_schemas = node_object_schemes.fake_data_config_base.FakeDataConfigBaseCreate
update_schemas = node_object_schemes.fake_data_config_base.FakeDataConfigBaseUpdate
multiple_update_schemas = node_object_schemes.fake_data_config_base.FakeDataConfigBaseMultipleUpdate

reload_related_redis_tables = {
    "outside_field":
        [
            {"module": node_object_data.fake_data_config, "field": "fake_data_config_base_id"},
            {"module": node_object_data.fake_data_config_template, "field": "fake_data_config_base_id"}
        ],
    "self_field":
        [
        ]
}
