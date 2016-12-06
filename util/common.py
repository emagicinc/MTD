 #!/usr/bin/env python
import sip
sip.setapi('QVariant', 2)
from PyQt4 import QtCore, QtGui, QtXml
#import math
#import hashlib
#from project.dictSet import DictSet
import urllib.request, urllib.parse, urllib.error
import codecs
import sqlite3
import chardet
import os
import re
import zlib
#import struct
import shutil
import random
import time
#用于遍历文件,以供删除
import glob
import json
from collections import OrderedDict
import traceback
from util import SMMessageBox
from bs4 import BeautifulSoup
import Preferences as Prefs

def getKeyTxt(key):
    '''将过滤词用空格断开,以获得模糊匹配'''
    keyTxt = ""
    if key != "":
        keyList = key.split(" ")
        keyTxt = "%%".join(keyList)    
        return keyTxt

def traceBack():
    """
    返回出错信息;
    受debugMode参数控制;
    """
    try: 
        return traceback.format_exc()
        traceback.print_exc()
    except:  
        return ''   
            
################################################
###                文件操作相关              ### 
################################################  
def copyTree(src, dst, symlinks=False):
    """
    复制文件夹;
    """
    names = os.listdir(src)
    if not os.path.isdir(dst):
        os.makedirs(dst)            
    errors = []
    for name in names:
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                shutil.copytree(srcname, dstname, symlinks)
            else:
                if os.path.isdir(dstname):
                    os.rmdir(dstname)
                elif os.path.isfile(dstname):
                    os.remove(dstname)
                shutil.copy2(srcname, dstname)
        except (IOError, os.error) as why:
            errors.append((srcname, dstname, str(why)))
        except OSError as err:
            errors.extend(err.args[0])
    try:
        shutil.copystat(src, dst)
    except WindowsError:
        pass
    except OSError as why:
        errors.extend((src, dst, str(why)))

def copyFile(src, dst):
    """
    复制文件;
    以后可以直接传参数进来,比如说是否覆盖;
    """
    src = src.replace("/", "\\")
    dst = dst.replace("/", "\\")
    shutil.copy2(src,dst)
    
def outputStream(mw, courseFile, content, type=None, outputCodec=None):
    """
    输出文件,格式为:文件名,内容,类型(增补,全新),输出编码
    """
    outFile = QtCore.QFile(courseFile)
    if not outputCodec:
        outputCodec  =  "UTF-8"
    if type == "append":#如果模式为append
        if not outFile.open(QtCore.QFile.Append|QtCore.QFile.Text):
            QtGui.QMessageBox.warning(mw, "文件写入错误",
                    "无法写入文件 %s:\n%s" % (courseFile, outFile.errorString()))
            return
    elif type == "append2":#如果模式为append
        if not outFile.open(QtCore.QFile.Append|QtCore.QFile.Text):
            QtGui.QMessageBox.warning(mw, "文件写入错误",
                    "无法写入文件 %s:\n%s" % (courseFile, outFile.errorString()))
            return                
    else:
        if not outFile.open(QtCore.QFile.WriteOnly|QtCore.QFile.Text):
            QtGui.QMessageBox.warning(mw, "文件写入错误",
                    "无法写入文件 %s:\n%s" % (courseFile, outFile.errorString()))
            return             
    outf = QtCore.QTextStream(outFile)
    #self.out.setDevice(outFile)
    outf.setCodec(outputCodec)#设置编码
    if type == "append":#如果是追加模式,就先写一行时间        
        outf << "@写入时间: " << QtCore.QDate.currentDate().toString("yyyy-MM-dd") << " " << QtCore.QTime.currentTime().toString("hh:mm:ss") << '\n'
    outf << content
    outFile.close()
    return True

def getSelTxt(obj):
    '''返回TE控件中的选中文本'''
    data = obj.createMimeDataFromSelection()
    txt = data.text().replace("[]", "")
#    cursor = obj.textCursor()
#    txt = cursor.selectedText()
    txt = txt.strip(" ")
    txt = txt.strip("　")
    return txt

def outTxt(mw, fileName, content, type=None, outputCodec=None):
    """
    输出文件,格式为:文件名,内容,类型(增补,全新),输出编码
    """
    outFile = QtCore.QFile(fileName)
    if not outputCodec:
        outputCodec  =  "UTF-8"
    if type == "append":#如果模式为append
        if not outFile.open(QtCore.QFile.Append|QtCore.QFile.Text):
            QtGui.QMessageBox.warning(mw, "文件写入错误",
                    "无法写入文件 %s:\n%s" % (fileName, outFile.errorString()))
            return
    elif type == "append2":#如果模式为append
        if not outFile.open(QtCore.QFile.Append|QtCore.QFile.Text):
            QtGui.QMessageBox.warning(mw, "文件写入错误",
                    "无法写入文件 %s:\n%s" % (fileName, outFile.errorString()))
            return                
    else:
        if not outFile.open(QtCore.QFile.WriteOnly|QtCore.QFile.Text):
            QtGui.QMessageBox.warning(mw, "文件写入错误",
                    "无法写入文件 %s:\n%s" % (fileName, outFile.errorString()))
            return             
    outf = QtCore.QTextStream(outFile)
    #self.out.setDevice(outFile)
    outf.setCodec(outputCodec)#设置编码
    if type == "append":#如果是追加模式,就先写一行时间        
        outf << "@写入时间: " << QtCore.QDate.currentDate().toString("yyyy-MM-dd") << " " << QtCore.QTime.currentTime().toString("hh:mm:ss") << '\n'
    outf << content
    outFile.close()
    return True    

          
def readFile(mw, fileName, type=None, codec=None):
    '''读取文件,可返回整体或仅仅是文件头'''
    file = QtCore.QFile(fileName)
    if not file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
        pass
#        QtGui.QMessageBox.warning(mw, "SuperMemo课程编辑器",
#                "无法读取文件 %s:\n%s." % (fileName, file.errorString()))
#        return
    ####检测输入编码#####
    inputCodec = codec
    if not codec:
        f = codecs.open(fileName, "rb")
        content = f.read(1*1024)
        detect = chardet.detect(content)
        f.close()            
        inputCodec = detect.get("encoding")
        inputCodec = correctCodec(inputCodec)
    inf = QtCore.QTextStream(file)
    inf.setCodec(inputCodec)
    if not type:
        return inf.readLine()
    else:
        return inf.readAll()
    file.close()

def correctCodec(codec):
    '''校验编码'''
    if codec in ("ascii",  "IBM866", "windows-1252"):
        return "GBK"
    elif codec in ("EUC-jp", "other", "ISO-8859-2") :
        return "UTF-8"
    elif codec in ("gb2312", "GB2312", "GB18030") :
        return "GB2312"
    else:
        return "UTF-8"

def strippedPath(fullFileName):#包含文件名
    return QtCore.QFileInfo(fullFileName).absoluteFilePath()
  
def getFileInfo(type, fileName):
    """
    获取文件名信息;
    如果文件名为空,则取当前文件名
    type:suffix(扩展名),baseName(不带扩展名),fullName(完整文件名),basePath(仅路径),fullPath(完整路径,带文件名)
    此程序可取代原来的stripPath系列程序
    """
#    if not fileName:
#       fileName = mw.curFile
    if type == "suffix":
        return QtCore.QFileInfo(fileName).suffix()
    elif type == "baseName":
        return QtCore.QFileInfo(fileName).completeBaseName()
    elif type == "fullName":
        return QtCore.QFileInfo(fileName).fileName()        
    elif type == "basePath":
        return QtCore.QFileInfo(fileName).path()          
    elif type == "fullPath":
        return QtCore.QFileInfo(fileName).absoluteFilePath()          
    elif type == "url":
        return  QtCore.QUrl.fromLocalFile(QtCore.QFileInfo(fileName).absoluteFilePath())

def toList(value):
    '''
    Module function to convert a value to a list.        
    @param value value to be converted
    @return converted data
    '''
    if value is None:
        return []
    elif not isinstance(value, list):
        return [value]
    else:
        return value
        
################################################
###                 控件相关                 ### 
################################################  

def getOpenFileName(title, object=None, type=None, parent=None, fileType=None):
    """
    打开文件对话框,获取文件名;
    parent用作返回活动窗口;
    type为控件的类别,如combo或lineedit;
    """
    text = ""
    if type == "combo":
        text = object.currentText()
    elif type == "LE":
        text = object.text()
    if not fileType:
        fileType = "文本文件 (*.txt);;所有文件 (*)"
    options = QtGui.QFileDialog.Options()
    fileName = QtGui.QFileDialog.getOpenFileName(parent,
            title, text,
            fileType, options)
    if fileName:
        if type == "combo":            
            object.setEditText(fileName)
        elif type == "LE":
            object.setText(fileName)
        elif type == "file":
            return fileName
 
def getExistingDir(title, object, type, parent):
    """
    打开文件对话框,获取文件夹名;
    parent用作返回活动窗口;
    type为控件的类别,如combo或lineedit;
    """
    if type == "combo":
        text = object.currentText()
    elif type == "LE":
        text = object.text()
    options = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly
    directory = QtGui.QFileDialog.getExistingDirectory(parent,
            title, text, options)
    if directory:
        if type == "combo":            
            object.setEditText(directory)
        elif type == "LE":
            object.setText(directory)
            
def resetCombo(combo, items, isMulti=None, indexItem=None, dataType=None):
    """
    以传入的items(列表)重置组合框值;
    indexItem为str;
    isMulti 若为True,则为多元列表,如模型设置中的题型列表;
    dataType若为int,则为直接设置索引值;若为findData,则使用findData,否则用findText;
    """ 
    combo.clear()
    try:
        if not isMulti:
            for i in items:
                combo.addItem(i)
        else:#二元列表
            for i in items:
                combo.addItem(i[0], i[1]) 
        if indexItem:
            try:
                if dataType == "int":
                    index = int(indexItem)
                elif dataType == "findData":
#                        print("in")
                    index = combo.findData(indexItem)
#                        print(index)
                elif dataType == "findText":
                    index = combo.findText(indexItem)
                if index:
                    combo.setCurrentIndex(index)
                else:
                    combo.setCurrentIndex(0)
            except:
                if not dataType:                        
                    combo.setEditText(indexItem)
                else:
                    combo.setCurrentIndex(0)
        else:
            combo.setCurrentIndex(0)
    except:
        pass
#
#def setItem(mw, obj, elem, parent, id, type, name, TARGET=None):
#    '''obj是来源控件，一是主窗口的章节树（由xmlTree控制），二是课程列表编辑器'''
#    '''设置各章节树的item,用于parseFolderElement'''
#    '''TARGET仅用于课程列表编辑器，表示处理右侧的目标章节树'''
#    item = obj.createItem(elem, parent, TARGET)
#    item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
#    start = 0
#    if not TARGET:
#        start = 1
#        if id in mw.posList:#posList用于检测重载时是否勾选Item
#            item.setCheckState(start - 1, QtCore.Qt.Checked)
#        else:
#            item.setCheckState(start - 1, QtCore.Qt.Unchecked)
#    item.setText(start, name)
#    item.setData(start, 32, [id, type])
#    item.setText(start + 1, id)
#    #决定是否展开
#    folded = (type == 'pres')#如果属性是章节
#    self.tree.setItemExpanded(item, folded)#打开
#    if type == "pres":
#        item.setIcon(0, self.mw.folderIcon)
#    else:
#        item.setIcon(0, self.mw.bookmarkIcon)
#    return item
        
################################################
###               课程/数据库相关            ### 
################################################  
def connectDb(mw, db=None):
    '''连接数据库,141021新增'''
    '''若存在数据库连接,则先关闭'''
    if mw.cxn:
        mw.cxn.close()
    if not db:
        db = Prefs.getCourse("db")
        mw.curDb = "system"
