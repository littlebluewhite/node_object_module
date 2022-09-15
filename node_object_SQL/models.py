import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON, DateTime, Float
from sqlalchemy.orm import relationship

from node_object_SQL.database import Base


class NodeNodeGroup(Base):
    __tablename__ = "node_node_group"

    node_id = Column('node_id', Integer, ForeignKey('node.id'), primary_key=True)
    node_group_id = Column('node_group_id', Integer, ForeignKey('node_group.id'), primary_key=True)


class ObjectObjectGroup(Base):
    __tablename__ = "object_object_group"

    object_id = Column('object_id', Integer, ForeignKey('object.id'), primary_key=True)
    object_group_id = Column('object_group_id', Integer, ForeignKey('object_group.id'), primary_key=True)


class NodeBase(Base):
    __tablename__ = "node_base"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    description = Column(String(256))  # 節點文字描述
    value = Column(String(256))
    node_type = Column(String(256), default=None)  # 節點資訊id，表示該節點對應到的資訊，用以反向查詢該節點的資訊索引

    device_info = relationship("DeviceInfo", lazy="joined")


# 節點
class Node(Base):
    __tablename__ = "node"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    node_id = Column(String(256), unique=True, nullable=False)  # 設備(節點)對應真實的物件id，可能是來自於廠商整合的hub、SCADA、不同protocol的uuid
    name = Column(String(256))  # 節點名稱
    principal_name = Column(String(256))  # 節點負責人
    last_maintain_date = Column(DateTime)  # 節點最後維護時間
    next_maintain_date = Column(DateTime)  # 節點下次維護時間
    tags = Column(JSON)  # 節點標籤
    parent_node_id = Column(Integer, ForeignKey("node.id"))
    node_base_id = Column(Integer, ForeignKey("node_base.id"), unique=True)

    create_at = Column(DateTime, default=datetime.datetime.now)
    update_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)  # 最後更新時間

    node_base = relationship("NodeBase", lazy="joined", uselist=False)
    child_nodes = relationship("Node",
                               lazy="joined",
                               join_depth=2)
    third_dimension_instance = relationship("ThirdDimensionInstance", lazy="joined", uselist=False)
    objects = relationship("Object", back_populates="node", lazy="joined")
    node_groups = relationship("NodeNodeGroup", lazy="joined")  # 節點所屬的節點群組，這是一張列表，表示這個點為可能屬於多個節點群組


class NodeTemplate(Base):
    __tablename__ = "node_template"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(256))  # 節點名稱
    node_template_id = Column(String(256))  # 設備(節點)對應真實的物件id，可能是來自於廠商整合的hub、SCADA、不同protocol的uuid
    parent_node_id = Column(Integer, ForeignKey("node.id"))
    node_base_id = Column(Integer, ForeignKey("node_base.id"), unique=True)

    update_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)  # 最後更新時間

    node_base = relationship("NodeBase", lazy="joined", uselist=False)
    child_node_templates = relationship("Node",
                                        lazy="joined",
                                        join_depth=2)
    object_templates = relationship("ObjectTemplate", lazy="joined")


# 節點群組
class NodeGroup(Base):
    __tablename__ = "node_group"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(256), nullable=False, unique=True)  # 節點群組名稱
    is_topics = Column(Boolean, default=True, nullable=False)  # 是否為主題
    description = Column(String(256))

    update_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)  # 最後更新時間

    nodes = relationship("NodeNodeGroup", lazy="joined")


