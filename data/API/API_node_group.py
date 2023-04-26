from app.SQL import models
from schemas.API import API_node_group

redis_tables = []
sql_model = models.NodeGroup
main_schemas = API_node_group.APINodeGroup
create_schemas = API_node_group.APINodeGroupCreate
update_schemas = API_node_group.APINodeGroupUpdate
multiple_update_schemas = API_node_group.APINodeGroupMultipleUpdate

reload_related_redis_tables = {}