#        else:
#            '''#临时#,后期应改为可设置'''
#            db = "./user.dat"
#            mw.curDb = "user"
#    print(db)
    if QtCore.QFile.exists(db):
        mw.cxn = sqlite3.connect(db, isolation_level="DEFERRED")
#        mw.cxn = sqlite3.connect(db, isolation_level="DEFERRED")#IMMEDIATE,EXCLUSIVE
        mw.cxn.execute('PRAGMA page_size = %s' % '1024') # 1024, 2048, 4096, 8192, 16384, 32768
        mw.cxn.execute('PRAGMA synchronous = %s' % 'OFF') # FULL, OF        
        mw.cur = mw.cxn.cursor()
        return True
        
def closeDb(mw):
    '''关闭数据库'''
    if mw.cxn:
        mw.cxn.close()
        mw.cxn = None
        mw.cur = None

def execSql(mw, sql, type, db=None):
    '''执行sql语句，注意与其它程序不同！'''
    '''此程序的执行，必须先调用self.connectDb'''
    '''注意，本文档中大部分用到execSql的地方都需要修改！'''
    #todo, 未考虑使用插件时,数据库的切换问题,似应加条件到connectDb中
    if not mw.cxn:
        connectDb(db)
    if type not in ["blob", "updateAll"]:
        mw.cur.execute(sql)#执行查询,blob和updateAll时不用执行查询
    if type == "one":
        return mw.cur.fetchone()
    elif type == "all":
        return mw.cur.fetchall()
    elif type == "update" or type == "del":#此处可直接返回一个值，比如：return  cxn.commit()
        try:
            mw.cxn.commit()
        except:
            return True #返回错误信号,下同
    elif type == "updateAll":#以列表方式传入sql
        for i in sql:
            if i is not None:
                mw.cxn.execute(i)
        try:
            mw.cxn.commit()
        except:
            return True
    elif type == "blob":
        with open('blob.dat', 'rb') as f:
            mw.cur.execute("""UPDATE Courses SET OptRec=(?) WHERE Id='%s'""" % sql, (sqlite3.Binary(f.read()), ))
        try:
            mw.cxn.commit()
        except:
            return True

#def execSql(sql, type, db=None):
#    '''检索数据库,此处可加消息框'''
#    if not db:
#        db = Prefs.getCourse("db")
#    if QtCore.QFile.exists(db):
#        cxn = sqlite3.connect(db, isolation_level=None)
#        cxn.execute('PRAGMA page_size = %s' % '1024') # 1024, 2048, 4096, 8192, 16384, 32768
#        cxn.execute('PRAGMA synchronous = %s' % 'OFF') # FULL, OFF
#        cur = cxn.cursor()
#        if type not in ["blob", "updateAll"]:
#            cur.execute(sql)#执行查询,blob和updateAll时不用执行查询
#        if type == "one":
#            return cur.fetchone()
#        elif type == "all":
#            return cur.fetchall()
#        elif type == "update" or type == "del":
#            cxn.commit()
#        elif type == "updateAll":#以列表方式传入sql
#            for i in sql:
#                cxn.execute(i)
#            cxn.commit()
#        elif type == "blob":
##                sBytes = readPic('blobUX.dat')
###                cxn.execute("""UPDATE Courses SET OptRec=(?) WHERE Id='%s'""" % sql, (sqlite3.Binary(sBytes), )) 
##                cxn.execute("UPDATE Courses SET OptRec=(?) WHERE Id=24", (sqlite3.Binary(sBytes), ))
#            with open('blob.dat', 'rb') as f:
#                cur.execute("""UPDATE Courses SET OptRec=(?) WHERE Id='%s'""" % sql, (sqlite3.Binary(f.read()), ))
##                cxn.execute("""UPDATE Courses SET OptRec='%s' WHERE Id=%s""" % (sBytes, sql))
#            try:
#                cxn.commit()
#            except:
#                pass
#        cxn.close()
            
def readPic(fileName):
    '''读图片为bytes'''
    sBytes = ""
    try:
#        sBytes = readFile(None, fileName, True)
        f = open(fileName, "rb")
        sBytes = f.read()
        f.close()
    except:
        pass
    return sBytes

#def getLastId(table):
#    '''获取当前的最大一个rowid'''
#    sqlExp = """SELECT rowid FROM %s""" % table
#    query = queryDB(sqlExp)
#    query.last()
#    rec = query.record()
#    if not rec.value(0):
#        return 0
#    return rec.value(0)

#def queryDB(sqlExp):
#    """数据库查询"""
#    query = QtSql.QSqlQuery()
#    query.exec_(sqlExp)
#    return query
    
def getId(id):
    '''返回页面ID'''
    id = "00000" + str(id)
    id = id[-5:]
    return id

def setItemId(mw, courseId=None):
    '''设置itemId'''
    if not courseId:
        courseId = Prefs.getCourse("courseId")
    mw.itemId = 1
    sqlExp = """SELECT PageNum FROM Items WHERE courseId='%s' ORDER BY rowid desc""" % courseId
    result = execSql(mw, sqlExp, "one")
    if result:
        mw.itemId = result[0] + 1 #自增1
#            
#    sqlExp = """select PageNum from Items WHERE courseId='%s'""" % courseId
#    result = execSql(mw, sqlExp, "all")
#    if result:
#        try:
#            mw.itemId = resultToId(result)
#        except:
#            mw.itemId = 1  
                    
def getImgFile(id, suffix, coursePath=None):
    """
    利用传来的id返回图片文件;
    若无coursePath,则使用默认路径;
    传来的coursePath需带有override;后期可以自动判断一下;
    """
    itemId = getId(id)
    if not coursePath:
        coursePath = Prefs.getCourse("coursePath")
#        courseName = Prefs.getCourse("courseName")
        mediaPath = """%s/override/media""" % getFileInfo("fullPath", coursePath)
#        mediaPath = """%s/%s/override/media""" % (getFileInfo("fullPath", coursePath), courseName)
    imgFile = """%s/%s%s.png""" % (mediaPath, itemId, suffix)
    return imgFile
    
def getMediaFile(mw, suffix, ext, coursePath=None, newId=None):
    """
    根据mw.ui.modeBtn2是否选中来判断ID;
    若无coursePath,则使用默认路径;
    传来的coursePath需带有override;后期可以自动判断一下;
    """
    id = mw.itemId
    if newId:
        #目前只有在使用划词插件的状态下才传入 newId
        #此举可避开modeBtn2的干扰
        id = newId
    else:
        if mw.ui.modeBtn2.isChecked():#表示此时将编辑现有item
            id = mw.editItemId
    itemId = getId(id)
    if not coursePath:
        coursePath = Prefs.getCourse("coursePath")
        mediaPath = """%s/override/media""" % getFileInfo("fullPath", coursePath)
        mediaPath = mediaPath.replace("//", "/")
    mediaFile = """%s/%s%s.%s""" % (mediaPath, itemId, suffix, ext)
    mediaFile = mediaFile.replace("/", "\\")
    return mediaFile

def getItemFile(id, coursePath=None):
    """
    利用传来的id返回item文件;
    若无coursePath,则使用默认路径;
    传来的coursePath需带有override;后期可以自动判断一下;
    """
    itemId = getId(id)
    if not coursePath:
        coursePath = Prefs.getCourse("coursePath")
        coursePath = getFileInfo("fullPath", coursePath) + "/override"
    itemFile = """%s/item%s.xml""" % (coursePath, itemId)
    return itemFile

def removeMedia(id, coursePath=None):
    '''根据传来的id查找相应的媒体文件;使用通配符匹配文件 
    若无coursePath,则使用默认路径;
    传来的coursePath需带有override;后期可以自动判断一下;'''
    itemId = getId(id)
    if not coursePath:
       coursePath = Prefs.getCourse("coursePath")
       coursePath = getFileInfo("fullPath", coursePath) + "/override"
    mediaFile = """%s/media/%s*.*""" % (coursePath, itemId)
    from glob import glob#通配符匹配文件
    file_names = glob(mediaFile)
    for file in file_names:
        os.remove(file)

def makeImageList():
    """
    获取图片后缀列表
    z后缀留着作为机动
    """
    imageNameList = [ i for i in ('m', 'n', 'o', 'p','r', 's', 't', 'u', 'v', 'w', 'x', 'y')]#避开Q和A,从m到y
    return imageNameList
    
def makeAudioList():
    """
    获取音频后缀列表
    
    """
    audioNameList = [ i for i in ('b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l')]#从B到l
    return audioNameList
        
def copyImage(imgList, coursePath):
    """
    背景图复制程序,传进来的是图片编号list;
    """
#    shutil.copy2(".\\template\\images.xml", coursePath + "\\override\\images")
    if not os.path.exists(coursePath + "/override/images"):
        os.mkdir(coursePath + "/override/images")
    copyFile(".\\template\\images.xml", coursePath + "\\override\\images")
    for id in imgList:
        imgId = getId(id)
        img = ".\\template\\" + imgId + "_"
        for i in ["0512", "0720", "1024"]:
            imgFile = """%s\\%s.png""" % (img, i)
            if not os.path.exists(imgFile):#不存在模板文件则复制
                copyFile(img + i + ".png", coursePath + "\\override\\images")
            else:#如果有文件,则直接中止
                break

def copyTemplate(mw, tempNum, tempImg, coursePath):
    """复制模板"""
    tempPath = ".\\template"
    tempDir = """template%s""" % getId(tempNum)
    src = """%s\\%s""" %(tempPath, tempDir)
    targetDir = coursePath.replace("/", "\\") + "\\override\\"
    targetFile = """%s%s\\template.xml""" % (targetDir, tempDir)
    target = """%s%s""" % (targetDir, tempDir)
#    print(QtCore.QFileInfo(tempPath).fileName(), tempDir)
    if int(tempNum) > 12:#如果模板编号大于12,说明启用了自定义模板
#        if not os.path.exists(src):#如果不存在这样的文件夹
##            if QtCore.QFileInfo(tempPath).fileName() == tempDir:#那就检查一下是不是选中了当前文件夹
##                try:
##                    copyTree(tempPath, target)  
##                except:
##                    pass
##                    mw.Log += "复制自定义模板时出错!" + '\n'
#        else:#如果存在这个文件夹
        try:
            if not os.path.exists(targetFile):#不存在模板文件则复制
                copyTree(src, target)  
        except:
            pass
        
    #复制背景图
    imgList = [tempImg]
    try:
        copyImage(imgList, coursePath)
    except:
        pass
#        mw.Log += "复制模板背景图时出错!" + '\n'

def initCourseList(mw, coursePath, courseName):
    """
    初始化课程列表;
    """
    ####公用参数####
#    coursePath = Prefs.getCourse("coursePath")#课程路径
#    courseName = Prefs.getCourse("courseName")#课程名称
    courseListFile = getCourseList(mw, coursePath, courseName)
#    pagesPerChap = int(Prefs.getCourse("pagesPerChap"))
    ##########启用封面#####
#    useCover = settings.value("/cover/useCover")
#    if script:
#        useCover = scriptSettings.value("/script/" + script + "/useCover")
    ####私有参数####
    ##练习标题
#    exTreeMode = courseDict["exTreeMode"]
#    cusExTree = courseDict["cusExTree"]
#    exTreeNumMode = courseDict["exTreeNumMode"]#是否启用练习标题序号,1启用,2不启用
#    exTreeNum = int(courseDict["exTreeNum"])#练习标题序号
#    exTreeV = courseDict["exTreeV"]
    ###章节标题
#    chapTreeMode = courseDict["chapTreeMode"]#章节标题模式
#    cusChapTree = courseDict["cusChapTree"]
#    chapTreeNumMode = courseDict["chapTreeNumMode"]#是否启用练习标题序号,1启用,2不启用
#    chapTreeNum = int(courseDict["chapTreeNum"])#练习标题序号
#    chapMode = str(courseDict["chapMode"])#章节模式,131207新增
#    disableSign = "disabled"
#    if chapMode != "0":#章节模式 
#        disableSign = "enabled"        
#    j = 0
    return courseListFile
    
