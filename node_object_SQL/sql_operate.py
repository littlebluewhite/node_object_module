from fastapi.encoders import jsonable_encoder
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import UnmappedInstanceError


class SQLOperate:
    def __init__(self, exc):
        self.exc = exc
        self.null_set = {0, ""}

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
        update_data_dict = dict()
        update_data_id_set = set()
        try:
            for update_data in update_list:
                update_data_dict[update_data.id] = update_data
                update_data_id_set.add(update_data.id)
            sql_data_list = db.query(sql_model).filter(sql_model.id.in_({i.id for i in update_list})).all()
            if len(sql_data_list) != len(update_data_id_set):
                raise self.exc(status_code=404, detail=f"id: one or many of {update_data_id_set} is not exist")
            for sql_data in sql_data_list:
                update_data = update_data_dict[getattr(sql_data, "id")]
                for item in update_data:
                    print(item)
                    if item[1] is not None and item[0] != "id":
                        if type(item[1]) == str or type(item[1]) == int:
                            if item[1] in self.null_set:
                                setattr(sql_data, item[0], None)
                            else:
                                setattr(sql_data, item[0], item[1])
                        else:
                            setattr(sql_data, item[0], item[1])
                db.flush()
                db.refresh(sql_data)
            return sql_data_list
        except IntegrityError as e:
            code, msg = e.orig.args
            if code == 1452:
                raise self.exc(status_code=403, detail=msg)
            elif code == 1406:
                raise self.exc(status_code=403, detail=msg)
        except UnmappedInstanceError:
            raise self.exc(status_code=404, detail=f"id: one or more of {update_data_id_set} is not exist")

    def delete_multiple_sql_data(self, db: Session, id_set: set, sql_model) -> list:
        try:
            delete_data_list = db.query(sql_model).filter(sql_model.id.in_(id_set)).all()
            if len(id_set) != len(delete_data_list):
                raise self.exc(status_code=404, detail=f"id: one or many of {str(id_set)} is not exist")
            stmt = delete(sql_model).where(sql_model.id.in_(id_set))
            db.execute(stmt)
            db.flush()
            return delete_data_list
        except IntegrityError as e:
            code, msg = e.orig.args
            if code == 1451:
                raise self.exc(status_code=403, detail=msg)
        except UnmappedInstanceError:
            raise self.exc(status_code=404, detail=f"id: one or more of {str(id_set)} is not exist")


if __name__ == "__main__":
    pass
