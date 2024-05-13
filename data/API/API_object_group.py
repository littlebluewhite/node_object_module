from app.SQL import models
from schemas.API import API_object_group
from schemas.API import API_object

redis_tables = []
sql_model = models.ObjectObjectGroup
main_schemas = API_object_group.APIObjectGroupMain
create_schemas = API_object_group.APIObjectGroupCreate
update_schemas = API_object_group.APIObjectGroupUpdate
multiple_update_schemas = API_object_group.APIObjectGroupMultipleUpdate
object_schemas = API_object.APIObject

reload_related_redis_tables = {}
