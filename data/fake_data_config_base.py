import data.fake_data_config
import data.fake_data_config_template
import schemas.fake_data_config_base
from app.SQL import models

name = "fake_data_config_base"
redis_tables = [
    {"name": name, "key": "id"},
]
sql_model = models.FakeDataConfigBase
main_schemas = schemas.fake_data_config_base.FakeDataConfigBase
create_schemas = schemas.fake_data_config_base.FakeDataConfigBaseCreate
update_schemas = schemas.fake_data_config_base.FakeDataConfigBaseUpdate
multiple_update_schemas = schemas.fake_data_config_base.FakeDataConfigBaseMultipleUpdate

reload_related_redis_tables = {
    "outside_field":
        [
            {"module": data.fake_data_config, "field": "fake_data_config_base_id"},
            {"module": data.fake_data_config_template, "field": "fake_data_config_base_id"}
        ],
    "self_field":
        [
        ]
}
