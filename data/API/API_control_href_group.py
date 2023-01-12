from app.SQL import models
from schemas.API import API_control_href_group

redis_tables = []
sql_model = models.ControlHrefGroup
main_schemas = API_control_href_group.APIControlHrefGroup
simple_schemas = API_control_href_group.APIControlHrefGroupSimple
create_schemas = API_control_href_group.APIControlHrefGroupCreate
update_schemas = API_control_href_group.APIControlHrefGroupUpdate
multiple_update_schemas = API_control_href_group.APIControlHrefGroupMultipleUpdate

reload_related_redis_tables = {}
