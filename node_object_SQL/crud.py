from datetime import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import UnmappedInstanceError
from app_node_object.node_object_SQL import models
from app_node_object.node_object_SQL.database import SessionLocal
from dispatch_data.sql_model_data import models_dict
from app_node_object.node_object_exception import ColdDataException
from dispatch_schemas import task_schemas


def create_dispatch_task(db: Session, task: task_schemas.DispatchTaskCreate):
    try:
        with db.begin():
            fake_dispatch_event_id = task.job.replace(" ", "_")+"_"+str(datetime.now()).replace(" ", "_")
            db_task = models.DispatchTask(**task.dict(), dispatch_event_id=fake_dispatch_event_id)
            db.add(db_task)
        db.refresh(db_task)
        return db_task
    except IntegrityError as e:
        code, msg = e.orig.args
        if code == 1062:
            raise ColdDataException(status_code=403, detail=msg)
        elif code == 1452:
            raise ColdDataException(status_code=403, detail=msg)


def create_sql_data(db: Session, create_schemas, sql_model_name):
    model = models_dict[sql_model_name]
    try:
        with db.begin():
            datum = model(**create_schemas.dict())
            db.add(datum)
        db.refresh(datum)
        return datum
    except IntegrityError as e:
        code, msg = e.orig.args
        if code == 1452:
            raise ColdDataException(status_code=403, detail=msg)


def get_sql_data(db: Session, data_id: int, sql_model_name):
    model = models_dict[sql_model_name]
    return db.query(model).filter(model.id == data_id).first()


def get_all_sql_data(db: Session, sql_model_name):
    model = models_dict[sql_model_name]
    skip: int = 0
    limit: int = 100
    result = list()
    while db.query(model).offset(skip).limit(limit).all():
        result += db.query(model).offset(skip).limit(limit).all()
        skip = limit
        limit += 100
    return result


def update_sql_data(db: Session, update_data, data_id: int, sql_model_name):
    model = models_dict[sql_model_name]
    try:
        with db.begin():
            datum = db.query(model).filter(model.id == data_id).first()
            for item in update_data:
                if item[1] is not None:
                    setattr(datum, item[0], item[1])
        db.refresh(datum)
        return datum
    except IntegrityError as e:
        code, msg = e.orig.args
        if code == 1452:
            raise ColdDataException(status_code=403, detail=msg)
        elif code == 1406:
            raise ColdDataException(status_code=403, detail=msg)


def delete_sql_data(db: Session, data_id: int, sql_model_name):
    model = models_dict[sql_model_name]
    try:
        with db.begin():
            delete_data = db.query(model).filter(model.id == data_id).first()
            db.delete(delete_data)
        return delete_data
    except UnmappedInstanceError:
        raise ColdDataException(status_code=404, detail=f"id:{str(data_id)} is not exist")


if __name__ == "__main__":
    db2 = SessionLocal()
    # ex = db2.query(models.DispatchTask).filter(models.DispatchTask.id == 2).first()
    ex = db2.query(models.DispatchLevel).filter(models.DispatchLevel.id == 2).first()
    print(type(ex.task))
    a = jsonable_encoder(ex.task)
    # print(type(jsonable_encoder(ex)))
    # a = task_schemas.DispatchTask(**jsonable_encoder(ex), confirm=ex.confirm)
    # print(a.json())
    # b = status_schemas.DispatchStatus(**jsonable_encoder(ex.status))
    # print(b.json())
