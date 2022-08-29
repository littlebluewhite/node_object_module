import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON, DateTime, Table, Float
from sqlalchemy.orm import relationship

from node_object_SQL.database import Base

node_node_group = \
    Table('node_node_group', Base.metadata,
          Column('node_id', Integer, ForeignKey('node.id')),
          Column('node_group_id', Integer, ForeignKey('node_group.id'))
          )

object_object_group = \
    Table('object_object_group', Base.metadata,
          Column('object_id', Integer, ForeignKey('object.id')),
          Column('object_group_id', Integer, ForeignKey('object_group.id'))
          )


# 節點群組
class NodeGroup(Base):
    __tablename__ = "node_group"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(256))  # 節點群組名稱
    is_topics = Column(Boolean, default=True, nullable=False)  # 是否為主題
    description = Column(String(256))

    update_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)  # 最後更新時間

    nodes = relationship("Node", back_populates="node_groups", secondary=node_node_group)


# 節點
class Node(Base):
    __tablename__ = "node"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    node_id = Column(String(256))  # 設備(節點)對應真實的物件id，可能是來自於廠商整合的hub、SCADA、不同protocol的uuid
    name = Column(String(256))  # 節點名稱
    principal_name = Column(String(256))  # 節點負責人
    last_maintain_date = Column(DateTime)  # 節點最後維護時間
    next_maintain_date = Column(DateTime)  # 節點下次維護時間
    tags = Column(JSON)  # 節點標籤
    parent_node_id = Column(Integer, ForeignKey("node.id"))
    node_base_id = Column(Integer, ForeignKey("node_base.id"), unique=True)
    third_dimension_instance_id = Column(Integer, ForeignKey("third_dimension_instance.id"), unique=True)

    create_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    update_time = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)  # 最後更新時間

    node_base = relationship("NodeBase")
    child_node = relationship("Node",
                              lazy="joined",
                              join_depth=30)
    third_dimension_instance = relationship("ThirdDimensionInstance", back_populates="node", lazy="joined")
    object = relationship("Object", back_populates="node", lazy="joined")
    node_groups = relationship("NodeGroup", back_populates="nodes",
                               secondary=node_node_group)  # 節點所屬的節點群組，這是一張列表，表示這個點為可能屬於多個節點群組


class NodeBase(Base):
    __tablename__ = "node_base"

    description = Column(String(256))  # 節點文字描述
    value = Column(String(256))
    node_type = Column(String(256), default=None)  # 節點資訊id，表示該節點對應到的資訊，用以反向查詢該節點的資訊索引
    device_info_id = Column(Integer, ForeignKey("device_info.id"), unique=True)

    device_info = relationship("DeviceInfo", back_populates="node_base")


# 3D物件
class ThirdDimensionInstance(Base):
    __tablename__ = "third_dimension_instance"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    streaming_url = Column(String(256), default=None)  # 該節點的影像串流位置(可能是CCTV或複合式設備)
    image_url = Column(String(256), default=None)  # 該節點的影片路徑、網址
    area = Column(String(256), default=None)  # 描述節點所屬樓層、區域
    floor = Column(String(256), default=None)  # 描述節點所屬樓層

    position = Column(JSON)  # {"x":0.0,"y":0.0,"z":0.0} 節點世界座標
    rotation = Column(JSON)  # {"x":0.0,"y":0.0,"z":0.0} 節點旋轉Euler角(0.0~360.0)
    scale = Column(JSON)  # {"x":0.0,"y":0.0,"z":0.0} 節點縮放大小
    model_url = Column(String(256), default=None)  # 節點的模型路徑 TODO 目前是第一版先以本地路徑、第二版是結合後端的FileSys指向雲端的路徑
    location_path = Column(String(256), default=None)  # 階層路徑 (或是用ParentId, 可為空<root>)
    layer_id = Column(Integer, default=0)  # 節點定義層級 (Building/Floor/Room/Device/Pipe/Sensor) TODO 也許透過 Node 概念來解決?

    update_time = Column(DateTime, default=datetime.datetime.now)  # 最後更新時間

    node = relationship("Node", back_populates="third_dimension_instance", lazy="joined")
    node_scheme = relationship("NodeSchemes", back_populates="third_dimension_instance", lazy="joined")


