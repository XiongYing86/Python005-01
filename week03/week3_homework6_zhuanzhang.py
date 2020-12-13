# Author : chen wei
# Date : 2020-12-13
'''
张三给李四通过网银转账 100 极客币，现有数据库中三张表：
一张为用户表，包含用户 ID 和用户名字，另一张为用户资产表，包含用户 ID 用户总资产，
第三张表为审计用表，记录了转账时间，转账 id，被转账 id，转账金额。
请合理设计三张表的字段类型和表结构；
请实现转账 100 极客币的 SQL(可以使用 pymysql 或 sqlalchemy-orm 实现)，张三余额不足，转账过程中数据库 crash 等情况需保证数据一致性。
'''

import pymysql
import sys
from datetime import datetime


class TransferMoney(object):
    """定义一个转账的类"""

    def __init__(self, db):
        self.db = db

    # 检查账户
    def check_acct_available(self, name):
        cursor = self.db.cursor()
        try:
            sql = "select * from user3 where name = '%s'" % name
            cursor.execute(sql)
            print(f'check_acct_available:{sql}')
            rs = cursor.fetchall()
            if len(rs) != 1:
                raise Exception("账号%s不存在" % name)
        finally:
            cursor.close()

    # 检查余额
    def has_enough_money(self, name, money):
        cursor = self.db.cursor()
        try:
            sql = "select money from zichan where id in (select id from user3 where name = '%s') and money>%s" % (
                name, money)
            cursor.execute(sql)
            print(f'has_enough_money: {sql}')
            rs = cursor.fetchall()
            if len(rs) != 1:
                raise Exception("账号%s没有足够的钱" % name)
        finally:
            cursor.close()

    # 一个账户减款
    def reduce_money(self, name, money):
        cursor = self.db.cursor()
        try:
            sql = "update zichan set money = money-%s where id in (select id from user3 where name = '%s')" % (
                money, name)
            cursor.execute(sql)
            print(f'reduce_money:{sql}')
            if cursor.rowcount != 1:
                raise Exception("账号%s减款失败" % name)
        finally:
            cursor.close()

    # 一个账户加款
    def add_money(self, name, money):
        cursor = self.db.cursor()
        try:
            sql = "update zichan set money = money+%s where id in (select id from user3 where name = '%s')" % (
                money, name)
            cursor.execute(sql)
            print(f'add_money:{sql}')
            if cursor.rowcount != 1:
                raise Exception("账号%s加款失败" % name)
        finally:
            cursor.close()

    # 转账
    def transfer(self, source_name, target_name, money):
        try:
            self.check_acct_available(source_name)
            self.check_acct_available(target_name)
            self.has_enough_money(source_name, money)
            self.reduce_money(source_name, money)
            self.add_money(target_name, money)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e


if __name__ == '__main__':
    # source_name = sys.argv[1]
    # target_name = sys.argv[2]
    # money = sys.argv[3]
    source_name = input("请输入转账人：")
    target_name = input("请输入被转帐人：")
    money = float(input("请输入转款数："))
    # 定义数据库连接
    db = pymysql.connect("127.0.0.1", "chenwei1", "Chenwei@123456", "tsdb_mb4")
    tr_money = TransferMoney(db)
    # 检查转账是否成功。
    try:
        tr_money.transfer(source_name, target_name, money)
        time1 = datetime.now()
        sql1 = "select id from user3 where name = '%s'" % source_name
        zid = db.cursor().execute(sql1)
        sql2 = "select id from user3 where name = '%s'" % target_name
        bzid = db.cursor().execute(sql2)
        sql = "INSERT INTO audit (zhuanzhang_time,zhuanzhang_id,beizhuanzhuang_id,zhuanzhuang_money) Values(%s,%s,%s,%s)"
        value = (time1, zid, bzid, money) # 转账id和被转账id暂时还未获取到，待再想办法
        db.cursor().execute(sql, value)
        db.commit()
    except Exception as e:
        print(f'转账出问题了: {e}')
    finally:
        db.close()
