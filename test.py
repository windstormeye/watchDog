from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import sessionmaker

from faker import Factory

engine = create_engine('mysql+mysqldb://root:woaiwoziji123@localhost:3306/restful?charset=utf8')
Base = declarative_base()

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
def addNewUnit():
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    unit = Hardware(
        name = 'redLED',
        status = 0,
        num = 1)
    session.add(unit)
    session.commit()

#  电子原件执行read或write筛选方法
def updateStatusWithHardware(tableName, operatorStatus, hardwareNum, status):
    if tableName == 'hardware':
        if operatorStatus == 1:
            return writeHardware(hardwareNum, status)
        else:
            readHardware(hardwareNum)
        
# 执行write操作
def writeHardware(hardwareNum, status):
    if readHardware('redLED') == 1 and status == 1:
        return '已开启'
    if readHardware('redLED') == 0 and status == 0:
        return '已关闭'
    
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind = engine)
    session = Session()
    unit = session.query(Hardware).get(hardwareNum)
    unit.status = status;
    session.add(unit)
    session.commit()
    return '操作成功'


# 执行read操作
def readHardware(harawareNum):
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind = engine)
    session = Session()
    unit = session.query(Hardware).filter_by(name=harawareNum).first()
    return unit.status


