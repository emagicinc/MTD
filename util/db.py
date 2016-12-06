# -*- coding: utf-8 -*-
# Copyright: Damien Elmes <anki@ichi2.net>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

#150525已调整完毕

import os, time
#import sqlite3 as sqlite
#import sqlalchemy as sa
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
import pandas as pd

#from sqlalchemy.ext.declarative import declarative_base #创建基类用
#Base = declarative_base() #基类
#from sqlalchemy import Column, Integer, String #可用来将数据库映射过来
##构建一个基类，查询Subtask表中的id和title.其它字段要查的话，统一放到这个基类中
#class Sub(Base):
#     __tablename__= 'Subtask'
#     id= Column(Integer, primary_key=True)
#     title = Column(String)
##创建会话
#Session = sessionmaker(bind=engine)
#se = Session() #用这个se就可以去查询了
##例如，查Sub基类（实际上是在查Subtask表）的，迭代出title字段值：
#for i in se.query(Sub).order_by(Sub.id):
#    print(i.title)
##查询的时候还可以切片：
#for u in se.query(Sub).order_by(Sub.id)[1:3]:
#    print(u.title)
##把这个查询命名为query:
#query = se.query(Sub).filter(Sub.title != None).order_by(Sub.id)
##然后就可以和pd交互：注意要用statement，加上数据库引擎sq作为第二参数
#df = pd.read_sql(query.statement, sq) #sq亦可以用se.bind代替
#
##复杂的查询可以参考下面的，未测试：
#c = query.statement.compile(query.session.bind)
#df = pandas.read_sql(c.string, query.session.bind, params=c.params)

class DB(object):
    def __init__(self, path, text=None, timeout=0):
#        encpath = path
#        if isinstance(encpath, str):
#            encpath = path.encode("utf-8")
#        self.engine = create_engine("""sqlite:///%s""" % path, echo=True)
        self.engine = create_engine("""sqlite:///%s""" % path, echo=False)
        Session = sessionmaker(bind = self.engine) #就是session对象
        self.se = Session() #就是session对象
        self._db = self.se #就是session对象
#        self._db = sqlite.connect(encpath, timeout=timeout)
        if text:
            self._db.text_factory = text
        self._path = path
        self.echo = os.environ.get("DBECHO") 
#        self.echo = "2"
        self.mod = False

    def execute(self, sql, *a, **ka):
        s = sql.strip().lower()
        # mark modified?
        for stmt in "insert", "update", "delete":
            if s.startswith(stmt):
                self.mod = True
        t = time.time()
        if ka:
            res = self._db.execute(sql, ka)
        else:
            # execute("...where id = ?", 5)
#            print(sql, a)
            res = self._db.execute(sql, a)
        if self.echo:
            #print a, ka
            print(sql, "%0.3fms" % ((time.time() - t)*1000))
            if self.echo == "2":
                print(a, ka)
        return res

    def executemany(self, sql, l):
        self.mod = True
        t = time.time()
        self._db.executemany(sql, l)
        if self.echo:
            print(sql, "%0.3fms" % ((time.time() - t)*1000))
            if self.echo == "2":
                print(l)

    def commit(self):
        t = time.time()
        self._db.commit()
        if self.echo:
            print("commit %0.3fms" % ((time.time() - t)*1000))

    def executescript(self, sql):
        self.mod = True
        if self.echo:
            print(sql)
        self._db.executescript(sql)

    def rollback(self):
        self._db.rollback()

    # def scalar(self, base):
        # res = self.execute(*a, **kw).fetchone()
        # if res:
        #     return res[0]
        # return None

    def getParentId(self, base, onlineId):
        """获取parentId"""
        query = self.se.query(base.parentId).filter(base.onlineId == onlineId)
        res = query.scalar()
        return res

    def updateParentId(self, base, onlineId, parentId):
        """更新parentId"""
        self.se.query(base).filter(base.onlineId == onlineId).update({"parentId": parentId})
        self.se.commit()

    def all(self, *a, **kw):
        return self.execute(*a, **kw).fetchall()

    def first(self, *a, **kw):
        c = self.execute(*a, **kw)
        res = c.fetchone()
        c.close()
        return res

    def lis(self, base):
        """返回title列表"""
        s = select([base.title])
        res = s.execute().fetchall()
        df = pd.DataFrame(res, columns=['title'])
        return list(df['title']) #将这一栏转为列表

#def lis(base):
#    """返回title列表"""
#    s = select([base.title])
#    res = s.execute().fetchall()
#    df =pd.DataFrame(res, columns=['title'])
#    return list(df['title']) #将这一栏转为列表
#
#def dic(base):
#    """返回字典，k,v = onlineId,title"""
#    s = select([base.onlineId, base.title])
#    res = s.execute().fetchall()
#    d = {}
#    for i in res:
#        d[i[0]] = i[1]
#    return d
        
    def dic(self, base, parentId=None):
        """返回字典，k,v = onlineId,title"""
#        s = select([base.onlineId, base.title])
        query = self.se.query(base).order_by(base.id)
#        s = select([tasks.c.title, tasks.c.onlineId], tasks.c.title != '云手') 
        if parentId:
            query = query.filter(base.parentId == parentId)
#            s = select([base.onlineId, base.title], base.parentId==parentId)        
        res = query.all()
        d = {}
        for i in res:
            d[i.onlineId] = i.title
        return d

#def dic(base, parentId=None):
#    query = se.query(base).order_by(base.id)
#    if parentId:
#        query = query.filter(base.parentId == parentId)
#    res = query.all()
#    d = {}
#    for i in res:
#        d[i.onlineId] = i.title
#    return d        
#    def list(self, *a, **kw):
#        return [x[0] for x in self.execute(*a, **kw)]
        
    def close(self):
        self._db.close()

    def set_progress_handler(self, *args):
        self._db.set_progress_handler(*args)

    def __enter__(self):
        self._db.execute("begin")
        return self

    def __exit__(self, exc_type, *args):
        self._db.close()

    def totalChanges(self):
        return self._db.total_changes

    def interrupt(self):
        self._db.interrupt()
