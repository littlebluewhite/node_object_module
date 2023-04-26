from function.General_operate import GeneralOperate
import data.node
import data.node_base
import data.third_dimension_instance
import data.device_info
import data.node_node_group
import data.node_group

class APINodeGroupFunction:
    pass

class APINodeGroupOperate(GeneralOperate, APINodeGroupFunction):
    def __init__(self, module, redis_db, exc):
        self.exc = exc
        GeneralOperate.__init__(self, module, redis_db, exc)
        self.node_operate = GeneralOperate(data.node, redis_db, exc)
        self.node_base_operate = GeneralOperate(data.node_base, redis_db, exc)
        self.third_d_operate = GeneralOperate(data.third_dimension_instance, redis_db, exc)
        self.device_info_operate = GeneralOperate(data.device_info, redis_db, exc)
        self.nn_group_operate = GeneralOperate(data.node_node_group, redis_db, exc)
        self.node_group_operate = GeneralOperate(data.node_group, redis_db, exc)

    def get_APINode_group(self):
        pass