# 節點資訊
class DeviceInfo(Base):
    __tablename__ = "device_info"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))  # 節點資訊名稱
    company = Column(String(256))  # 節點廠商
    contact_name = Column(String(256))  # 節點聯絡人
    phone_number = Column(Integer)  # 節點廠商連絡電話
    email = Column(String(256))  # 節點廠商連絡電子郵件

    node_base = relationship("NodeBase", back_populates="device_info", lazy="joined")


# 物件群組
class ObjectGroup(Base):
    __tablename__ = "object_group"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))  # 節點資訊名稱
    description = Column(String(256), default=None)  # 點位(物件)群組文字描述

    is_topics = Column(Integer(), default=1)  # 是否為主題

    update_time = Column(DateTime, default=datetime.datetime.now)  # 最後更新時間

    node_group = relationship("NodeGroup", back_populates="object_group", secondary=node_group_and_object_group)
    object = relationship("Object", back_populates="object_group", secondary=object_group_and_object)
    object_scheme = relationship("ObjectScheme", back_populates="object_group",
                                 secondary=object_group_and_object_scheme)


# 點位(物件)
class Object(Base):
    __tablename__ = "object"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))  # 點位(物件)名稱

    node_id = Column(Integer, ForeignKey("node.id"), default=None)  # 點位(物件)所屬的節點，是個列表，"僅含一個節點"
    node = relationship("Node", back_populates="object", lazy="immediate")

    object_id = Column(String(256), default=None)  # 這不是自身關聯，而是對應真實的物件id，可能是來自於廠商整合的hub、SCADA、不同protocol的uuid
    value = Column(String(256), default=None)  # 點位(物件)的值
    unit = Column(String(256), default=None)  # 點位(物件)的單位，可能是百分比、度C、攝氏、莫氏硬度、百帕...等等

    description = Column(String(256), default=None)  # 點位(物件)文字描述
    data_type = Column(String(256), default=None)  # 描述點位(物件)Value的類型

    calculator_reader = Column(String(256), default=None)  # 點位(物件)讀取資料的運算方式，僅限數值類[float、int、bool]
    calculator_writer = Column(String(256), default=None)  # 點位(物件)寫入資料的運算方式，僅限數值類[float、int、bool]

    max_value = Column(Float, default=None)  # 點位(物件)最大值，僅限數值類
    min_value = Column(Float, default=None)  # 點位(物件)最小值，僅限數值類
    dec = Column(Integer, default=0)  # 顯示上允許的小數點位數

    control_able = Column(Boolean, default=0)  # 點位(物件)是否可控
    control_href_group_id = Column(Integer, ForeignKey("control_href_group.id"), default=None)  # 點位(物件)控制選像
    fake_data_config_id = Column(Integer, ForeignKey("fake_data_config.id"), default=None)  # 點位(物件)所屬的假資料設定Id
    object_scheme_id = Column(Integer, ForeignKey("object_scheme.id"), default=None)  # 點位(物件)所屬樣式Id

    update_time = Column(DateTime, default=datetime.datetime.now)  # 最後更新時間

    object_group = relationship("ObjectGroup", back_populates="object", secondary=object_group_and_object)
    control_href_group = relationship("ControlHrefGroup", back_populates="object", lazy="immediate")
    fake_data_config = relationship("FakeDataConfig", back_populates="object", lazy="immediate")
    object_scheme = relationship("ObjectScheme", back_populates="object", lazy="immediate")


# 控制選項列表
class ControlHrefGroup(Base):
    __tablename__ = "control_href_group"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))  # 控制選項列表名稱

    control_href_item = relationship("ControlHrefItem", back_populates="control_href_group", lazy="immediate")  # 控制選項
    object = relationship("Object", back_populates="control_href_group", lazy="immediate")
    object_scheme = relationship("ObjectScheme", back_populates="control_href_group", lazy="immediate")


# 控制選項
class ControlHrefItem(Base):
    __tablename__ = "control_href_item"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))  # 控制選項列表名稱
    control_data = Column(String(256))  # 控制選項所帶的參數，可能是URL、後端的某個命令、參數等等
    color = Column(String(256))  # 選項自帶的色票

    control_href_group_id = Column(Integer, ForeignKey("control_href_group.id"), default=None)  # 控制選項
    control_href = relationship("ControlHrefGroup", back_populates="control_href_item", lazy="immediate")


