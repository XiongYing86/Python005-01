# Author : chen wei
# Date : 2020-12-13
'''
使用 sqlalchemy ORM 方式创建如下表，使用 PyMySQL 对该表写入 3 条测试数据，并读取:
用户 id、用户名、年龄、生日、性别、学历、字段创建时间、字段更新时间
将 ORM、插入、查询语句作为作业内容提交
'''
import pymysql
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import DateTime

# 创建一个Base实例，必须继承declarative_base
Base = declarative_base()


class User_table(Base):
    __tablename__ = 'user'  # 属性
    user_id = Column(Integer(), primary_key=True)
    user_name = Column(String(20))
    user_age = Column(Integer())
    user_shengri = Column(String(20))
    user_sex = Column(Enum('男', '女'))
    user_xueli = Column(String(8))
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return "User_table(user_id={self.user_id}," \
                "user_name={self.user_name},"\
                "user_age={self.user_age},"\
                "user_shengri={self.user_shengri},"\
                "user_sex={self.user_sex},"\
                "user_xueli={self.user_xueli})".format(self=self)


dburl = "mysql+pymysql://chenwei1:Chenwei@123456@127.0.0.1:3306/tsdb_mb4"
engine = create_engine(dburl, echo=True, encoding='UTF-8')

# 创建表
Base.metadata.create_all(engine)

# 创建session
sessionClass = sessionmaker(bind=engine)
session = sessionClass()
# 增加数据
user_demo = User_table(user_name='zhangsan', user_age=17, user_shengri='2003-11-12', user_xueli='大专',
                       user_sex='男')  # 类的实例化
user_demo1 = User_table(user_name='lisi', user_age=27, user_shengri='1993-10-10', user_xueli='硕士',
                        user_sex='女')
user_demo2 = User_table(user_name='王麻子', user_age=60, user_shengri='1960-03-03', user_xueli='高中',
                        user_sex='男')
session.add(user_demo)
session.add(user_demo1)
session.add(user_demo2)

# 把查询的数据打印出来
for result in session.query(User_table):
    print(result)

session.commit()
