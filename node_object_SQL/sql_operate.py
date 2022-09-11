from fastapi.encoders import jsonable_encoder
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import UnmappedInstanceError


class SQLOperate:
    def __init__(self, exc):
        self.exc = exc

    def create_multiple_sql_data(self, db: Session, create_list: list, sql_model) -> list:
        try:
            add_list = list()
            for datum in create_list:
                datum = sql_model(**datum.dict())
                add_list.append(datum)
                db.add_all(add_list)
            db.flush()
            result = list()
            for datum in add_list:
                db.refresh(datum)
                result.append(datum)
            return result
        except IntegrityError as e:
            code, msg = e.orig.args
            if code == 1452:
                raise self.exc(status_code=403, detail=msg)
            elif code == 1062:
                raise self.exc(status_code=403, detail=msg)

    def get_sql_data(self, db: Session, sql_model, field_value_set: set,
                     sql_field: str = "id", check_data_list: bool = True) -> list:
        data_list = db.query(sql_model).filter(getattr(sql_model, sql_field).in_(field_value_set)).all()
        if not data_list and check_data_list:
            raise self.exc(status_code=404, detail=f"one or more {sql_field} value are not in {field_value_set}")
        return data_list

    @staticmethod
    def get_all_sql_data(db: Session, sql_model):
        skip: int = 0
        limit: int = 100
        result = list()
        while db.query(sql_model).offset(skip).limit(limit).all():
            result += db.query(sql_model).offset(skip).limit(limit).all()
            skip = limit
            limit += 100
        return [jsonable_encoder(i) for i in result]

    def update_multiple_sql_data(self, db: Session, update_list: list, sql_model):
        try:
            sql_data_list = list()
            for row in update_list:
                datum = db.query(sql_model).filter(sql_model.id == row.id).first()
                if not datum:
                    raise self.exc(status_code=404, detail=f"id:{row.id} not found")
                for item in row:
                    if item[1] is not None and item[0] != "id":
                        setattr(datum, item[0], item[1])
                db.flush()
                db.refresh(datum)
                sql_data_list.append(datum)
            return sql_data_list
        except IntegrityError as e:
            code, msg = e.orig.args
            if code == 1452:
                raise self.exc(status_code=403, detail=msg)
            elif code == 1406:
                raise self.exc(status_code=403, detail=msg)

    def delete_multiple_sql_data(self, db: Session, id_set: set, sql_model) -> list:
        try:
            delete_data_list = db.query(sql_model).filter(sql_model.id.in_(id_set)).all()
            if len(id_set) != len(delete_data_list):
                raise self.exc(status_code=404, detail=f"id: one or many of {str(id_set)} is not exist")
            stmt = delete(sql_model).where(sql_model.id.in_(id_set))
            db.execute(stmt)
            db.flush()
            return delete_data_list
        except UnmappedInstanceError:
            raise self.exc(status_code=404, detail=f"id: one or more of {str(id_set)} is not exist")


if __name__ == "__main__":
    pass