# 假資料設定檔
class FakeDataConfig(Base):
    __tablename__ = "fake_data_config"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))  # 假資料設定檔名稱
    faking_frequency = Column(Float, default=5.0)  # 打假資料的頻率
    faking_default_value = Column(Float, default=0.0)  # 假資料預設值
    faking_inc_limit = Column(Float, default=0.0)  # 假資料增加上限
    faking_dec_limit = Column(Float, default=0.0)  # 假資料減少上限
    faking_extra_info = Column(Float, default=0.0)  # 假資料額外資訊

    object = relationship("Object", back_populates="fake_data_config", lazy="immediate")
    object_scheme = relationship("ObjectScheme", back_populates="fake_data_config", lazy="immediate")


# 點位(物件)樣式
class ObjectScheme(Base):
    __tablename__ = "object_scheme"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))  # 點位(物件)樣式群組名稱
    unit = Column(String(256), default=None)  # 點位(物件)的單位，可能是百分比、度C、攝氏、莫氏硬度、百帕...等等

    description = Column(String(256), default=None)  # 點位(物件)文字描述
    data_type = Column(String(256), default=None)  # 描述點位(物件)Value的類型

    calculator_reader = Column(String(256), default=None)  # 點位(物件)讀取資料的運算方式，僅限數值類[float、int、bool]
    calculator_writer = Column(String(256), default=None)  # 點位(物件)寫入資料的運算方式，僅限數值類[float、int、bool]

    max_value = Column(Float, default=None)  # 點位(物件)最大值，僅限數值類
    min_value = Column(Float, default=None)  # 點位(物件)最小值，僅限數值類
    dec = Column(Integer, default=0)  # 顯示上允許的小數點位數

    control_able = Column(Boolean, default=0)  # 點位(物件)是否可控
    control_href_group_id = Column(Integer, ForeignKey("control_href_group.id"), default=None)  # 點位(物件)控制選像
    fake_data_config_id = Column(Integer, ForeignKey("fake_data_config.id"), default=None)  # 點位(物件)所屬的假資料設定Id

    update_time = Column(DateTime, default=datetime.datetime.now)  # 最後更新時間

    node_scheme_id = Column(Integer, ForeignKey("node_scheme.id"), default=None)

    object_group = relationship("ObjectGroup", back_populates="object_scheme", secondary=object_group_and_object_scheme)
    control_href_group = relationship("ControlHrefGroup", back_populates="object_scheme", lazy="immediate")
    fake_data_config = relationship("FakeDataConfig", back_populates="object_scheme", lazy="immediate")
    object_scheme = relationship("Object", back_populates="object_scheme", lazy="immediate")


# 節點樣式
class NodeSchemes(Base):
    __tablename__ = "node_scheme"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))  # 節點樣式群組名稱
    description = Column(String(256), default=None)  # 節點樣式文字描述

    parent_node_scheme_id = Column(Integer, ForeignKey("node_scheme.id"), default=None)
    child_node_scheme = relationship("NodeSchemes",
                                     lazy="joined",
                                     join_depth=5)
    # child_node_scheme = relationship(
    #     "NodeSchemes",
    #     secondary=parent_node_scheme,
    #     primaryjoin=(parent_node_scheme.c.parent_node_scheme_id == id),
    #     secondaryjoin=(parent_node_scheme.c.child_node_scheme_id == id),
    #     lazy="joined",
    #     backref=backref('parent_node_scheme', lazy='joined')
    # )

    node_type = Column(String(256), default=None)  # 節點資訊id，表示該節點對應到的資訊，用以反向查詢該節點的資訊索引

    third_dimension_instance_id = Column(Integer, ForeignKey("third_dimension_instance.id"), default=None)
    third_dimension_instance = relationship("third_dimension_instance", back_populates="node_scheme", lazy="joined")

    object_scheme = relationship("ObjectScheme", back_populates="node_scheme", lazy="joined")
    node_group = relationship("NodeGroup", back_populates="node_scheme",
                              secondary=node_group_and_node_schemes)  # 節點所屬的節點群組，這是一張列表，表示這個點為可能屬於多個節點群組

    node_info_id = Column(Integer, ForeignKey("node_info.id"), default=None)
    node_info = relationship("NodeInfo", back_populates="node_scheme",
                             lazy="joined")  # 節點資訊id，表示該節點對應到的資訊，用以反向查詢該節點的資訊索引

    update_time = Column(DateTime, default=datetime.datetime.now)  # 最後更新時間
