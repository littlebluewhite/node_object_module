from node_object_SQL import models
from node_object_schemes.API import API_node
redis_tables = []
sql_model = models.Node
main_schemas = API_node.APINode
create_schemas = API_node.APINodeCreate
update_schemas = API_node.APINodeUpdate
multiple_update_schemas = API_node.APINodeMultipleUpdate

reload_related_redis_tables = {}
