from node_object_SQL import models

if __name__ == "__main__":
    a = models.Node(id=1)
    print(getattr(models.Node, "id"))