def getCourseList(mw, coursePath, courseName):
    '''创建课程列表文件,被initCourseList和produceDlg的produce调用'''
    fileHead = ""
#    chapterId = ""
    courseListFile = """%s/override/course.xml""" % coursePath
#    print(getFileInfo("baseName", coursePath))
    if getFileInfo("baseName", coursePath) != courseName:
        courseListFile = """%s/%s/override/course.xml""" % (coursePath, courseName)
        
#    courseListFile = """%s/%s/override/course.xml""" % (coursePath, courseName)
    fileHead =  getCourseHead(courseName)
#    subSet = ""
#    subTypeExercise = ""
#    subTypeChapter = ""
    outFile = QtCore.QFile(courseListFile)
    if not outFile.open(QtCore.QFile.WriteOnly|QtCore.QFile.Text):
        QtGui.QMessageBox.warning(mw, "Codecs",
                "Cannot write file %s:\n%s" % (courseListFile, outFile.errorString()))
        return
    out = QtCore.QTextStream()
    out.setDevice(outFile)
    out.setCodec('utf-8')#设置编码
    out <<  fileHead
    out <<  '</course>' << '\n'
    outFile.close()
    return courseListFile

def getRandom(num):
    """
    生成GUID用的随机数
    """
    randChar = random.sample('abcdef0123456789',num)
    return ''.join(randChar)    

def getOnlineId():
    """
    生成OnlineId用的随机数
    """
    randChar = random.sample('0123456789', 8)
    return ''.join(randChar)
    
    
def getGuid():
    """
    生成课程GUID
    130810已按新版要求增加一段4位的GUID
    """
    guid = """%s-%s-%s-%s-%s""" % (getRandom(8), getRandom(4), getRandom(4), \
            getRandom(4), getRandom(12))
    return guid

def writeCourseList(mw, id, name, type, REPLACE=None, item=None, targetId=None):
    '''向courseList文件追加一条或多条记录'''
    '''type值:pres表示章节,exercise表示页面'''
    '''disableSign先默认为enabled,以后再改'''
    '''chapPos为1表示插入到指定ID前面,2则为插入到后面'''
    '''传入coursePath:制作课程时使用'''
    disableSign = "enabled"
    chapPos = str(Prefs.getCourse("chapPos"))#章节插入位置
    if type == "exercise":
        disableSign = None
        chapPos = str(Prefs.getCourse("itemPos"))#页面插入位置
    coursePath = Prefs.getCourse("coursePath")#课程路径
#    curChap = mw.curChapId #当前选中章节,此时已是章节属性
    courseListFile = """%s/override/course.xml""" % coursePath
#    courseListFile = """%s/%s/override/course.xml""" % (coursePath, courseName)
    contentsDoc = QtXml.QDomDocument()
    xml_file = QtCore.QFile(courseListFile)
    statusOK, errorStr, errorLine, errorColumn = \
            contentsDoc.setContent(xml_file, False)#这里是True的话,就会多出xmlns命名空间的定义
    root = contentsDoc.documentElement()
#    root = contentsDoc.documentElement("element")
    """"下面开始处理元素"""       
    child = root.firstChildElement('element')
#    j = id
    elementN = contentsDoc.createElement("element")
    done = None#140922新增,用于检测输出是否成功
    if not REPLACE:
        #设置Element
#        print(mw.curChapId)
        elementN = setElement(elementN, str(id), type, name, disableSign)
        #获取child
#        childElem = testReader(mw, courseListFile, chapPos, curChap)
        #添加Element
#        childElem.appendChild(elementN)
        done = appendElem(mw, root, elementN, child, chapPos)
    else:
        if REPLACE == "replace":#替换
            replaceElem(root, elementN, child, id, name, type, disableSign, item)
        elif REPLACE == "remove":#删除
            removeElem(mw, root, id, item)
        elif REPLACE == "move":#移动
            moveElem(root, id, item, targetId)#
#    print(chapPos, curChap, name)
    #关闭文件
    xml_file.close()
    #写文件
    file1 = QtCore.QFile(courseListFile)
    if not file1.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
        return
    out1 = QtCore.QTextStream(file1)
    contentsDoc.save(out1, 2)
    file1.close()
    return done
    
def moveElem(root, id, item, targetId):
    '''移动id到指定章节下'''
#    setElement(newChild, str(id), type, name, disableSign)#设置newChild,作为替换用的newChild
#    nodeList = root.elementsByTagName('element')
#    parentId = item.parent().data(0, 32)[0]
#    oldChild = None
#    for i in range(len(nodeList)):
#        node = nodeList.at(i)
#        if node.toElement().attribute("id") == parentId:
#            parent = node
#        if node.toElement().attribute("id") == id:
#            oldChild = node
#    if oldChild:
#        parent.replaceChild(newChild, oldChild)
#    return 
    #要注意,可能会将原章节关系打成扁平化
    nodeList = root.elementsByTagName('element')#获取所有节点
    oldParentId = "0"
    oldParent = root
    newParent = root
    if item.parent():
        oldParentId = item.parent().text(2)
    child = None
    for i in range(len(nodeList)):#遍历节点
        node = nodeList.at(i)
        if node.toElement().attribute("id") == oldParentId:#定位原父节点
            oldParent = node
        if node.toElement().attribute("id") == id:#定位要移动的节点
            child = node
        if node.toElement().attribute("id") == targetId:#定位要接收的节点
            newParent = node            
#    oldParent.removeChild(child)#老节点下删除要移动的节点
    newParent.appendChild(child)#新节点下添加节点
    return    
    
def replaceElem(root, newChild, child, id, name, type, disableSign, item):
    '''替换元素'''#140517注:此方法貌似只能实现根下面的替换!
    #仅用于主窗口中的章节树 140517修改
#    while not child.isNull():
#        childElem = child.toElement()
#        if childElem.attribute('id') == str(id):
#            if childElem.attribute('name') != name:
#                setElement(elem, str(id), type, name, disableSign)
#                parent.replaceChild(elem, child)#替换
#                writeDb(id, name)#更新数据库
#                break
#        child = child.nextSiblingElement()
#    return
#此方法的  setElement有误，会将child给喀嚓掉！  
#    setElement(newChild, str(id), type, name, disableSign)#设置newChild,作为替换用的newChild
#    nodeList = root.elementsByTagName('element')
#    parentId = "0"
#    parent = root
#    if item.parent():
#        parentId = item.parent().data(0, 32)[0]
#    oldChild = None
#    for i in range(len(nodeList)):
#        node = nodeList.at(i)
#        if node.toElement().attribute("id") == parentId:
#            parent = node
#        if node.toElement().attribute("id") == id:
#            oldChild = node
#    if oldChild:
#        parent.replaceChild(newChild, oldChild)
#    return    

    nodeList = root.elementsByTagName('element')
    target = None
    for i in range(len(nodeList)):
        node = nodeList.at(i)
        if node.toElement().attribute("id") == id:
            target = node
    if target:
        elem = target.toElement()
        if elem.hasAttribute("name"):
            elem.setAttribute("name", name)
    return
    
def removeElem(mw, root, id, item):
    '''移除元素'''
    nodeList = root.elementsByTagName('element')
    parentId = "0"
    parent = root
    if id != "0":
        parentId = mw.chapIdDict.get(id)
    child = None
    for i in range(len(nodeList)):
        node = nodeList.at(i)
        if node.toElement().attribute("id") == parentId:
            parent = node
        if node.toElement().attribute("id") == id:
            child = node
    parent.removeChild(child)
    return
    
#        cNodeList = node.childNodes()
#        for i in range(len(cNodeList)):
#            cNode = cNodeList.at(i)    
#    while not child.isNull():
#        childElem = child.toElement()
#        print(childElem.attribute('id'))
#        if childElem.attribute('id') == str(id):
#            
#            item.parent().removeChild(child)#移除
##            break
#        child = child.nextSibling()
#    return
#    
def appendElem(mw, root, elem, child, chapPos):
    '''添加元素 parent,要写入列表'''
    node = mw.ui.chapTree.currentItem()
    mode = "root"
    if node:
        parent = node.parent()#获取父章节
        nodeId, nodeType = node.data(0, 32)
        if chapPos == "2":#添加到章节内
            #当前节点是练习就添加到当前节点的父章节下,当前节点是章节就添加到当前节点下
            if nodeType != "pres":#节点是练习
                if not parent:
                    parent = root
                else:#必须用节点模式,将parent取出id,根据id添加,非常重要!
                    mode = "node"
            else:#节点是章节
                parent = node#此节点是TreeWidgetItem
                mode = "node"
#            __appendElem(parent, elem, child, chapPos, nodeId)
        else:#插入到当前节点之前或之后
            #无论是不是章节都要添加到父章节下!
            #根章节节点
            if not parent:
                parent = root
                mode = "root"
    else:
        parent = root
#        mode = "root"
        chapPos = "2"#强制放在root下
        nodeId = "0"
    return __appendElem(parent, elem, child, chapPos, nodeId, mode)#140922修改
    
def __appendElem(parent, elem, child, chapPos, nodeId, mode):
    '''添加元素'''
    '''mode:=root,表示在根节点下添加;=node表示在章节下添加'''
    if mode == "root":#表示当前节点为根节点
        if chapPos == "2":#添加到文档末
            parent.appendChild(elem)
        else:
            while not child.isNull():
                if child.toElement().attribute('id') == str(nodeId):            
                    if chapPos == "1":#插入当前位置之后
                        parent.insertAfter(elem, child)
                    elif chapPos == "0":#插入当前位置之前
                        parent.insertBefore(elem, child)
                    return True#140922新增
                child = child.nextSiblingElement()
    else:#表示当前节点非根节点
        parentId = parent.data(0, 32)[0]
        while not child.isNull():
            if chapPos == "2":#章节下添加
                if child.toElement().attribute('id') == str(parentId):
                    child.appendChild(elem)#添加到章节内
                    return True#140922新增
            else:
                if child.toElement().attribute('id') == str(parentId):
                    childNode = child.firstChildElement('element')
                    while not childNode.isNull():#继续循环以找到子节点
                        if childNode.toElement().attribute('id') == str(nodeId):
                            if chapPos == "1":#插入当前节点之后 
                                child.insertAfter(elem, childNode)
                            elif chapPos == "0":#插入当前位置之前
                                child.insertBefore(elem, childNode)
                            return True#140922新增
                        childNode = childNode.nextSiblingElement()
            child = child.nextSiblingElement()
    return
    
def setElement(element, id, type, name, disabled=None):
    '''设置元素'''
#    useSubSet = courseDict["useSubSet"]
#    subSetId = courseDict["subSetId"]
#    subTypeId = courseDict["subTypeId"]
#    useSubType = courseDict["useSubType"]
    element.setAttribute("id", id) 
    element.setAttribute("type", type) 
    element.setAttribute("name", name)
    if disabled:
        element.setAttribute(disabled, "true")
#    if useSubSet == "1":
#        element.setAttribute("subsets", str(subSetId))
#    if useSubType == "1":
#        element.setAttribute("subtype", str(subTypeId))
    return element
 
def getCourseHead(courseName):
    '''生成课程列表头部;'''
    typeValue = "regular"
    content =  '<?xml version="1.0" encoding="utf-8"?>' + '\n'\
                + '<course xmlns="http://www.supermemo.net/2006/smux">' + '\n'\
                + '  <guid>' + getGuid() + '</guid>' + '\n'\
                + '  <title>' + courseName + '</title>' + '\n'\
                + '  <created>' + QtCore.QDate.currentDate().toString("yyyy-MM-dd") + '</created>' + '\n'\
                + '  <modified>' + QtCore.QDate.currentDate().toString("yyyy-MM-dd") + '</modified>' + '\n'\
                + '  <language-of-instruction>en</language-of-instruction>' + '\n'\
                + '  <language-taught>en</language-taught>' + '\n'\
                + '  <default-items-per-day>30</default-items-per-day>' + '\n'\
                + '  <default-template-id>1</default-template-id>' + '\n'\
                + '  <type>' + typeValue + '</type>' + '\n'\
                + '  <author>舍得</author>' + '\n'\
                + '  <rights-owner>舍得</rights-owner>' + '\n'\
                + '  <description lang="en">本课程由SuperMemo课程编辑器制作</description>' + '\n'\
                + '  <translators>舍得</translators>' + '\n'\
                + '  <box-link>www.emagic.org.cn</box-link>' + '\n'\
                + '  <sorting>default</sorting>' + '\n'\
                + '  <version>1.0.3531</version>' + '\n'
    return content
    
