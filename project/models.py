# from django.db import models
# import datetime
from datetime import datetime
# from django.contrib.auth.models import User
# from emagic.utils import todayStamp
from sqlalchemy.ext.declarative import declarative_base  # 创建基类用
from sqlalchemy import *  # 可用来将数据库映射过来

Base = declarative_base()  # 基类


###############################################
########         各类数据表        ############
###############################################
class Unit(Base):
    __tablename__ = 'Unit'
    id = Column(Integer, primary_key=True)
    onlineId = Column(Text)
    title = Column(Text)
    createdAt = Column(DateTime, default=datetime.now)
    updatedAt = Column(DateTime, default=datetime.now)


class Category(Base):
    __tablename__ = 'Category'
    id = Column(Integer, primary_key=True)
    onlineId = Column(Text)
    title = Column(Text)
    createdAt = Column(Text)
    updatedAt = Column(Text)


class List(Base):
    __tablename__ = 'List'
    id = Column(Integer, primary_key=True)
    onlineId = Column(Text)
    title = Column(Text)
    unitId = Column(Text, ForeignKey('Unit.onlineId'), default="1450386127")
    listType = Column(Text, default="LIST")
    createdAt = Column(DateTime, default=datetime.now)
    updatedAt = Column(DateTime, default=datetime.now)


class Task(Base):
    __tablename__ = 'Task'
    id = Column(Integer, primary_key=True)
    onlineId = Column(Text)
    title = Column(Text)
    createdAt = Column(DateTime, default=datetime.now)
    updatedAt = Column(DateTime, default=datetime.now)
    parentId = Column(Text, ForeignKey('List.onlineId'))
    dueDate = Column(Text)
    starred = Column(Boolean)
    completed = Column(Boolean)
    completedAt = Column(Text)
    #    usageTime = Column(Time)
    #    workLoad = Column(Float)
    #    lastPos = Column(Integer)
    unitId = Column(Text, ForeignKey('Unit.onlineId'))
    categoryId = Column(Integer, ForeignKey('Category.id'))  # 分类, 相当于sp在书架外多一个学科分类


class Subtask(Base):
    __tablename__ = 'Subtask'
    id = Column(Integer, primary_key=True)
    onlineId = Column(Text)
    title = Column(String)
    createdAt = Column(DateTime, default=datetime.now)
    updatedAt = Column(DateTime, default=datetime.now)
    parentId = Column(Text, ForeignKey('Task.onlineId'))
    completed = Column(Boolean)
    completedAt = Column(Text)


# usageTime = Column(Time)
#    workLoad = Column(Float)
#    lastPos = Column(Integer)
#    unit = Column(Integer)   

class Record(Base):
    __tablename__ = 'Record'
    id = Column(Integer, primary_key=True)
    onlineId = Column(Text)
    title = Column(Text)
    createdAt = Column(DateTime, default=datetime.now)
    updatedAt = Column(DateTime, default=datetime.now)
    parentId = Column(Text, ForeignKey('Task.onlineId'))
    usageTime = Column(Integer)
    workLoad = Column(Integer)
    minCount = Column(Integer)
    maxCount = Column(Integer)


# unit = Column(Integer, ForeignKey(Unit.id)) #单位由任务决定

class Note(Base):
    __tablename__ = 'Note'
    id = Column(Integer, primary_key=True)
    onlineId = Column(Text)
    content = Column(Text)
    createdAt = Column(Text)
    updatedAt = Column(Text)
    parentId = Column(Text)

