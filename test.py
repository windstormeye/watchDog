from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import sessionmaker

from faker import Factory

engine = create_engine('mysql+mysqldb://root:woaiwoziji123@localhost:3306/restful?charset=utf8')
Base = declarative_base()

Base.metadata.create_all(engine)
Session = sessionmaker(bind = engine)
session = Session()

# 硬件表
class Hardware(Base):
    __tablename__ = 'hardware'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    status = Column(Integer, nullable=False)
    num = Column(Integer, nullable=False)


# 添加电子原件方法
# 原件name及针脚num需要配置
# 原件状态默认关闭
def addNewUnit(hardwareName, status, num):
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    unit = Hardware(
        name = hardwareName,
        status = status,
        num = num)
    session.add(unit)
    session.commit()

#  电子原件执行read或write筛选方法
def updateStatusWithHardware(tableName, operatorStatus, hardwarename, status):
    if tableName == 'hardware':
        if operatorStatus == 1:
            return writeHardware(hardwarename, status, 0)
        else:
            return readHardware(hardwarename)
        
# 执行write操作
def writeHardware(hardwarename, status, num): 
    unit = readHardware(hardwarename)
    unit = session.query(Hardware).get(unit.id)
    if unit:
        unit.status = status
        if 'Unit' in hardwarename:
            unit.num = num;
        session.add(unit)
        session.commit()
        return '操作成功'
    return '操作失败，请联系管理员'

# 执行read操作
def readHardware(hardwarename):
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind = engine)
    session = Session()
    unit = session.query(Hardware).filter_by(name=hardwarename).first()
    return unit