def getItemIdFromDb(mw):
    '''从数据库中获取页面编号'''
    courseId = Prefs.getCourse("courseId")
    sqlExp = """select PageNum from Items WHERE courseId='%s'""" % courseId
    result = execSql(mw, sqlExp, "all")
    if result:
        try:
            mw.itemId = resultToId(result)
        except:
            mw.itemId = 1
    else:
        mw.itemId = 1
    return
    
def getItemId(settings, coursePath=None, key=None):
    """
    目前这方法还未被调用
    获取当前课程最大的itemID;
    后期要考虑将大于99990的数去掉(因为要自动加版权页);
    !!!注意,这里的elemList计算还是有点麻烦,用两个type不如直接统计<element id="">比较好;
    120607修改:传入coursePath参数,用于实时预览时处理非当前课程路径的文件;
    ——此时将不统计章节，而且返回的将是id列表
    """
    '''可以考虑用数据库来取
    sqlExp = """select PageNum from Items WHERE courseId = '%s' """ % courseId
    result = execSql(sqlExp, "all", db)
    if result:
        id = resultToId(result)#id为页面编号
    '''
    if not coursePath:
        path = Prefs.getCourse("coursePath") + "/override"#课程路径
    else:
        path = coursePath
    try:
        if not key:#直接从course.xml文件中读取
            fileName = path + "/course.xml"
            basePath = strippedPath(fileName)
            url = QtCore.QUrl.fromLocalFile(basePath).toString()       
            request = urllib.request.urlopen(url)            
            chunk = request.read()
            soup = BeautifulSoup(chunk)
            idList = []
#                if not coursePath:
            elemList = soup.findAll(attrs = {"type" : "exercise"}) + soup.findAll(attrs = {"type" : "pres"})
#                else:
#                    elemList = soup.findAll(attrs = {"type" : "exercise"})
            if elemList:
                for elem in elemList:
                    """新增判断,封面封底等ID不计在内"""
                    if elem['id'] not in ("99999", "99998", "99997"):
                        idList.append(elem['id'])
                idList.sort(key = int)
                if not coursePath:
                    return int(idList[-1])
                else:
                    return idList
            else:
                return 1

        else:#从现有item文件中读取
            hitList = []
            pattern = re.compile(key)
            dir = path + "/override"
            for root, dirs, files in os.walk(dir):
                for f in files:
                    hit = pattern.search(f)
                    if hit:
                        hitList.append(f[4:9])
            if len(hitList) > 0:
                hitList.sort(key = int)
                return int(hitList[-1]) #没有加1
            else:
                return 0
    except:
        return 0
   
def getEmptyItem(mw, id, coursePath=None):
    '''生成空的Item文件,创建新章节用'''
    '''131207准备更新为:传入head中的章节名称值'''
    if not coursePath:
        coursePath = Prefs.getCourse("coursePath")
    itemFile =  """%s\\override\\item%s.xml""" % (coursePath, getId(id))
    content = getXMLHead() + getXMLMid() + getXMLFoot()
    outputStream(mw, itemFile, content)#输出

def getXMLHead(title=None):
    """
    生成页面文件头部;与转换精灵相比,省去N多变化
    #若传入 title, 表示在使用划词插件,将使用传入的title当作quTitle
    """
    courseName = Prefs.getCourse("courseName")
    chapName = Prefs.getCourse("chapName")
    quTitle = ""
    if not title:
        mode = Prefs.getCourse("mode")
        if mode == "1":
            quTitle = Prefs.getCourse("spellTxt")
        elif mode == "2":
            quTitle = Prefs.getCourse("qaTxt")
        elif mode == "3":
            quTitle = Prefs.getCourse("chooseTxt")
        elif mode == "4":
            quTitle = Prefs.getCourse("tfTxt")
    else:
        quTitle = title
#    print(courseName)
#    print(chapName)
#    print(quTitle)
    content =  '<?xml version="1.0" encoding="utf-8"?>' + '\n'\
                + '<item xmlns="http://www.supermemo.net/2006/smux">' + '\n'\
                + '  <lesson-title>' + courseName + '</lesson-title>' + '\n'\
                + '  <chapter-title>' + chapName + '</chapter-title>' + '\n'\
                + '  <question-title>' + quTitle + '</question-title>' + '\n'\
                + '  <question>'
    return content

def getXMLMid():
    '''item文件中部'''
    content =  '</question>' + '\n' + '  <answer>'
    return content        
            
def getXMLFoot(chrome=None):
    #注意,传过来的是包括所有qa的moduleDict,用于判断自动音频
    #chrome传入时,指为插件服务
    tempNum = Prefs.getCourse("tempNum")
    tempImg = Prefs.getCourse("tempImg")
    date = QtCore.QDate.currentDate().toString("yyyy-MM-dd")
    content = '</answer>' + '\n'
    if not chrome:
        if Prefs.getCourse("autoAudioQ") == "1":#输出question-audio
            content += '  <question-audio>true</question-audio>' + '\n'
        if Prefs.getCourse("autoAudioA") == "1":
            content += '  <answer-audio>true</answer-audio>' + '\n'
    elif chrome == "q":
        content += '  <question-audio>true</question-audio>' + '\n'
    elif chrome == "a":
        content += '  <answer-audio>true</answer-audio>' + '\n'
    content += '  <modified>' + date + '</modified>' + '\n'\
                + '<template-id>' + str(tempNum) + '</template-id>' + '\n'\
                + '<gfx-1 id=\"' + str(tempImg) + '\" group-id=\"1\" />' + '\n'\
                + '</item>'  + '\n'  
    return content

def saveEditItem(mw):
    '''储存对现有item的编辑'''
    question = mw.ui.questionTE.toPlainText()
    question = escaping(question)
    answer = mw.ui.answerTE.toPlainText()
    answer = escaping(answer)
    item = mw.ui.chapTree.currentItem()        
    itemId, type = item.data(0, 32)
    itemFile = getItemFile(itemId)
    data = readFile(mw, itemFile, True)#读取页面文件内容
    data = re.sub('<question>[\s\S]*?</question>', """<question>%s</question>""" % question, data, re.M)
    data = re.sub('<answer>[\s\S]*?</answer>', """<answer>%s</answer>""" % answer, data, re.M)
    outputStream(mw, itemFile, data)#写回item文件
            
def escaping(data):
    """
    转义;
    可否改为字典的形式?
    """
    if data is not None:
        data = data.replace('&amp;amp;', '&')
        data = data.replace('&amp;', '&')
        data = data.replace('&', '&amp;')
        data = data.replace('e͟ɪ', 'eɪ')
        data = data.replace('ɔː', 'ɔ:')
        data = data.replace('e̱', 'e')
#        data = data.replace('<', '&lt;')
#        data = data.replace('>', '&gt;')
        data = data.replace('&lt;br&gt;', '<br/>')
        data = data.replace('<br>', '<br/>')
        data = data.replace('\x02', '<br/>')
        data = data.replace('&lt;br/&gt;', '<br/>')
#        data = data.replace('\n', '')
#        data = data.replace('\r', '')
    return data
    
def splitDefinition(txt):
    '''尝试分割中英文释义'''
    #若只有一个值，则默认中英文都为此值
    #todo, 未考虑到列表长度>2的情况
    defList = txt.split('<br/>')
    if not defList:
        return
    if len(defList) == 1:
        return [defList[0], defList[0]]
    result = []
    if re.search(r'^\s+$',defList[1], re.M):
        return [defList[0], defList[0]]
    else:
        return [defList[0], defList[1]]
        
def resetModelCombo(mw, pr=None):
    '''重置modelCombo'''
    #只传mw时表示适用于主窗口的modelCombo,传入pr表示合适用config窗口的
    combo = mw.ui.modelCombo
    if pr:
        combo = pr.ui.modelCombo
    combo.clear()
    if mw.confDict:
        confDict = OrderedDict(sorted(mw.confDict.items(), key=lambda t: int(t[0])))
        for k, v in confDict.items():
            combo.addItem(v['name'], k)
        modelId = Prefs.getCourse('model')
        index = combo.findData(modelId)
        if index is None:
            index = 0
        combo.setCurrentIndex(index)
            
def getModelId(pr):
    '''取modelCombo中的data'''
    index = pr.ui.modelCombo.currentIndex()
    return pr.ui.modelCombo.itemData(index)
        
def loadConf(mw):
    '''根据当前modelCombo载入conf'''
    modelId = getModelId(mw)
    if pr:
        modelId = getModelId(pr) #todo,其实两个应该是一样的
    
    conf = mw.confDict.get(str(modelId))
    if not conf:
        return
    modelConf = conf.get('conf')
    if not modelConf:
        return
    mode, audioType, qaMode, spellMode, spellHint, imageMatch, useSentence, useCnDefinition, scaleValue = modelConf   
    #['2', 4, 0, 1, 1, True, True, False, 930]
    #控制主窗口的RB
    if mode == "1":
        mw.ui.spellRB.setChecked(True)
    else:#拒绝出现除1、2外的参数
        mw.ui.qaRB.setChecked(True)
    try:
        mw.ui.audioTypeCombo.setCurrentIndex(audioType) #语音库类型
        mw.ui.qaModeCombo.setCurrentIndex(qaMode) #问答模式
        mw.ui.spellModeCombo.setCurrentIndex(spellMode)#填空模式
        mw.ui.spellHintCombo.setCurrentIndex(spellHint)#填空提示
        mw.ui.imageMatchCB.setChecked(imageMatch)#自动匹配图片
        mw.ui.useSentenceCB.setChecked(useSentence)#启用原始例句
        mw.ui.useCnDefinitionCB.setChecked(useCnDefinition)#启用中文释义 
        mw.ui.scaleLocalSpin.setValue(pr.getScale(scaleValue)) 
    except:
        pass
            
def writeItemFileFromChrome(pr, fields, audio, preview=None):
    '''写入页面文件@chrome划词助手'''
    word = fields.get('expression')
    phonetic = fields.get('reading')
    sentence = fields.get('sentence')
    if sentence:
        sentList = sentence.split('\n\n')
        if sentList:
            sentence = sentList[-1]
        sentence = escaping(sentence)
        
    if phonetic:
        phonetic = phonetic.replace('/', '') #将/去掉，注意，这不仅是去除首尾的/
        if not re.search(r'^\s+$',phonetic, re.M):
            phonetic = """<br/>[%s]""" % phonetic
    txtQ = """%s%s""" % (word, phonetic)
#    question = mw.ui.questionTE.toHtml()
    question = txtQ = escaping(txtQ)#转义处理
    txtAList = fields.get('glossary')
    if not txtAList:#无释义,直接放弃操作
        return
    txtA = '<br/>'.join(txtAList) #传入的释义是列表格式
    answer = txtA = escaping(txtA)

    ###通用变量
    modelId = Prefs.getCourse("modelId") #0:无;1:在线美音;2:在线英音;3:本地;
    if modelId is None:
        modelId = 0    

    conf = pr.mw.confDict.get(str(modelId))
    if not conf:
        return
    modelConf = conf.get('conf')
    mode, audioType, qaMode, spellMode, spellHint, imageMatch, useSentence, useCnDefinition, scaleValue = modelConf
    if mode is None:
        mode = 1
    mode = int(mode)
    if not useCnDefinition:
        defList = splitDefinition(answer)
        if defList:
            answer = defList[1]
            
