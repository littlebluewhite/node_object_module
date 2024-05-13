from app.SQL import models
from schemas.API import API_node_group
from schemas.API import API_node

redis_tables = []
sql_model = models.NodeNodeGroup
main_schemas = API_node_group.APINodeGroupMain
create_schemas = API_node_group.APINodeGroupCreate
update_schemas = API_node_group.APINodeGroupUpdate
multiple_update_schemas = API_node_group.APINodeGroupMultipleUpdate
node_schemas = API_node.APINode

reload_related_redis_tables = {}
