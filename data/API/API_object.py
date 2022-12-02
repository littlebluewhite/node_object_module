from app.SQL import models
from schemas.API import API_object

redis_tables = [
    {"name": "object_value"}
]
sql_model = models.Object
main_schemas = API_object.APIObject
create_schemas = API_object.APIObjectCreate
update_schemas = API_object.APIObjectUpdate
multiple_update_schemas = API_object.APIObjectMultipleUpdate
insert_schemas = API_object.InsertValue
get_value_schemas = API_object.GetValue

reload_related_redis_tables = {}