#    audioType = Prefs.getCourse("audioType") #0:无;1:在线美音;2:在线英音;3:本地;
#    qaMode = Prefs.getCourse("qaMode") #0:常规,即回忆释义; 1:回想词汇
#    spellMode = Prefs.getCourse("spellMode") #1:例句填空;2:单词听写
#    mode = Prefs.getCourse("mode") #题型,1:填空;2:问答
#    useSentence = Prefs.getCourse("useSentence") #启用原始例句
#    useCnDefinition = Prefs.getCourse("useCnDefinition") #启用中文释义
    audSrc = None #源音频文件    
    
    title = "根据提示填空"

    def getSuffix():
        '''主要用于音频后缀的获取'''
        if mode == 1:#填空
            if spellMode == 0:#例句填空
                return "a"
            else: #单词听写
                return "q"
        elif mode == 2: #问答
           if qaMode == 0:#回忆释义
               return "q"
           else:#回想单词
               return "a"

    def getTitle(audSrc):
        '''根据模式返回title'''
        if mode == 1:#填空
            if spellMode == 0:#例句填空
                return "根据提示填空"
            else:#单词听写
                if audSrc:
                    return "聆听录音,拼写单词,回忆释义"
                else:#无音频的情况,还是做成回忆释义
                    return "看单词, 回忆释义"
        elif mode == 2:#问答
            if qaMode == 0:#回忆释义
                return "看单词, 回忆释义"
            else:
                return "根据释义, 回想单词"
            
                
    ###音频处理
    suffix = getSuffix() #音频后缀
    
    if mode == 1 and spellMode == 1 and audioType == 0:
        audioType = 3 #单词听写模式下,当audioType为0时强制使用本地语音库
    if audioType is not None:
        audSrc = pr.getAudio(word, suffix, fields, audioType)
    else:
        suffix = None #后缀,兼作音频代码信号
    ###页面内容处理
    if mode == 2 and qaMode == 1:#问答题,逆向,将二者返过来
        #逆向时对其英文释义部分进行处理,单词部分用~代替
        question = replaceWord(word, txtA)
        answer = txtQ
    elif mode == 1: #填空题
        if spellMode == 0:#例句填空
            #todo, 未考虑到例句中词汇是变形词的情况
            hint = ""
#            spellHint = Prefs.getCourse("spellHint")
            if spellHint is not None:
                spellHint = int(spellHint)
#                defList = txtA.split('<br/>')
                defs = splitDefinition(txtA)
                if not defs:
                    return
                cnDef, enDef = defs
#                cnDef = re.sub(r'^.*?<samp>(.*?)</samp>', r'\1', defList[0], re.M)
#                cnDef = re.sub(r'^.*?<span.*?>(.*?)</span>', r'\1', defList[0], re.M) #只取span标签内
#                cnDef = re.sub(r'^.*?<samp>(.*?)</samp>', r'\1', defList[0], re.M) #只取samp标签内
                if spellHint == 1:
                    #直接显示中文释义
                    hint = cnDef
                elif spellHint == 2:
                    #中文释义隐式显示
                    hint = """<text><sentence><small>给点提示?</small></sentence>"""\
                        """<translation>%s</translation></text>""" % cnDef
                elif spellHint == 3:
                    #英文释义隐式显示
                    if len(defList) < 2:
                        return
                    enDef = replaceWord(word, defList[1])
                    hint = """<text><sentence><small>给点提示?</small></sentence>"""\
                        """<translation>%s</translation></text>""" % enDef                    
#            question = re.sub(r'<b>(.*?)</b>', r"""<spellpad correct="\1" /> (%s)""" % hint, sentence)
            question = re.sub(r""" %s """ % word, r""" <spellpad correct="%s" /> (%s)""" % (word, hint), sentence)
        elif spellMode == 1:
            #单词听写
            if audioType is not None and audSrc:
                question = """<spellpad correct="%s" /><br/>""" % word
                answer = """%s<br/>%s""" % (phonetic, answer)
    '''启用例句'''
    if useSentence:
        if mode == 1 and spellMode == 0:
            answer = answer
        else:
            answer = """%s<br/><br/><code>%s</code>""" % (answer, sentence)
        
    ###图片处理
    imgQ = ""
    imgA = ""
#    imageMatch = Prefs.getCourse("imageMatch") #图片匹配
    if imageMatch:
        imgSrc = pr.mw.searchImage(word)
        if imgSrc:
            imgSuffix = pr.mw.imageList.pop(0)
            ext = pr.mw.ui.imgFormatCombo.currentText().lower()
            imgDst = getMediaFile(pr.mw, imgSuffix, ext, None, pr.mw.itemId)
            copyFile(imgSrc, imgDst)
            scaleLocal = Prefs.getCourse("scaleLocal")
            if scaleLocal is None:
                scaleLocal = 1024
            imgQ += """<gfx file='%s' scale-base='%s' /><br/>""" % (imgSuffix, scaleLocal)

    '''写入Item文件'''
    head = getXMLHead(getTitle(audSrc))
    foot = getXMLFoot(suffix) #音频代码的插入在此处进行
    txt = treatQA(pr.mw, question, answer)#mw在选择题处理中用到
    content = head + imgQ + txt + imgA + foot
    if not preview:#表示实时写入
        coursePath = Prefs.getCourse("coursePath")
        courseFile =  """%s\\override\\item%s.xml""" % (coursePath, getId(pr.mw.itemId))    
        return outputStream(pr.mw, courseFile, content)#输出,返回信号
    else:#表示预览,返回内容以供调用
        return content

def replaceWord(word, txt):
    '''将txt中的word替换成~'''
    if re.search(r"""[> ]%s[< ]""" % word, txt):
        txt = re.sub(r"""([> ])%s([< ])""" % word, r'\1~\2', txt)
        txt = re.sub(r'<b>(.*?)</b>', r'\1', txt)
    else:
        txt = re.sub(r'<b>.*?</b>', '~', txt)
    return txt
            
def writeItemFile(mw, preview=None):
    '''写入页面文件'''
    '''注意,要适应空页面'''
    question = mw.ui.questionTE.toPlainText()
#    question = mw.ui.questionTE.toHtml()
    question = escaping(question)#转义处理
    answer = mw.ui.answerTE.toPlainText()
    answer = escaping(answer)    
    ###图片处理
    countImgQ = mw.ui.qImgLW.count()
    countImgA = mw.ui.aImgLW.count()
    imgQList = []
    imgAList = []
    #取图片扩展名
    for i in range(countImgQ):
        item = mw.ui.qImgLW.item(i)
        imgQList.append(item.text())
    for i in range(countImgA):
        item = mw.ui.aImgLW.item(i)
        imgAList.append(item.text())
    imgQ = ""
    imgA = ""
    scaleQ = Prefs.getCourse("scaleQ")
    if scaleQ is None:
        scaleQ = 1024
    scaleA = Prefs.getCourse("scaleA")
    if scaleA is None:
        scaleA = 1024
    if len(imgQList) > 0:
        for i in imgQList:
            imgQ += """<gfx file='%s' scale-base='%s' /><br/>""" % (i, scaleQ)
    if len(imgAList) > 0:
        for i in imgAList:
            imgA += """<gfx file='%s' scale-base='%s' /><br/>""" % (i, scaleA)
    ###音频处理
    countAud = mw.ui.audLW.count()
    audList = []
    #取音频扩展名
    for i in range(countAud):
        item = mw.ui.audLW.topLevelItem(i)
        audList.append(item.text())  
    aud = "<br/>"
    if len(audList) > 0:
        for i in audList:
            aud += """<sfx file='%s' />　""" % i        
    '''写入Item文件'''
    head = getXMLHead()
#    mid = getXMLMid()
    foot = getXMLFoot()

#    question = imgQ + question + aud#图片放在前面,音频放后面)
#    answer = imgA + answer
    txt = treatQA(mw, question, answer)#mw在选择题处理中用到
#    print(txt)
    content = head + imgQ +  aud + txt + imgA + foot
    if not preview:#表示实时写入
        coursePath = Prefs.getCourse("coursePath")
    #    courseName = Prefs.getCourse("courseName")
        itemFile =  """%s\\override\\item%s.xml""" % (coursePath, getId(mw.itemId))    
    #    courseFile =  """%s\\%s\\override\\item%s.xml""" % (coursePath, courseName, getId(id))
        return outputStream(mw, itemFile, content)#输出
    else:#表示预览,返回内容以供调用
        return content

def deleteItemFile(mw):
    '''删除刚添加的页面文件'''
    '''主要用于写入课程列表失败的情况'''
    coursePath = Prefs.getCourse("coursePath")
    id = getId(mw.itemId)
    mediaPath = """%s\\override\\media""" % coursePath
    itemFile =  """%s\\override\\item%s.xml""" % (coursePath, id)
    if os.path.exist(itemFile):
        os.remove(itemFile)
    #删除媒体文件
    for i in files(mediaPath, """%s*.*""" % id):
        os.remove(i)

def files(dir, name):
    """列出指定目录下的指定文件"""
    for i in glob.glob(os.path.join(dir, name)):
        yield i

def updateChapTree(mw, name, type):
    '''更新chapTree'''
    chapPos = str(Prefs.getCourse("chapPos"))#章节插入位置
    if type == "exercise":
        chapPos = str(Prefs.getCourse("itemPos"))#页面插入位置
    node = mw.ui.chapTree.currentItem()
    item = QtGui.QTreeWidgetItem()
    if node:
        parent = node.parent()#获取父章节
        nodeType = node.data(0, 32)[1]
        if chapPos == "2":
            '''添加到之内'''
            if nodeType == "pres":#章节
                node.addChild(item)
            else:#练习
                if parent:
                    parent.addChild(item)
                else:#无父章节,则添加到树下
                    mw.ui.chapTree.addTopLevelItem(item)
        else:
            '''添加到之前或之后'''
            if parent:#有父章节
                index = parent.indexOfChild(node)#取节点的索引
                parent.insertChild(index + int(chapPos), item)
            else:#无父章节
                index = mw.ui.chapTree.indexOfTopLevelItem(node)#取节点的索引
                mw.ui.chapTree.insertTopLevelItem(index + int(chapPos), item)
    else:#未选节点,则直接加到树中
        item = QtGui.QTreeWidgetItem(mw.ui.chapTree)
    item.setText(0, name)
    item.setData(0, 32, [mw.itemId, type])
    if type == "pres":
        item.setIcon(0, mw.folderIcon)
    else:
        item.setIcon(0, mw.bookmarkIcon)    
    if type == "pres":
        mw.curChapId = mw.itemId
        mw.curChap = item
        
def treatQA(mw, question, answer):
    '''对问题和答案内容进行处理'''
    '''mode:1.填空;2.问答;3.选择;4.是非;'''
    mode = Prefs.getCourse("mode")
    mid = getXMLMid()
    if len(question) > 0:
#        print(len(question))
        if mode == "1":
            #填空题
            return uxSpellPad(mw, question, answer)
        elif mode == "2":
            return question + mid + answer.replace('\n', '<br/>')
        elif mode == "3":
            #选择题
            try:
                return uxChoose(mw, question, answer)#mid部分在选择题处理时添加,因考虑到有解析存在
            except:#做成问答题
                return question + mid + answer.replace('\n', '<br/>')
        elif mode == "4":
            #是非题
            return uxTrueFalse(mw, question, answer)
    else:
        if mode == "2":
            if  answer:
                return mid + answer
            else:
                return mid
        else:
            return mid
        