# 3D物件
class ThirdDimensionInstance(Base):
    __tablename__ = "third_dimension_instance"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    streaming_url = Column(String(256))  # 該節點的影像串流位置(可能是CCTV或複合式設備)
    image_url = Column(String(256))  # 該節點的影片路徑、網址
    area = Column(String(256))  # 描述節點所屬樓層、區域
    floor = Column(String(256))  # 描述節點所屬樓層
    position = Column(JSON)  # {"x":0.0,"y":0.0,"z":0.0} 節點世界座標
    rotation = Column(JSON)  # {"x":0.0,"y":0.0,"z":0.0} 節點旋轉Euler角(0.0~360.0)
    scale = Column(JSON)  # {"x":0.0,"y":0.0,"z":0.0} 節點縮放大小
    model_url = Column(String(256))  # 節點的模型路徑 TODO 目前是第一版先以本地路徑、第二版是結合後端的FileSys指向雲端的路徑
    location_path = Column(String(256))  # 階層路徑 (或是用ParentId, 可為空<root>)
    layer_id = Column(Integer)  # 節點定義層級 (Building/Floor/Room/Device/Pipe/Sensor) TODO 也許透過 Node 概念來解決?

    node_id = Column(Integer, ForeignKey("node.id"), unique=True)

    update_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)  # 最後更新時間


# 節點資訊
class DeviceInfo(Base):
    __tablename__ = "device_info"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))  # 節點資訊名稱
    company = Column(String(256))  # 節點廠商
    contact_name = Column(String(256))  # 節點聯絡人
    phone_number = Column(String(256))  # 節點廠商連絡電話
    email = Column(String(256))  # 節點廠商連絡電子郵件
    extra_info = Column(String(256))

    node_base_id = Column(Integer, ForeignKey("node_base.id"), unique=True)


class ObjectBase(Base):
    __tablename__ = "object_base"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(String(256))  # 點位(物件)的值
    unit = Column(String(256))  # 點位(物件)的單位，可能是百分比、度C、攝氏、莫氏硬度、百帕...等等
    description = Column(String(256))  # 點位(物件)文字描述
    data_type = Column(String(256))  # 描述點位(物件)Value的類型
    calculator_reader = Column(String(256))  # 點位(物件)讀取資料的運算方式，僅限數值類[float、int、bool]
    calculator_writer = Column(String(256))  # 點位(物件)寫入資料的運算方式，僅限數值類[float、int、bool]
    max_value = Column(Float)  # 點位(物件)最大值，僅限數值類
    min_value = Column(Float)  # 點位(物件)最小值，僅限數值類
    dec = Column(Integer, default=0)  # 顯示上允許的小數點位數
    is_control = Column(Boolean, default=False)  # 點位(物件)是否可控


# 點位(物件)
class Object(Base):
    __tablename__ = "object"

    id = Column(Integer, primary_key=True, index=True)
    # 這不是自身關聯，而是對應真實的物件id，可能是來自於廠商整合的hub、SCADA、不同protocol的uuid
    object_id = Column(String(256), unique=True, nullable=False)
    name = Column(String(256))  # 點位(物件)名稱
    object_base_id = Column(Integer, ForeignKey("object_base.id"), unique=True)
    node_id = Column(Integer, ForeignKey("node.id"), unique=True)  # 點位(物件)所屬的節點，是個列表，"僅含一個節點"
    tags = Column(JSON, default=list())
    control_href_group_id = Column(Integer, ForeignKey("control_href_group.id"))

    create_at = Column(DateTime, default=datetime.datetime.now)
    update_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)  # 最後更新時間

    node = relationship("Node", back_populates="objects", lazy="immediate", uselist=False)
    object_base = relationship("ObjectBase", lazy="immediate", uselist=False)
    object_groups = relationship("ObjectObjectGroup", lazy="joined")
    control_href_group = relationship("ControlHrefGroup", lazy="immediate", uselist=False)
    fake_data_config = relationship("FakeDataConfig", lazy="immediate", uselist=False)


class ObjectTemplate(Base):
    __tablename__ = "object_template"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))  # 點位(物件)名稱
    object_base_id = Column(Integer, ForeignKey("object_base.id"), unique=True)
    # 點位(物件)所屬的假資料設定Id
    node_template_id = Column(Integer, ForeignKey("node_template.id"), unique=True)  # 點位(物件)所屬的節點，是個列表，"僅含一個節點"

    update_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)  # 最後更新時間

    object_base = relationship("ObjectBase", lazy="joined", uselist=False)
    # 點位(物件)控制選像
    control_href_group_template = relationship("ControlHrefGroupTemplate", lazy="immediate", uselist=False)
    fake_data_config_template = relationship("FakeDataConfigTemplate", lazy="immediate", uselist=False)