# class Province(models.Model):
#    
##    id = models.IntegerField(primary_key=True)
#    name = models.CharField(max_length=64, null=True) #省名
#    class Meta:
#        verbose_name_plural = "省"
#        
#    def __str__(self):
#        return self.name
#        
# class City(models.Model):
#    
##    id = models.IntegerField(primary_key=True)
#    province = models.ForeignKey(Province, default=1, related_name="CITY_PROV") #省
#    name = models.CharField(max_length=64, null=True) #市名
##    vname = models.CharField(max_length=64, null=True) #市名 #临时测试用
#    class Meta:
#        verbose_name_plural = "市/区"
#        
#    def __str__(self):
#        return self.name
#        
# class County(models.Model):
#    
##    id = models.IntegerField(primary_key=True)
#    province = models.ForeignKey(Province, default=1, related_name="COUNTY_PROV") #省
#    city = models.ForeignKey(City, default=1, related_name="COUNTY_CITY") #市
#    name = models.CharField(max_length=64, null=True) #县名
#
#    class Meta:
#        verbose_name_plural = "区/县"
#        
#    def __str__(self):
#        return self.name
#
# class District(models.Model):
#    '''代替原来的省市县,可实现三级联动'''
#    #数字取自discuz x3,district表
#    name = models.CharField(max_length=64, null=True) #区域名
#    level = models.SmallIntegerField(default=0)
#    upid = models.IntegerField(default=0)
#    usetype = models.SmallIntegerField(default=0)
#    displayorder = models.SmallIntegerField(default=0)
#    
#    class Meta:
#        verbose_name_plural = "地区"
#        
#    def __str__(self):
#        return self.name
#        
# class School(models.Model):
#    
##    id = models.IntegerField(primary_key=True)
#    name = models.CharField(max_length=64, null=True) #校名
#    province = models.ForeignKey(Province, related_name="SCH_PROV") #省
#    city = models.ForeignKey(City, related_name="SCH_CITY") #市
##    county = models.ForeignKey(County) #县
#
#    class Meta:
#        verbose_name_plural = "学校"
#        
#    def __str__(self):
#        return self.name
#      
# class Class(models.Model):
#    
##    id = models.IntegerField(primary_key=True)
#    name = models.CharField(max_length=64, null=True) #班级名
#    school = models.ForeignKey(School, related_name="CLS_SCH") #学校
#    
#    class Meta:
#        verbose_name_plural = "班级"
#        
#    def __str__(self):
#        return self.name
#
# class Grade(models.Model):
#    '''年级仅用来区分课程,并不参与分班级'''
##    id = models.IntegerField(primary_key=True)
#    name = models.CharField(max_length=64, null=True) #年级名/级别
#    count = models.IntegerField(default=1) #该年级/级别下的课程数
#    
#    class Meta:
#        verbose_name_plural = "年级"
#        
#    def __str__(self):
#        return self.name
#
# class Subject(models.Model):
#    '''科目/学科'''
##    id = models.IntegerField(primary_key=True)
#    name = models.CharField(max_length=64, null=True) #科目/分类名
#    count = models.IntegerField(default=1) #该科目/分类下的课程数
#    level = models.SmallIntegerField(default=0)
#    upid = models.IntegerField(default=0)
#    usetype = models.SmallIntegerField(default=0) #控制是否显示,即是否禁用
#    displayorder = models.SmallIntegerField(default=0)
#    
#    class Meta:
#        verbose_name_plural = "科目"
#        
#    def __str__(self):
#        return self.name
#
##class Unit(models.Model):
##    '''单元'''
##    id = models.IntegerField(primary_key=True)
##    name = models.CharField(max_length=64, null=True) #科目名
##    
##    class Meta:
##        verbose_name_plural = "科目"
##        
##    def __str__(self):
##        return self.name
#
################################################
#########           课程相关        ############
################################################
#
##class Col(models.Model):
##    '''课程配置表：记录课程配置'''
##    '''此表已基本弃用'''
##    id = models.IntegerField(primary_key=True)
##    crt = models.IntegerField(default=1)
##    mod = models.IntegerField(default=1)
##    scm = models.IntegerField(default=1)
##    ver = models.IntegerField(default=1)
##    dty = models.IntegerField(default=1)
##    usn = models.IntegerField(default=1)
##    ls = models.IntegerField(default=1)
##    conf = models.TextField(editable=True)
##    model = models.TextField(editable=True)
##    decks = models.TextField(editable=True)
##    dconf = models.TextField(editable=True)
##    tags = models.TextField(editable=True)
##
##    class Meta:
##        verbose_name_plural = "Col"
##        
##    def __str__(self):
##        return self.tags
#        
#
##class Notes(models.Model):
##    '''学习内容表：记录课程内容'''
##    '''此表已基本弃用'''
##    id = models.IntegerField(primary_key=True)
##    guid = models.TextField(editable=True)
##    mid = models.IntegerField(default=1)
##    mod = models.IntegerField(default=1)
##    usn = models.IntegerField(default=1)
##    tags = models.TextField(editable=True)
##    flds = models.TextField(editable=True)
##    sfld = models.IntegerField(default=1)
##    csum = models.IntegerField(default=1)
##    flags = models.IntegerField(default=1)
##    data = models.TextField(editable=False)
##
##    class Meta:
##        verbose_name_plural = "Notes"
##        
##    def __str__(self):
##        return self.id
#        
# class Courses(models.Model):
#    '''课程表：记录课程列表'''
##    id = models.IntegerField(primary_key=True)
#    guid = models.TextField(editable=True)
#    title = models.TextField(editable=True)
#    type = models.IntegerField(default=1)
#    path = models.TextField(editable=True) #似无必要
#    created = models.DateTimeField(default=datetime.datetime.now)
#    desc = models.TextField(editable=True, default="") #描述
#    author = models.TextField(editable=True, default="", null=True) #作者,后期用
#    disable = models.BooleanField(default=False, editable=True) #禁用,可临时关闭课程,而不必删除
#    allPages = models.IntegerField(default=1) #总页数
#    grade = models.ForeignKey(Grade, default=1, related_name="CRS_GRD") #年级
#    subject = models.ForeignKey(Subject, default=1, related_name="CRS_SUB") #科目
#    price = models.IntegerField(default=30) #价格
#    isFree =  models.BooleanField(default=False, editable=True) #是否免费
#    like = models.IntegerField(default=30) #投票
##    image_path = models.CharField(max_length=80, null=True, editable=True)
#    image_path = models.ImageField(upload_to='images', null=True, editable=True) #图片
#    conf = models.TextField(editable=True, null=True) #记录子类信息,以后或可包括子集
#    audio_type = models.IntegerField(default=0) #自动语音类型
#    
#    class Meta:
#        verbose_name_plural = "课程"
#        
#    def __str__(self):
#        return self.title
#        
# class Items(models.Model):
#    '''学习内容表：记录课程内容'''
#    '''Notes表为公用'''
##    id = models.IntegerField(primary_key=True)
#    course = models.ForeignKey(Courses, default=1, related_name="ITEM_CRS") 
##    courseId = models.IntegerField(default=1)
#    type = models.IntegerField(default=0)
#    disable = models.BooleanField(default=None)
#    subType = models.IntegerField(default=1)
#    parentId = models.IntegerField(default=1)
#    name = models.TextField(editable=True)
#    question = models.TextField(editable=True)
#    answer = models.TextField(editable=True)
#    command = models.TextField(editable=True)
#    lessonTitle = models.TextField(editable=True) #todo,可以不用?
#    chapterTitle = models.TextField(editable=True)
#    isFree =  models.BooleanField(default=False, editable=True) #是否为免费页面
#    mediaId = models.IntegerField(default=1, editable=True) #媒体Id,原课程的item_id
#    keyword = models.TextField(editable=True, null=True) #关键词,即单词
#
#    class Meta:
#        verbose_name_plural = "练习"
#        
#    def __str__(self):
#        return self.name
#
# class Cards(models.Model):
#    '''卡片表，记录复习数据'''
#    '''需增加用户字段，类似论坛的帖子，每一个页面的复习数据需要记录'''
#    '''但同一课程下只更新固定页面的数据'''
##    id = models.IntegerField(primary_key=True)
#    #todo150722,改nid为外键,ord为外键
#    item = models.ForeignKey(Items, default=1, related_name="CARD_ITEM") #页面内容,取代nid
#    user = models.ForeignKey(User, default=1, related_name="CARD_USER") #会员号,取代ord
#    course = models.ForeignKey(Courses, default=1, related_name="CARD_CRS") #课程,取代did
#    
#    nid = models.IntegerField(default=1) #此值暂且保留
#    did = models.IntegerField(default=1) #此值暂且保留
#    ord = models.IntegerField(default=0) #此值暂且保留
#    mod = models.IntegerField(default=1) #todo,这里是否改为Forienkey(改后需要改统计之类的代码)
#    usn = models.IntegerField(default=0)
#    type = models.IntegerField(default=0)
#    queue = models.IntegerField(default=0) #队列,如,1为巩固练习,0为未学习
#    due = models.IntegerField(default=0) 
#    ivl = models.IntegerField(default=0) #间隔
#    grade = models.IntegerField(default=0) #用户评分
#    factor = models.IntegerField(default=0)
#    reps = models.IntegerField(default=0)
#    lapses = models.IntegerField(default=0)
#    left = models.IntegerField(default=0)
#    odue = models.IntegerField(default=0)
#    odid = models.IntegerField(default=0)
#    flags = models.IntegerField(default=0)
#    data = models.TextField(editable=False, null=True)
#
#    class Meta:
#        verbose_name_plural = "进度"
#        
#    def __str__(self):
#        return self.id
#   
# class Course_set(models.Model):
#    '''课程设置:记录哪些用户学了哪些课程,具体的设置情况'''
#    '''后期可考虑增加金额字段,可统计消费情况'''
#    user = models.ForeignKey(User, related_name="SET_USER")
#    course = models.ForeignKey(Courses, related_name="SET_CRS")
#    buyed = models.BooleanField(default=False) #是否已购买(必须支付)
#    daily = models.IntegerField(default=30) #每组学习新材料数
#    fi = models.IntegerField(default=10) #遗忘指数
#    todayDone = models.IntegerField(default=0) #今日学习
#    allDone = models.IntegerField(default=0) #总共学习
#    crt = models.IntegerField(default=0) #课程注册日期
#    mod = models.IntegerField(default=0) #课程数据更新日期,与上一个均取值todayStamp,当日第一次学习时更新
#    #注:mod值用于查看todayDone值是否要从0开始计算(还是直接累加)
#    usn = models.IntegerField(default=1) #同步用
#    conf = models.TextField(editable=True, null=True)
#    dconf = models.TextField(editable=True, null=True)
#    tags = models.TextField(editable=True, default="[]")
#
####用户档案
# class UserProfile(models.Model):
#    # 这一句是必须的，链接UserProfile到Django的用户模型
#    user = models.OneToOneField(User, related_name="PROFILE")
##    user = models.ForeignKey(User, unique=True)
##    user = models.ForeignKey(User)
#    # 我们想要增加的额外字段
##    website = models.URLField(null=True)
#    realName = models.CharField(max_length=64, null=True) #真实姓名
#    sex = models.CharField('性别', choices = SEX_CHOICES, max_length = 1, default=0)
#    mobilePhone = models.IntegerField(null=True, default=0) #手机
#    phone = models.IntegerField(null=True, default=0) #座机
#    qq = models.IntegerField(null=True, default=0) #qq
##    mail = models.EmailField (null=True) #邮件
#    conf = models.TextField(editable=False, null=True) #配置
#    parentId = models.IntegerField(default=0) #家长账号
#    tutorId = models.IntegerField(default=0) #导师账号
##    classId = models.IntegerField(default=0) #班级编号
##    schoolId = models.IntegerField(default=0) #学校编号
#    school = models.ForeignKey(School, default=1, related_name="PROF_SCH")
#    classes = models.ForeignKey(Class, default=1, related_name="PROF_CLS")
#    subject = models.ForeignKey(Subject, default=1, related_name="PROF_SUB") #科目,当用户为老师时,指定他的任课课程,学生用户无效
#    isParent = models.BooleanField(default=False) #是否家长
#    isTutor = models.BooleanField(default=False) #是否导师
#    avatar = models.ImageField(upload_to='avatar', null=True) #头像
##    avatar = AvatarField(upload_to='avatar', width=100, height=100) #头像
#    crt =  models.IntegerField(default=todayStamp(), editable=True) #账号创建日期,用此值来做全局的crt,due根据此值来转换
#    usn =  models.IntegerField(default=-1) #同步标记
#    
#    class Meta:
#        verbose_name_plural = "用户档案"
#        
#    # 重写__str__方法，让它在被调用时显示用户名
#    def __str__(self):
#        return self.user.username
####测试或辅助用,用来存语音库的md5编码,可反向推测出以itemid命名的文件的词汇  
# class AudioBank(models.Model):
#    md5 = models.CharField (max_length=25, default='', null=True)#md5
#    data = models.CharField (max_length=25, default='', null=True)#放单词或路径
#    type = models.IntegerField(default=1)#类型:1.美音;2.英音;3.朗文
#    
####订单及订单内容
# class Order(models.Model):
#    user = models.ForeignKey(User, related_name="ORD_USER")
#    order_sn = models.CharField (max_length=25, default='free', null=True)
#    order_status = models.CharField (max_length=50, default='INIT', null=True)
#    pay_status = models.CharField (max_length=50, default='INIT', null=True)
#    add_time = models.DateTimeField (default=datetime.datetime(1900,1,1))
#    pay_time = models.DateTimeField (default=datetime.datetime(1900,1,1))
#    order_amount = models.IntegerField(default=1)
#    quantity = models.IntegerField(default=1)
#
#    class Meta:
#        verbose_name_plural = "订单管理"
#        
# class LineItem(models.Model):
#    product = models.ForeignKey(Courses, related_name="LINE_CRS")
#    order = models.ForeignKey(Order, related_name="LINE_ORD")
#    unit_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
#    quantity = models.IntegerField(default=1)
#
# def add_product(cart, product):
#    cart['total_price'] += float(product.price)
#    cart['total_quantity'] += 1
#    for item in cart['items']:
#        if item['fields']['id'] == product.id:
#            item['fields']["quantity"] += 1
#            return
#    cart['items'].append(
#        {"fields":
#        {"id":product.id, "price": float(product.price), "title": product.title,"quantity": 1}
#        }
#        )
#        
# def minus_product(cart, product):
#    cart['total_price'] -= float(product.price)
#    cart['total_quantity'] -= 1
#    for item in cart['items']:
#        if item['fields']['id'] == product.id:
#            item['fields']["quantity"] -= 1
#            if item['fields']["quantity"] <= 0:
#                index = cart['items'].index(item)
#                cart['items'].pop(index)
#            return
#
# class Cart(object):
#    def __init__(self, *args, **kwargs):
#        self.items = []
#        self.total_price = 0
#        
#    def add_product(self, product):
#        self.total_price += product.price
#        for item in self.items:
#            if item.product.id == product.id:
#                item.quantity += 1
#                return
#                
#        self.items.append(LineItem(product=product,unit_price=product.price,quantity=1))