def uxSpellPad(mw, question, answer):
    '''处理填空题'''
    '''填空题的素材中,question中对应answer的部分统一打[]标记,以便替换'''
    mid = getXMLMid()
    hintCount = 0
    answerList = answer.split('\n')
    keyList = None
    note = None#解析
    if len(answerList) == 0:
        SMMessageBox.information(mw,
            mw.trUtf8("注意"),
            mw.trUtf8(
                '''<p>答案还没输入哦！</p>'''))
        return
    elif len(answerList) >= 1:
        keyList = multiKey(answerList[0], True)#第二个值意味着将使用双管道符进行分割
        if len(answerList) > 1:#有答案和解析
            note = answerList[1]
    if keyList:
        for i in keyList:
            hintWord = " /></big>"#直接结尾
            if int(hintCount) > 0 and int(hintCount) < len(i):
                hintWord = ">" + i[0:int(hintCount)] + "</spellpad></big>"
            #那就用答案对question进行替换
            question = question.replace("""[]%s""" % i, """<big><spellpad correct="%s"%s""" % (i,  hintWord), 1)
        result = question + mid
        if note:#有解析的话,附上解析
            result += note            
        return result
    
def uxTrueFalse(mw, question, answer):
    '''处理是非题'''
    def answerConv(txt):
        #处理定位模式下对全半角数字,大小写字母的处理,宜完善全角和小写
        tfList = ["true", "True", "TRUE", "Yes", "yes", "YES", "对", "正确", "√", "是", "A", "T", "Y", "y", "1"]
        if txt in tfList:
            return "true"
        else:
            return "false"      
    trueText = "对"
    falseText = "错"
    mid = getXMLMid()
    answerList = answer.split('\n')
    answerTxt = None
    note = None#解析
    if len(answerList) == 0:
        SMMessageBox.information(mw,
            mw.trUtf8("注意"),
            mw.trUtf8(
                '''<p>答案还没输入哦！</p>'''))
        return
    elif len(answerList) >= 1:
        answerTxt = answerList[0]
        answerTxt = answerTxt.strip("|")
        if len(answerList) > 1:#有答案和解析
            note = answerList[1]
    if answerTxt:
        result = """%s<br/><br/><true-false true="%s" false="%s" correct="%s" /><br/>%s""" % \
            (question, trueText, falseText, answerConv(answerTxt), mid)
        if note:
            result += note
        return result
            
def uxChoose(mw, question, answer):
    '''处理选择题'''
    mid = getXMLMid()
    stem, option = question.split("\n")
    optionList = multiKey(option, True)#第二个值意味着将使用双管道符进行分割
    answerList = answer.split('\n')
    keyList = None
    note = None#解析
    if len(answerList) == 0:
        SMMessageBox.information(mw,
            mw.trUtf8("注意"),
            mw.trUtf8(
                '''<p>答案还没输入哦！</p>'''))
        return
    elif len(answerList) >= 1:#有答案
        keyList = multiKey(answerList[0])
        if len(answerList) > 1:#有答案和解析
            note = answerList[1]
    if keyList:
        for i in range(len(keyList)):#对答案进行处理
            keyList[i] = keyConv(keyList[i])
        #处理选项
        optionTxt = ""
        for num, i in enumerate(optionList):
            num = str(num + 1)#用这个去跟key核对
            if num in keyList:
                optionTxt += """<option correct="true">%s</option>""" % autoTrim(i).replace("<br/>", "")
            else:
                optionTxt += """<option>%s</option>""" % autoTrim(i).replace("<br/>", "")
        chooseStyle = "2" #强制使用竖排
        brSymbol = "<br/>" #默认,预留后期处理接口
        if len(keyList) <= 1:
            if chooseStyle == "1":#横排
                chooseHead = '<br/><radio orientation="horizontal">'
                chooseFoot = '</radio>' + brSymbol
            elif chooseStyle == "2":#竖排
                chooseHead = '<br/><radio display="inline">'
                chooseFoot = '</radio>' + brSymbol
            elif chooseStyle == "3":#行内
                chooseHead = '<radio display="inline">'
                chooseFoot = '</radio>'
            elif chooseStyle == "4":#0927新增:拼接式
                chooseHead = '<br/><radio display="inline">'
                chooseFoot = '</radio>' + brSymbol
        else:#自动转多选
            if chooseStyle == "1":#横排
                chooseHead = '<br/><checkbox orientation="horizontal">'
                chooseFoot = '</checkbox>' + brSymbol
            elif chooseStyle == "2":#竖排
                chooseHead = '<br/><checkbox display="inline">'
                chooseFoot = '</checkbox>' + brSymbol
            elif chooseStyle == "3":#行内
                chooseHead = '<checkbox display="inline">'
                chooseFoot = '</checkbox>'
        optionTxt = optionTxt.replace("<option></option>", "")#0918新增,去除可能产生的多余选择空项
        result = stem + chooseHead + optionTxt + chooseFoot + mid
        if note:#有解析的话,附上解析
            result += note
        return result
    
def multiKey(key, mode=None):
    """处理定位模式下的多个答案"""
    """处理标记模式下仅使用一个题肢的情况:useOneBranch"""
    """传入mode值的时候,只启用双管道符切分"""
    multiKey = []
    if mode:
        multiKey = key.split('||')
    else:
        if  re.search(r'\|\|', key):
            multiKey = key.split('||')
        elif re.search(r'\|', key):
            multiKey = key.split('|')
        elif re.search(r',', key):
            multiKey = key.split(',')
        elif re.search(r'　', key):#全角空格
            key = key.replace(' ', '')#去除半角空格再清理
            key = key.replace('　', '')#去除全角空格再清理
            multiKey = list(multiKey)
        elif re.search(r' ', key):#半角空格
            key = key.replace(' ', '')#去除空格再清理
            multiKey = list(key)
        else:#不用任何符号
            multiKey = list(key)
    keys = []
    for i in multiKey:
        if len(i) > 0:
            keys.append(i)
    return keys
    
def keyConv(key):
    """#处理定位模式下对全半角数字,大小写字母的处理"""
    keyV = ord(str(key))
    if keyV < 58:#半角数字,取到9
        keyV = keyV - 48
    elif keyV > 64 and keyV < 74:#大写字母,取到I
        keyV = keyV - 64
    elif keyV > 96 and keyV < 106:#小写字母,取到i
        keyV = keyV - 96
    elif keyV > 65296 and keyV < 65306:#全角数字,取到９
        keyV = keyV - 65296
    elif keyV > 65312 and keyV < 65322:#全角大写字母,取到I
        keyV = keyV - 65312
    elif keyV > 65344 and keyV < 65354:#全角小写字母,取到i
        keyV = keyV - 65344            
    keyV = str(keyV)
    return keyV
                
def autoTrim(txt):
    """去除文本前的abcd等符号"""
    """样式:0.半角字母+、
    1.半角字母+.
    2.半角字母
    3.全角字母+.
    4.全角字母+、
    5.全角字母+、
    6.半角数字+、
    7.半角数字+.
    8.半角数字
    9.全角数字+、
    10.全角数字+.
    11.全角数字, 
    12.中文数字+、
    13.中文数字+.
    14.中文数字
    15.英文半角括号数字
    16.中文半角括号数字
    17.加圈数字"""
#            print(useTrim)
    trimType = "1" #强制为1
    pattern =  re.compile(r"^[a-fA-F]\.", re.M)
    if trimType == "0":
        pattern =  re.compile(r"^[abcdefABCDEF]、", re.M)
    elif trimType == "1":
        pattern =  re.compile(r"^[abcdefABCDEF]\.", re.M)
    elif trimType == "2":
        pattern =  re.compile(r"^[abcdefABCDEF]", re.M)
    elif trimType == "3":
        pattern =  re.compile(r"^[ａｂｃｄｅｆＡＢＣＤＥＦ]\.", re.M)
    elif trimType == "4":
        pattern =  re.compile(r"^[ａｂｃｄｅｆＡＢＣＤＥＦ]、", re.M)
    elif trimType == "5":
        pattern =  re.compile(r"^[ａｂｃｄｅｆＡＢＣＤＥＦ]", re.M)
    elif trimType == "6":
        pattern =  re.compile(r"^[123456]\.", re.M)
    elif trimType == "7":
        pattern =  re.compile(r"^[123456]、", re.M)
    elif trimType == "8":
        pattern =  re.compile(r"^[123456]", re.M)
    elif trimType == "9":
        pattern =  re.compile(r"^[１２３４５６]\.", re.M)
    elif trimType == "10":
        pattern =  re.compile(r"^[１２３４５６]、", re.M)
    elif trimType == "11":
        pattern =  re.compile(r"^[１２３４５６]", re.M)
    elif trimType == "12":
        pattern =  re.compile(r"^[一二三四五六]\.", re.M)
    elif trimType == "13":
        pattern =  re.compile(r"^[一二三四五六]、", re.M)
    elif trimType == "14":
        pattern =  re.compile(r"^[一二三四五六]", re.M)
    elif trimType == "15":
        pattern =  re.compile(r"^\([123456]\)", re.M)
    elif trimType == "16":
        pattern =  re.compile(r"^（[123456]）", re.M)
    elif trimType == "17":
        pattern =  re.compile(r"^[①②③④⑤⑥]", re.M)
    txt = pattern.sub("", txt)
    txt = txt.strip(' ')
    return txt

#def writeSource(mw):
#    '''写入源文件'''
#    """先确定输出文件"""
#    date = QtCore.QDate.currentDate().toString("yyyyMMdd")
#    pre = "SP"
#    if mw.ui.qaRB.isChecked():
#        pre = "QA"
#    elif mw.ui.chooseRB.isChecked():
#        pre = "CH"
#    elif mw.ui.tfRB.isChecked():
#        pre = "TF"            
#    outFile = """./output/%s_%s.txt""" % (pre, date)
#    question = mw.ui.questionTE.toPlainText()
#    question = question.replace('\n', '\t')#替换
#    answer = mw.ui.answerTE.toPlainText()
#    content = """%s\t%s\n""" % (question, answer)
#    outputStream(mw, outFile, content, "append2")
    
def getUserList(mw):
    '''获取用户数据,可同时为"写入数据库"和"课程同步"服务'''
    import platform
    import getpass
    system = "win7"
    if "XP" in platform.platform():
        system = "winxp"
    sysUser = getpass.getuser()
    drive = os.getenv("SystemDrive")
    userPath = """%s/Users/%s/AppData/Roaming/"""\
        """SuperMemo World/SuperMemo UX/""" % (drive, sysUser)
    if system == "winxp":
        userPath = """%s/Documents and Settings/%s/Application Data"""\
            """/SuperMemo World/SuperMemo UX/""" % (drive, sysUser)
    userFile = """%sUsers.dat""" % userPath
#    SMMessageBox.information(self,
#        self.trUtf8("路径"),
#        self.trUtf8(
#            '''<p>请使用"打开课程"功能打开此课程.</p>'''
#            '''<p>%s!</p>''' % userFile))    
    userList = []
    if os.path.exists(userFile):
        data = readFile(mw, userFile, "getData")
        soup = BeautifulSoup(data)
        userTags = soup.findAll("user", {"login":True})
        if userTags:
            for i in userTags:
                userList.append(i["login"])
    return (userPath, userList)

def verifyCourseName(mw, courseName):
    '''校验课程名称'''
    sqlExp = """SELECT * FROM Courses WHERE TITLE='%s'""" % courseName
    return execSql(mw, sqlExp, "all")
            
def resultToId(result, count=None):
    '''将表中取出的result中最大的Id取出,加1后返回'''
    #获取id列表
    idList = []
    guids = []
    exList = [99999, 99998, 99997, 99996, 99995, 99994]#排除列表
    newId = 1
    if result:
        for rec in result:
            if rec[0] not in exList:
                idList.append(rec[0]) 
            if count:#如果传过来的是两个
                guids.append(rec[1])
        if len(idList) > 0:
            idList.sort(key=lambda x:int(x))
            newId = int(idList[-1]) + 1
        if count:
            return (newId, guids)
        else:
            return newId
 
def date_uxStamp(dt):
    '''将日期转为ux 5位时间戳,适用于iphone数据转ux'''
    value = time_timestamp(dt)
    #原值中加了1000,要先除以1000,再加回时差再除以每日秒数
    return int((value / 1000 + 3600 * 8) / 86400)
    
