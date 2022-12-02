import data.node
import schemas.third_dimension_instance
from app.SQL import models

name = "third_dimension_instance"
redis_tables = [
    {"name": name, "key": "id"},
]
sql_model = models.ThirdDimensionInstance
main_schemas = schemas.third_dimension_instance.ThirdDimensionInstance
create_schemas = schemas.third_dimension_instance.ThirdDimensionInstanceCreate
update_schemas = schemas.third_dimension_instance.ThirdDimensionInstanceUpdate
multiple_update_schemas = schemas.third_dimension_instance.ThirdDimensionInstanceMultipleUpdate

reload_related_redis_tables = {
    "outside_field":
        [
        ],
    "self_field":
        [
            {"module": data.node, "field": "node_id"}
        ]
}
