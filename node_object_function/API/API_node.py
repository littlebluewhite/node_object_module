class APINodeFunction:
    @staticmethod
    def format_api_node(node):
        child_nodes = []
        node_groups = []
        objects = []
        for item in node["child_nodes"]:
            child_nodes.append(item["id"])
        for item in node["node_groups"]:
            node_groups.append(item["node_group_id"])
        for item in node["objects"]:
            objects.append(item["id"])
        node["child_nodes"] = child_nodes
        node["node_groups"] = node_groups
        node["objects"] = objects
        return node