def time_timestamp(dt):
    #dt为字符串
    s = time.mktime(time.strptime(dt, '%Y-%m-%d'))
    #因SuperMemo.db需要,比常规时间戳多3位
    return int(s * 1000)

def getCourse(mw, db=None):
    '''载入课程名称列表'''
    result = None
#    sqlExp = 'SELECT Title, Id, path, guid FROM Courses WHERE type=0'
    #加回type=0的设定
    sqlExp = 'SELECT Title, Id, path, guid FROM Courses WHERE type=0'
#    sqlExp = 'SELECT Title, Id, path, guid FROM Courses'
    result = execSql(mw, sqlExp, "all")
#    print(result)
    return result
    
def getCourseInfo(result):
    """
    查询数据库路径,以courseId为key建立courseDict;
    result为getCourse中的查询结果;        
    获取以ID为Key,guid为值的字典
    """
    guidDict = {}
    pathDict = {}
    if result:
        for title, id, path, guid in result:
            guidDict[id] = guid
#            coursePath = QtCore.QFileInfo(path).path()
            pathDict[id] = path
        return (guidDict, pathDict)  

#############解包#########
#def unpack(path=None, file=None, type=None):
#    '''解包,path为输出路径'''
##        if not path:
##            if not os.path.exists(".\\override"):
##                os.mkdir(".\\override")
##            path = "./override/"
#    if not file:
#        '''未指定文件,则提取全部'''
#        for entry in self.entries:
#            fileName = entry["name"]
#            if "/" in fileName:
#                tmpDir = path + QtCore.QFileInfo(fileName).path()
#                if not QtCore.QFile.exists(tmpDir):
#                    os.mkdir(tmpDir) 
#
#            f = open(path + fileName, "wb")
#            f.write(read_file(entry["name"]))
#            f.close()
#    else:#指定文件名
#        if file in self.files:
#            if type in ("preview", "data"):
#                '''用于预览或直接指定返回该文件的内容'''
#                return self.read_file(file)
#            else:
#                if "/" in file:
#                    tmpDir = path + QtCore.QFileInfo(file).path()
#                    if not QtCore.QFile.exists(tmpDir):
#                        os.mkdir(tmpDir)
#                f = open(path + file, "wb")
#                f.write(read_file(file))
#                f.close() 

def read_file(mw, name):
    '''在unpack中用到'''
    if name in mw.files:
        entry = mw.files[name]
        mw.stream.seek(entry["data_offset"])
        data = mw.stream.read(entry["data_size"])
        if entry["mode"] == 1:
            data = zlib.decompress(data, -15)
        return data
            
#def getCourseData(mw, pakFile, type):
#    '''从课程包中获取指定课程文档内容'''
##        print("in")
#    def getData():
#        '''获取课程列表文件'''
#        mw.version = binascii.b2a_hex(header_data[8:10]).decode("latin")
#        if mw.version == "0101":
#            mw.headerMap = mw.headerMapOld
#        for tag, (start, end, t) in mw.headerMap.items():
#            mw.data[tag], = struct.unpack(t, header_data[start:end])
#        file = "course.xml"
#        self.__read_entries(file)#131203新增:只取一个文件         
#        self.__read_entry_name(file)
#        courseData = unpack(None, file, "data")
#        return courseData
#        
#    lockInfo = None
#    if os.path.exists(pakFile):
#        mw.stream = codecs.open(pakFile, "rb")
#        header_data = mw.stream.read(34)
#        data = header_data.decode("latin")
#        if data[:8] == "-SMArch-": 
#            if type == "lockInfo":
#                lockInfo = binascii.b2a_hex(header_data[10:12]).decode("latin")
#                mw.stream.close()
#                return lockInfo
#            elif type == "guid":
#                courseData = getData()
#                guid = parseGuid(courseData)
#                mw.stream.close()
#                return guid
#            elif type == "data":
#                data = getData()
#                mw.stream.close()
#                return data
#        mw.stream.close()
#    else:
#        return False

def parseGuid(data):
    '''获取guid'''
    xml = QtCore.QXmlStreamReader()
    xml.addData(data)
    guid = None
    while not xml.atEnd():
        xml.readNext()
        if xml.name() == "guid":
            guid = xml.readElementText()
            xml.clear()
            break
    return guid
    
def parseDbCourse(mw):
    '''根据courseId读取数据库记录,以此记录初始化章节树'''
    courseId = Prefs.getCourse("colCourseId")
    sqlExp = """SELECT PageNum, Name, Type, ParentId FROM ITEMS WHERE CourseId = '%s' ORDER BY PageNum""" % courseId
    result = execSql(mw, sqlExp, "all")
    if result:
        from util.xmlTree import XmlTree
        xmlTree = XmlTree(mw) 
        if xmlTree.parse(result):
            mw.statusBar().showMessage("数据已载入", 2000)    
    
def parseCourseList(mw, file):
    '''初始化chapTree'''
#    courseXML = readFile(mw, file, "getdata")
    print("in")

    from util.xmlTree import XmlTree
    xmlTree = XmlTree(mw)

    xmlTree.read(file)
#        mw.statusBar().showMessage("文件已载入", 2000)
 
def getFlds(type):
    '''返回数据库的字段名'''
    if type == "course":#返回COURSES表的字段
        return """Id, Guid, VersionSave, Title, BoxLink, SfxPresent, GfxPresent, LangSource, LangTaught,"""\
               """ Type, Path, SubscribeDate, ItemsPerDay, Today, TodayDone, LastPageNum, RequestedFI, OptRec, """\
               """FilterMode, FilterSorting, FilterId, LastServerUpdate, KeyboardLayout, Flags, LastSynchro,"""\
               """ LastFreeDaysUpdate, MenuOrder"""
    elif type == "item":#返回ITEMS表的字段
        return """PageNum, CourseId, Type, Disabled, Subtype, ParentId, Frequency, Name, Keywords, """\
               """PartOfSpeech, QueueOrder, PendingDate, Status, LastRepetition, NextRepetition, AFactor,"""\
               """EstimatedFI, ExpectedFI, FirstGrade, Flags, Grades, Lapses, NewInterval, NormalizedGrade, """\
               """Repetitions, RepetitionsCategory, UFactor, UsedInterval, OrigNewInterval, Keywords2"""  


def saveEditData(mw):
    '''数据编辑:储存对现有item的编辑'''
    '''#临时#暂不考虑音频/图片等文档'''
    question, answer, courseId = __getColData(mw)
    item = mw.ui.chapTree.currentItem()
    '''#注意#可否在chapTree中直接写入Data数据?'''
    itemId, type = item.data(0, 32)
    '''获取Data'''
    sqlExp = """SELECT Data FROM ITEMS WHERE PageNum = '%s'""" % itemId
    result = execSql(mw, sqlExp, "one")
    if result:
        data = result[0]
        '''替换数据'''
        data = re.sub('<question>[\s\S]*?</question>', """<question>%s</question>""" % question, data, re.M)
        data = re.sub('<answer>[\s\S]*?</answer>', """<answer>%s</answer>""" % answer, data, re.M)
        '''更新数据'''
        sqlExp = """UPDATE ITEMS SET Question='%s', Answer='%s', Data='%s', LastModified='%s'"""\
            """ WHERE PageNum='%s' and CourseId='%s'""" % (question, answer, data,  mw.today, str(itemId), courseId)
        execSql(mw, sqlExp, 'update')
    
def __getColData(mw):
    '''为writeColDb和saveEditData准备数据'''
    question = mw.ui.questionTE.toPlainText()
    answer = mw.ui.answerTE.toPlainText()
    question = sqliteEscape(question)
    answer = sqliteEscape(answer)
    courseId = Prefs.getCourse("colCourseId")
    return (question, answer, courseId)
    
def writeColDb(mw, itemId, CHAP=None, NAME=None):
    '''往采集数据库里写一条记录'''
    '''传进NAME时表示程序将对此id进行更新名称 ,暂不考虑'''
    '''ITEMS表: PageNum, CourseId, Name, Type, ParentId, Disabled, Question, Answer, Data, LastModified'''
    itemFlds = """PageNum, CourseId, Name, Type, ParentId, Disabled, Question, Answer, Data, LastModified"""
    chapPos = Prefs.getCourse("chapPos")
    curChap = Prefs.getCourse("curChap")
    parentNum = 0
    if chapPos == "2":
        parentNum = curChap    
    disabled = 0
    type = "0"
    '''CHAP是用来更新章节用的?放在列表编辑器中?'''
    if CHAP:
        type = "5"
    '''#临时#暂不考虑音频/图片等文档'''
    question, answer, courseId = __getColData(mw)
    data = writeItemFile(mw, True)
    values = """%s, %s, '%s', %s, %s, %s, '%s', '%s', '%s','%s' """ \
            % (itemId, courseId, question, type, parentNum, disabled, question, answer, data, mw.today)
    sqlExp = """INSERT INTO ITEMS (%s) VALUES (%s)""" % (itemFlds, values)
    execSql(mw, sqlExp, 'update')
        
def writeDb(mw, itemId, CHAP=None, NAME=None):
    '''往数据库里写一条记录'''
    '''传进NAME时表示程序将对此id进行更新名称'''
    itemFlds = getFlds("item")
#    chapName = Prefs.getCourse("chapName")
    name = """练习%s""" % str(itemId)
    courseId = Prefs.getCourse("courseId")
    itemPos = Prefs.getCourse("itemPos")
    curChap = Prefs.getCourse("curChap")
    parentNum = 0
    if itemPos == "2":
        parentNum = curChap
    disabled = 0 #disabled暂时默认为0
    #注意,PageNum应该就是ItemID
#    id = 1
#    sqlExp = """select PageNum from Items WHERE courseId = '%s' """ % courseId
#    result = execSql(sqlExp, "all", db)
#    if result:
#        id = resultToId(result)#id为页面编号
    #第三位type值应为5,如果是页面则为0
    type = "0"
    if CHAP:
        type = "5"
        name = Prefs.getCourse("chapName")
    values = """'%s', '%s', '%s', '%s', 0, '%s', 0, '%s', '', """\
            """'', '%s', Null, 0, 0, 0, 3.00, """\
            """0, 0, 6, 0, 0, 0, 0, 0, """\
            """0, 0, 0.00, 0, 0, '' """\
            % (str(itemId), str(courseId), type, disabled, parentNum, name, str(itemId))
    
    sqlExp = """insert into Items (%s) values (%s)""" % (itemFlds, values)
    if NAME:#更新章节名称
#        sqlExp = """update into Items (%s) values (%s) where PageNum='%s' and courseId='%s'""" % (itemFlds, values, str(itemId), str(courseId)
        sqlExp = """UPDATE Items SET Name='%s' WHERE PageNum='%s' and courseId='%s'""" % (NAME, str(itemId), courseId)
#    print(sqlExp)
    execSql(mw, sqlExp, "update")

def deleteRecord(items):
    '''移除数据库里指定记录(多条)'''
    '''传进的是item列表'''
    courseId = Prefs.getCourse("courseId")
    sqls = []
    for item in items:
        id = item.text(2)
        sqls.append("""delete from Items where PageNum=%s and courseId=%s""" % (id, courseId))
    execSql(mw, sqls, "updateAll")
    
def moveRecord(mw, items, parentId):
    '''批量移动页面:更新ParentId字段'''
    '''传进的是item列表'''
    courseId = Prefs.getCourse("courseId")
    sqls = []
    for item in items:
        id = item.text(2)
        sqls.append("""UPDATE Items SET ParentId='%s' where PageNum=%s and courseId=%s""" % (parentId, id, courseId))
    execSql(mw, sqls, "updateAll")    
    
################################################
###                预览模块相关              ### 
################################################

def GetPakFile(smpak, pakFile, fileName):
    '''解包:按指定文件'''
    content = smpak.unpack(None, fileName, "preview")
    return content

