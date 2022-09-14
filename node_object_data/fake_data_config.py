import node_object_data.object
import node_object_schemes.fake_data_config
from node_object_SQL import models

name = "fake_data_config"
redis_tables = [
    {"name": name, "key": "id"},
]
sql_model = models.FakeDataConfig
main_schemas = node_object_schemes.fake_data_config.FakeDataConfig
create_schemas = node_object_schemes.fake_data_config.FakeDataConfigCreate
update_schemas = node_object_schemes.fake_data_config.FakeDataConfigUpdate
multiple_update_schemas = node_object_schemes.fake_data_config.FakeDataConfigMultipleUpdate

reload_related_redis_tables = {
    "outside_field":
        [
        ],
    "self_field":
        [
            {"module": node_object_data.object, "field": "object_id"}
        ]
}
