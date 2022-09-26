from sqlalchemy import update

from node_object_SQL import models
from node_object_SQL.database import SQLDB

if __name__ == "__main__":
    db_config = {
        "host": "127.0.0.1",
        "port": "3306",
        "db": "node_object",
        "user": "root",
        "password": "123456"
    }
    db_session = SQLDB(db_config).new_db_session()()
    a = models.Node(id=1)
    print(a)
    c = {"name": "tt", "principal_name": None}
    print(getattr(models.Node, "name"))
    stmt = update(models.Node).where(models.Node.id == 7).values(**c)
    v = db_session.execute(stmt)
    db_session.commit()
    print("v: ", v)