# 物件群組
class ObjectGroup(Base):
    __tablename__ = "object_group"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False, unique=True)  # 節點資訊名稱
    is_topics = Column(Boolean, default=True, nullable=False)  # 是否為主題
    description = Column(String(256))  # 點位(物件)群組文字描述

    update_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)  # 最後更新時間

    objects = relationship("ObjectObjectGroup", lazy="joined")


# 控制選項列表
class ControlHrefGroup(Base):
    __tablename__ = "control_href_group"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False, unique=True)  # 控制選項列表名稱
    tags = Column(JSON)  # 節點標籤

    create_at = Column(DateTime, default=datetime.datetime.now)
    update_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)  # 最後更新時間

    control_href_items = relationship("ControlHrefItem", back_populates="control_href_group", lazy="immediate")  # 控制選項


class ControlHrefGroupTemplate(Base):
    __tablename__ = "control_href_group_template"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False, unique=True)  # 控制選項列表名稱

    object_template_id = Column(Integer, ForeignKey("object_template.id"), unique=True)

    update_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)  # 最後更新時間

    control_href_item_templates = relationship("ControlHrefItemTemplate", back_populates="control_href_group_template",
                                               lazy="immediate")  # 控制選項


# 控制選項
class ControlHrefItem(Base):
    __tablename__ = "control_href_item"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))  # 控制選項列表名稱
    control_data = Column(String(256))  # 控制選項所帶的參數，可能是URL、後端的某個命令、參數等等
    color = Column(String(256))  # 選項自帶的色票
    control_href_group_id = Column(Integer, ForeignKey("control_href_group.id"))  # 控制選項
    tags = Column(JSON)  # 節點標籤

    create_at = Column(DateTime, default=datetime.datetime.now)
    update_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)  # 最後更新時間

    control_href_group = relationship("ControlHrefGroup", back_populates="control_href_items", lazy="immediate")


class ControlHrefItemTemplate(Base):
    __tablename__ = "control_href_item_template"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))  # 控制選項列表名稱
    control_data = Column(String(256))  # 控制選項所帶的參數，可能是URL、後端的某個命令、參數等等
    color = Column(String(256))  # 選項自帶的色票
    control_href_group_template_id = Column(Integer, ForeignKey("control_href_group_template.id"))  # 控制選項

    update_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)  # 最後更新時間

    control_href_group_template = relationship("ControlHrefGroupTemplate",
                                               back_populates="control_href_item_templates",
                                               lazy="immediate")


# 假資料設定檔
class FakeDataConfigBase(Base):
    __tablename__ = "fake_data_config_base"

    id = Column(Integer, primary_key=True, index=True)
    faking_frequency = Column(Float, default=5.0)  # 打假資料的頻率
    faking_default_value = Column(Float, default=0.0)  # 假資料預設值
    faking_inc_limit = Column(Float, default=0.0)  # 假資料增加上限
    faking_dec_limit = Column(Float, default=0.0)  # 假資料減少上限
    faking_extra_info = Column(Float, default=0.0)  # 假資料額外資訊


class FakeDataConfig(Base):
    __tablename__ = "fake_data_config"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))  # 假資料設定檔名稱
    fake_data_config_base_id = Column(Integer, ForeignKey("fake_data_config_base.id"), unique=True)
    object_id = Column(Integer, ForeignKey("object.id"), unique=True)

    create_at = Column(DateTime, default=datetime.datetime.now)
    update_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)  # 最後更新時間

    fake_data_config_base = relationship("FakeDataConfigBase", lazy="immediate", uselist=False)


class FakeDataConfigTemplate(Base):
    __tablename__ = "fake_data_config_template"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))  # 假資料設定檔名稱
    fake_data_config_base_id = Column(Integer, ForeignKey("fake_data_config_base.id"), unique=True)
    object_template_id = Column(Integer, ForeignKey("object_template.id"), unique=True)

    update_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)  # 最後更新時間

    fake_data_config_base = relationship("FakeDataConfigBase", lazy="immediate", uselist=False)
