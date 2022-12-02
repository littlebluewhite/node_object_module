import data.object
import schemas.fake_data_config
from app.SQL import models

name = "fake_data_config"
redis_tables = [
    {"name": name, "key": "id"},
]
sql_model = models.FakeDataConfig
main_schemas = schemas.fake_data_config.FakeDataConfig
create_schemas = schemas.fake_data_config.FakeDataConfigCreate
update_schemas = schemas.fake_data_config.FakeDataConfigUpdate
multiple_update_schemas = schemas.fake_data_config.FakeDataConfigMultipleUpdate

reload_related_redis_tables = {
    "outside_field":
        [
        ],
    "self_field":
        [
            {"module": data.object, "field": "object_id"}
        ]
}