def ReadItemFile(content):
    '''解析Item文件,返回相应数据'''
    soup =  BeautifulSoup(content)
    question = GetElemText(soup.find("question"), "contents")
    answer = GetElemText(soup.find("answer"), "contents")
    command = GetElemText(soup.find("question-title"))
    chapterTitle = GetElemText(soup.find("chapter-title"))
    lessonTitle = GetElemText(soup.find("lesson-title"))
    tmpId = GetElemText(soup.find("template-id"))
    audioQ = GetElemText(soup.find("question-audio"))
    audioA = GetElemText(soup.find("answer-audio"))
    gfx1Id = 1
    gfx1Group = 1   
    gfx1Tag = soup.find("gfx-1")
    if gfx1Tag:
        gfx1Id = gfx1Tag["id"] 
        gfx1Group = gfx1Tag["group-id"]      
    return (question, answer, command, lessonTitle, chapterTitle, tmpId, audioQ, audioA, gfx1Id, gfx1Group)
    
#def ReadItemFile(smpak, pakFile, itemFile):
#    '''解析Item文件,返回相应数据,注意,未进行单引号转义'''
#    content = GetPakFile(smpak, pakFile, itemFile)
#    soup =  BeautifulSoup(content)
#    question = GetElemText(soup.find("question"), "contents")
#    answer = GetElemText(soup.find("answer"), "contents")
#    command = GetElemText(soup.find("question-title"))
#    chapterTitle = GetElemText(soup.find("chapter-title"))
#    lessonTitle = GetElemText(soup.find("lesson-title"))
#    tmpId = GetElemText(soup.find("template-id"))
#    gfx1Id = 1
#    gfx1Group = 1   
#    gfx1Tag = soup.find("gfx-1")
#    if gfx1Tag:
#        gfx1Id = gfx1Tag["id"] 
#        gfx1Group = gfx1Tag["group-id"]      
#    return (question, answer, command, lessonTitle, chapterTitle, tmpId, gfx1Id, gfx1Group)

def SavePic(picFileName, picData):
    '''写图片为bytes'''
    try:
        f = open(picFileName,"bw")
        f.write(bytes( picData ))
#        f.write( picData )
        f.close()
    except:
        pass

def GetElemText(tag, type=None):
    '''获取元素的文本)'''
    if tag:
        if not type:
            if tag.text:
                return tag.text.replace("'", "''")
            else:
                return ''
        else:
            return tag.contents
    else:
        return ''
        
def ParseItem(file, id=None):
    '''预览时提取参数'''
    """
    返回 [courseName, itemId, chapTit, quTit, qTxt, aTxt, tmpId, bgImgId, audioQ, audioA]
    """
    coursePath = Prefs.getCourse("coursePath")
    coursePath = getFileInfo("fullPath", coursePath) + "/override"
    soup = BeautifulSoup(file)
    audioQ = None
    audioA = None
    question = GetElemText(soup.find("question"), "contents")
    answer = GetElemText(soup.find("answer"), "contents")
    command = GetElemText(soup.find("question-title"))
    chapterTitle = GetElemText(soup.find("chapter-title"))
    lessonTitle = GetElemText(soup.find("lesson-title"))
    tmpId = GetElemText(soup.find("template-id"))
    audioQ = GetElemText(soup.find("question-audio"))
    audioA = GetElemText(soup.find("answer-audio"))
    gfx1Id = 1
    gfx1Tag = soup.find("gfx-1")
    if gfx1Tag:
        gfx1Id = gfx1Tag["id"]   
    return [lessonTitle, id, chapterTitle, command, question, answer, tmpId, gfx1Id, audioQ, audioA, coursePath]

def getBgImg(id):
    """
    根据背景图ID,返回背景图文件;
    注意,由于指定了base href,所以不用template文件夹
    """
    imgId = "00000" + str(id)
#    imgFile = imgId[-5:] + "_1024.png"
    imgFile = imgId[-5:] + "_0512.png"
    return imgFile

def getTmpFile(tmpId, ext, coursePath=None):
    """
    根据模板ID获取模板和CSS文件名;
    用于parseTemplate及style.css引用;
    css文件不需要带template文件夹
    """
    tmpId = getId(tmpId)
    tmpPath = "./template" + tmpId
    if coursePath:
        tmpPath = coursePath + "/template" + tmpId
    if not QtCore.QFile.exists(tmpPath):
        tmpPath = "./template/template" + tmpId
    if ext == "xml":
        return tmpPath + "/template.xml"
    elif ext == "css":
        return "template" + tmpId + "/style.css"
    
def parseTemplate(mw, tmpId, coursePath=None):
    """
    处理模板信息,返回相应的CSS内容
    """
    tmpFile = getTmpFile(tmpId, "xml", coursePath)
    if not QtCore.QFile.exists(tmpFile):
        try:
            tmpId = getId(tmpId)
        except:
            SMMessageBox.critical(mw,
                mw.trUtf8("发现异常!"),
                mw.trUtf8(
                """<p>找不到模板文件,模板编号为{0}!</p>""").format(tmpId))    
            return
    fullPath = getFileInfo("fullPath", tmpFile)
    url = "file:///" + fullPath
    request = urllib.request.urlopen(url)
    chunk = request.read()
    soup = BeautifulSoup(chunk)
    
    def transSize(size):
        '''尺寸变形'''
        return str(int(int(size) * 0.705))
        
    def getDimensions(obj):
        """
        处理四维等信息
        """
        dimensions = obj.find('dimensions')
        if dimensions:
            try:
                left = transSize(dimensions['left'])
            except:
                left = ""
            try:
                right = transSize(dimensions['right'])
            except:
                right = ""                    
            width = transSize(dimensions['width'])
#            width = "304"
            top = transSize(dimensions['top'])
            height = transSize(dimensions['height'])
#            height = "228"
            
        return [left, width, top, height, right]
        
#    def getDimensions(obj):
#        """
#        处理四维等信息
#        """
#        dimensions = obj.find('dimensions')
#        if dimensions:
#            try:
#                left = dimensions['left']
#            except:
#                left = ""
#            try:
#                right = dimensions['right']
#            except:
#                right = ""                    
##            width = dimensions['width']
#            width = "304"
#            top = dimensions['top']
##            height = dimensions['height']
#            height = "228"
#            
#        return [left, width, top, height, right]
        
    def getFont(obj, key):
        """
        处理字体等信息
        """
        txt = obj.find(key)
        try:
            align = txt['align']
        except:
            align = ''
        color =txt['color']
        font =txt['family']
        size =txt['size']
        return [align, color, font, size] 

    def getCSS(obj, area):
        """
        返回CSS
        """
        css = ""
        if area not in ("question", "answer"):
            left, width, top, height, right = getDimensions(obj)
            setRight = ""
            if right != "":
                setRight = " right: " + right + "px;"
            css = """div.%s\n{\noverflow: auto; position: absolute; left: %spx;%s width: %spx; top: %spx; height: %spx; """\
                  """z-index: 30;  padding-left: 0px;  padding-right: 0px;"""\
                  """  padding-top: 0px;  padding-bottom: 0px;""" % (area, left, setRight, width, top, height)
            
        if area in ("area0", "area6", "area7"):
            css += "\n}\n"
            
        elif area in ("area2", "area4", "area5"):
            align, color, font, size = getFont(obj, "text")
            css += """text-align: %s;  color: %s;  font-family: %s,Arial Unicode MS;  font-size: %spx;\n}\n""" % (align, color, font, size)                
        elif area in ("question", "answer"):
            #如果是question或answer,则不再用前面的内容,这里可以再加一个align
            align, color, font, size = getFont(obj, area)
            css = """div.%s, div.%s table, div.%s input\n{\n"""\
                  """text-align: %s; color: %s; font-family: Lucida Sans Unicode,%s,Arial Unicode MS; filter: alpha(opacity=0);font-size: %spx;\n}\n""" % (area, area, area, align, color, font, size)
        return css
        
    resolution = soup.find('resolution', width="512")
    if resolution:
        content = resolution.contents
        soup_0 = BeautifulSoup(str(content))
        css = ''            
        css += getCSS(soup_0.primary, "area0")
        css += getCSS(soup_0.command, "area2")
        css += getCSS(soup_0.lesson, "area4")
        css += getCSS(soup_0.chapter, "area5")
        css += getCSS(soup_0.find('media-question'), "area6")            
        css += getCSS(soup_0.find('media-answer'), "area7")
        css += """div.area8\n{\n  overflow: hidden;  position: absolute;  left: 0px;  width: 361px;  top: 0px;  height: 271px; """\
                  """z-index: 10;  padding-left: 0px;  padding-right: 0px;  padding-top: 0px;  padding-bottom: 0px;\n}\n"""
        css += getCSS(soup_0.find('fonts'), "question")
        css += getCSS(soup_0.find('fonts'), "answer")
        
        return css

def mergeTxt(conList):
    """
    将beautifulSoup处理过的列表拼合成文本;
    不能直接用join;
    """
    content = ""
    if conList:
        for txt in conList:
            content += str(txt)
    return content   

def getMediaName(path, id, suffix, extList):
    """
    利用传来的路径/ID和后缀,拼出文件名;
    注意,不带扩展名;
    """
    file = path + getId(id) + suffix
    ext = getExt(file, extList)
    if ext:
        return  file + ext

def getExt(file, extList):
    """
    通过文件检验获取扩展名;
    用于实时预览项目/图片预览项目校验音频/图片文件名;
    """
    for ext in extList:                
        if QtCore.QFile.exists(file + ext):
            return ext
            break

def gotoQASection(mw, item):
    '''将当前item内容取出,放到QA区'''
    itemId, type = item.data(0, 32)
    itemFile = getItemFile(itemId)
    content = readFile(mw, itemFile, True)
#    soup =  BeautifulSoup(content)
#    question = GetElemText(soup.find("question"), "contents")
#    answer = GetElemText(soup.find("answer"), "contents")
    question = re.findall('<question>(.*?)</question>', content, re.S)
    if question:
        mw.ui.questionTE.setPlainText(question[0])
#        print(question[0])
#    xml = QtCore.QXmlStreamReader()
#    xml.addData(content)
#    while not xml.atEnd():
#        xml.readNext()
#        if xml.name() == "question":
#            question = xml.readElementText()
#            xml.clear()
#            break
    answer = re.findall('<answer>(.*?)</answer>', content, re.S)
    if answer:
        mw.ui.answerTE.setPlainText(answer[0])
    return itemFile

def dbToQASection(mw, item):
    '''将数据库当前item内容取出,放到QA区'''
    itemId, type = item.data(0, 32)
    courseId = Prefs.getCourse("colCourseId")
    sqlExp = """SELECT Question, Answer, Data FROM ITEMS WHERE CourseId = '%s' AND PageNum = '%s'""" % (courseId, itemId)
    result = execSql(mw, sqlExp, "one")
    if result:
        question, answer, data = result
        mw.ui.questionTE.setPlainText(question)
        mw.ui.answerTE.setPlainText(answer)
        return data
    
def sqliteEscape(keyWord):
    '''对关键词进行转义，以便进行sqlite数据库操作'''
    keyWord = keyWord.replace("/", "//")
    keyWord = keyWord.replace("'", "''")
#    keyWord = keyWord.replace("\"", "\"\"")#双引号不需要转义，但sql语句中字符串必须用单引号括起
    keyWord = keyWord.replace("[", "/[")
    keyWord = keyWord.replace("]", "/]")
    keyWord = keyWord.replace("%", "/%")
    keyWord = keyWord.replace("&","/&")
    keyWord = keyWord.replace("_", "/_")
    keyWord = keyWord.replace("(", "/(")
    keyWord = keyWord.replace(")", "/)")
    return keyWord

################错误处理#####################
def warn(mw, msg):
    SMMessageBox.critical(mw,
        mw.trUtf8("发现错误"),
        mw.trUtf8(
        '''<p>%s!</p>''' % msg))   
