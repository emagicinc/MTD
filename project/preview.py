#!/usr/bin/env python
from PyQt4 import QtCore, QtGui
import re
import queue
from bs4 import BeautifulSoup
import random
import sys
import os
import shutil
from PIL import Image#处理图片尺寸
#from PyQt4.QtWebKit import QWebSettings
#import urllib.request, urllib.parse, urllib.error
#from collections import OrderedDict
#import PixmapCache
#import SMMessageBox
#from util.commonDlg import *
#from util.SMApplication import smApp
from util.common import ReadItemFile, GetPakFile, SavePic, ParseItem, copyFile, getFileInfo, getBgImg, \
    getTmpFile, readFile, getMediaName, getId, mergeTxt, parseTemplate
#from UI.ui_customDict import Ui_CustomDict
#from UI.ui_preview import Ui_PreviewDlg

#from util import SMMessageBox
#from .dict import Dict
#import sqlite3
#from .exerciseDlg import *
#from .exerciseDlg import *

#try:
#    from PyQt4.phonon import Phonon
#except:
#    pass
#except ImportError:
#    app = QtGui.QApplication(sys.argv)
#    QtGui.QMessageBox.critical(None, "Music Player",
#            "Your Qt installation does not have Phonon support.",
#            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
#            QtGui.QMessageBox.NoButton)
#    sys.exit(1)
#    
#from project.jquery_rc import *
#import .jquery_rc

#try:
#    import jquery_rc3
#except ImportError:
#    import jquery_rc2

def RenderItem(mw, data):
    '''将传入的页面内容处理成html格式并返回'''
#    
#    outputStream(mw, "./1.txt", data) 
    content = None
    itemId = mw.itemId
    if mw.ui.modeBtn2.isChecked():
        itemId = mw.editItemId
    paramList = ParseItem(data, itemId)#common中调用
    qTxt = paramList[4]
    if qTxt:
        content = getHtmlContent(mw, paramList)
    else:
        content = getEmptyPage(mw)
    autoPlay(mw, "audioQ")  
#    from util.common import outputStream
#    outputStream(mw, "./test.htm", content)    
    '''输出语句要去除;'''
    return content

def autoPlay(mw, type):
    '''自动播放音频,type为audioQ或audioA'''
    file =  mw.PreviewDict.get(type)
    mw.playAudio(file)
    
def getHtmlContent(mw, paramList):
    """
    根据传来的参数获取实时预览页面的内容;
    核心程序
    """
    def getAudioFile(qa):
        '''生成音频文件,并返回文件名'''
        audioFile = getSfxFile(mw, coursePath, itemId, None, qa)
        if QtCore.QFile.exists(audioFile):
            copyFile(audioFile, """./template/temp/media/%s%s.mp3""" % (getId(itemId), qa))
        return """temp/media/%s%s.mp3""" % (getId(itemId), qa)            

    def getAudioTxt(area, file, suffix):
        '''根据参数返回音频区文本'''
        txt = ""
        if os.path.exists("""./template/%s""" % file):
            txt = """<DIV id=area%s class=area%s><IMG onclick="python.alert('%s' + python.message());" """\
            """ onmouseup="sfxMouseOver('player%s', 18);" id=player%s class=sfx1L "onmouseover="sfxMouseOver('player%s', 18);"""\
            """ onmouseout="sfxMouseOut('player%s'); onmousedown="sfxMouseDown2('player%s', 18, 14, event);" """\
            """ style="BACKGROUND-IMAGE: url(api/player1.png)">\n</DIV>""" % \
            (area, area, file, suffix, suffix, suffix, suffix, suffix)

#        if os.path.exists("""./template/%s""" % file):
#            txt = """<DIV id=area%s class=area%s><IMG onclick="python.alert('%s' + python.message());" """\
#            """ onmouseup="sfxMouseOver('player%s', 26);" id=player%s class=sfx1L "onmouseover="sfxMouseOver('player%s', 26);"""\
#            """ onmouseout="sfxMouseOut('player%s'); onmousedown="sfxMouseDown2('player%s', 26, 18, event);" """\
#            """ style="BACKGROUND-IMAGE: url(api/player1.png)">\n</DIV>""" % \
#            (area, area, file, suffix, suffix, suffix, suffix, suffix)
        return txt
    mw.PreviewDict["audioQ"] = ''
    mw.PreviewDict["audioA"] = ''
    mw.answer = None#此处要考虑转为mw变量
    mw.hintCount = 0#提示题型数量,每次载入时初始化
    courseName, itemId, chapTit, quTit, qTxt, aTxt, tmpId, bgImgId, audioQ, audioA, coursePath = paramList
    question, questionCheck = parseExType(mw, itemId, qTxt, coursePath)#answerTxt用在检查答案时对内容的转换
    answer = ""
    if aTxt:
        answer, answerCheck = parseExType(mw, itemId, aTxt, coursePath)
    basePath = getFileInfo("fullPath", "./template/")
    head = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n"""\
           """<HTML xmlns="http://www.w3.org/1999/xhtml">\n<HEAD><TITLE>%s</TITLE>\n""" % (courseName + "(" + str(itemId) + ")")
    head += """<META content="text/html; charset=utf-8" http-equiv=Content-Type>\n"""\
           """<META content=progid:DXImageTransform.Microsoft.GradientWipe(GradientSize=1.0,WipeStyle=0,Duration=0.5,Motion=forward) """\
           """http-equiv=Page-Exit>\n<META content=IE=7 http-equiv=X-UA-Compatible>\n<BASE href="file:///%s/">\n""" % basePath
    #取模板
    bgImg = ""
    if bgImgId:
        bgImg = getBgImg(bgImgId)
    tmpContent = parseTemplate(mw, tmpId, coursePath)
    head += """<STYLE type=text/css>\nbody\n{\n  margin: 0px 0px 0px 0px;  padding: 0px 0px 0px 0px;  background-color: #F0F0F0;\n}\n"""\
        """div.template\n{\n  position: absolute;  left: 0px;  top: 0px;  width: 361px;  height: 271px;  background-color: #FFFFFF;  """\
        """background-image: url('%s'); background-size: 361px auto; background-position: left top;  background-repeat: no-repeat;  text-align: left;  z-index: 0;\n}\n"""\
        """%s</STYLE>\n"""% (bgImg, tmpContent)
#    head += """<STYLE type=text/css>\nbody\n{\n  margin: 0px 0px 0px 0px;  padding: 0px 0px 0px 0px;  background-color: #F0F0F0;\n}\n"""\
#        """div.template\n{\n  position: absolute;  left: 0px;  top: 0px;  width: 1024px;  height: 768px;  background-color: #FFFFFF;  """\
#        """background-image: url('%s');  background-position: left top;  background-repeat: no-repeat;  text-align: left;  z-index: 0;\n}\n"""\
#        """%s</STYLE>\n"""% (bgImg, tmpContent)        
    cssFile = getTmpFile(tmpId, "css", coursePath)#模板中带的CSS文件
    script = readFile(mw, "./template/api/learn.js", "getData")
    ###处理排序题/匹配题的脚本
    globalLoad = """function globalLoad()\n{\n"""
    dragNum = mw.PreviewDict['dragNum']
    if len(mw.orderDict) > 0:
        for k, v in mw.orderDict.items():
            globalLoad += """rlLoad('%s', '%s');\n""" % (k, v)
    if dragNum:
        if dragNum > 0:
            dropSign = "__________"
            for i in range(dragNum):
                globalLoad += """dpInitDrop(%s, "%s");\n""" % (i, dropSign)
            globalLoad += """dpInitDragDrop();\n"""
    globalLoad += """}\n</SCRIPT>\n"""
    head += """<script src="api/html5media.min.js"></script>\n<link rel="stylesheet" href="api/styles.css"/>\n"""\
        """<LINK rel=stylesheet type=text/css href="api/learn.css">\n"""\
        """<LINK rel=stylesheet type=text/css href="%s">\n%s%s""" % (cssFile, script, globalLoad)
    #问题区和答案区
    head += """</HEAD>\n"""\
        """<BODY ondragstart="return false;" onmouseup=globalMouseUp(); onload=globalLoad(); onselectstart="return false;" onmousemove=globalMouseMove();>\n"""\
        """<DIV id=template class=template>\n<DIV id=area0 class=area0>\n"""
    bodyQ = """<DIV id=question class=question>\n%s\n</DIV>\n<DIV id=answer class=answer></DIV></DIV>\n<DIV id=area0_2 class=area0_2></DIV>\n""" % question
    bodyA = """<DIV id=question class=question>\n%s\n</DIV>\n<DIV id=answer class=answer>%s&nbsp;</DIV></DIV>\n<DIV id=area0_2 class=area0_2></DIV>\n""" % (questionCheck, answer)
    titles = """<DIV id=area2 class=area2>%s</DIV>\n<DIV id=area5 class=area5>%s</DIV>\n"""\
            """<DIV id=area4 class=area4>%s</DIV>\n""" % (quTit, chapTit, courseName)
    #处理音频
    audioTxtQ = ""
    audioTxtA = ""
    if audioQ:
        audioQFile = getAudioFile("q")
        mw.PreviewDict["audioQ"] = audioQFile
        audioTxtQ += getAudioTxt("6", audioQFile, "q")
    if audioA:
        audioAFile = getAudioFile("a")
        mw.PreviewDict["audioA"] = audioAFile
        audioTxtA += getAudioTxt("7", audioAFile, "a")
    #尾部
    hintScript = readFile(mw, "./template/api/mouse.js", "getData")
    foot = """</DIV>\n%s</BODY>\n</HTML>\n""" % hintScript
    mw.orderDict = {}#重置
    mw.answer = head + bodyA + titles + audioTxtA + foot#此处要考虑转为mw变量
    return head + bodyQ + titles + audioTxtQ + foot
    
def getEmptyPage(mw):
    '''生成一个空白页面'''
    basePath = getFileInfo("fullPath", "./template/")
    content = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n"""\
           """<HTML xmlns="http://www.w3.org/1999/xhtml">\n<HEAD><TITLE></TITLE>\n"""
    content += """<META content="text/html; charset=utf-8" http-equiv=Content-Type>\n"""\
           """<META content=progid:DXImageTransform.Microsoft.GradientWipe(GradientSize=1.0,WipeStyle=0,Duration=0.5,Motion=forward) """\
           """http-equiv=Page-Exit>\n<META content=IE=7 http-equiv=X-UA-Compatible>\n<BASE href="file:///%s/">\n""" % basePath
    #取模板n
    bgImg = getBgImg("123")
    tmpContent = parseTemplate(mw, "99996")
    content += """<STYLE type=text/css>\nbody\n{\n  margin: 0px 0px 0px 0px;  padding: 0px 0px 0px 0px;  background-color: #F0F0F0;\n}\n"""\
        """div.template\n{\n  position: absolute;  left: 0px;  top: 0px;  width: 361px;  height: 271px;  background-color: #FFFFFF;  """\
        """background-image: url('%s');  background-size: 361px auto; background-position: left top;  background-repeat: no-repeat;  text-align: left;  z-index: 0;\n}\n"""\
        """%s</STYLE>\n"""% (bgImg, tmpContent)
#    content += """<STYLE type=text/css>\nbody\n{\n  margin: 0px 0px 0px 0px;  padding: 0px 0px 0px 0px;  background-color: #F0F0F0;\n}\n"""\
#        """div.template\n{\n  position: absolute;  left: 0px;  top: 0px;  width: 1024px;  height: 768px;  background-color: #FFFFFF;  """\
#        """background-image: url('%s');  background-position: left top;  background-repeat: no-repeat;  text-align: left;  z-index: 0;\n}\n"""\
#        """%s</STYLE>\n"""% (bgImg, tmpContent)        
    cssFile = getTmpFile("99996", "css")#模板中带的CSS文件
    content += """<script src="api/html5media.min.js"></script>\n<link rel="stylesheet" href="media/styles.css"/>\n"""\
        """<LINK rel=stylesheet type=text/css href="learn.css">\n"""\
        """<LINK rel=stylesheet type=text/css href="%s">\n""" % cssFile
    #问题区和答案区
    content += """</HEAD>\n"""\
        """<BODY ondragstart="return false;" onmouseup=globalMouseUp(); onload=globalLoad(); onselectstart="return false;" onmousemove=globalMouseMove();>\n"""\
        """<DIV id=template class=template>\n<DIV id=area0 class=area0>\n<DIV id=question class=question>\n"""\
        """<h1>%s%s</h1>\n</DIV>\n"""\
        """<DIV id=answer class=answer><h1>%s</h1></DIV></DIV>\n<DIV id=area0_2 class=area0_2></DIV>\n""" % ("&nbsp;" * 15, "亲,这一页木有内容哦!", "")
    content += """<DIV id=area2 class=area2>%s</DIV>\n<DIV id=area5 class=area5>%s</DIV>\n"""\
            """<DIV id=area4 class=area4>%s</DIV>\n""" % ("", "", "SuperMemo课程编辑器")
    content += """</DIV>\n</BODY>\n</HTML>\n"""
    return content
            
################################################
###                题型处理相关              ### 
################################################  
def spellpad(num, tag, itemId):
    '''拼写题处理'''
    sTxt = ""
    aTxt = ""
    for i in tag.contents:
        if i.name == "spellpad":
            sTxt += """<SPAN class=spFrameQuestion><INPUT id=spell%s onchange=spStore(this); class=spInputQuestion """\
                """onkeyup=spStore(this);onselect=spStore(this); onclick=spStore(this); value='' size='' ></SPAN>"""\
                % (str(num))
            aTxt += """[<SPAN class=spFrameWrong>(no answer)</SPAN> | <SPAN class=spFrameCorrect>%s</SPAN>]""" % i["correct"]
        else:
            sTxt += str(i)
            aTxt += str(i)
    return ("""<big>%s</big>""" % sTxt, aTxt)
    
def hint(mw, num, tag):
    '''提示题型处理'''
    sTxt = ""
    tranTxt = ""
    id = mw.hintCount
    for i in tag.contents:
        if i.name == "sentence":
            sTxt = mergeTxt(i.contents)
        if i.name == "translation":
            tranTxt = mergeTxt(i.contents)                
#            print(i.name)
    content = """<div class="wrap">\n<div id="borderdiv"></div>\n<div id="sentence%s">%s&nbsp;&nbsp;</div>""" % (id, sTxt)
    content += """<div class="translation" id="translation%s" style="background:#399">"""\
        """<font color="white">%s</font></div>\n</div>""" % (id, tranTxt)
    mw.hintCount += 1
    return (content, content)  
    
def getImgFile(path, itemId, quotId, suffix, altSuffix):
    """
    获取三个文件名;
    suffix是指后缀,并非扩展名;
    所有文件暂不指定扩展名,要通过文件校验来获取扩展名;
    如果不存在文件,应尝试从smpak文件中提取;
    """
    mediaPath = path + "/media/"
    extList = [".png", ".jpg", ".gif", ".bmp", ".media"]
    imgFile = getMediaName(mediaPath, itemId, suffix, extList)
    quotFile = None
    altFile = None
    if quotId:
        quotFile = getMediaName(mediaPath, quotId, suffix, extList)
        altFile = getMediaName(mediaPath, quotId, altSuffix , extList)
    else:
        if altSuffix:
            altFile = getMediaName(mediaPath, itemId, altSuffix, extList)
    return [imgFile, altFile, quotFile]

def getPakImg(mw, itemId, quotId, suffix, altSuffix):
    '''获取课程包中的媒体文件,mediaPath相当于媒体文件的前缀'''
    def getImg(file):
        '''生成文件,返回全路径的文件名'''
        if file:
            if not os.path.exists(file):
                mw.smpak.unpack("""./template/temp/""", file)
            return """%s/media/%s""" % (basePath, file[6:])
    mediaPath = "media/"
    extList = [".png", ".jpg", ".gif", ".bmp", ".media"]
    imgFile = getMediaName(mediaPath, itemId, suffix, extList)
    quotFile = None
    if quotId:
        quotFile = getMediaName(mediaPath, quotId, suffix, extList)
        altFile = getMediaName(mediaPath, quotId, altSuffix, extList)
    else:
        altFile = getMediaName(mediaPath, itemId, altSuffix, extList)
    basePath = QtCore.QFileInfo("./template/temp").absoluteFilePath()
    if not os.path.exists(basePath):
        os.mkdir(basePath)
    return([getImg(imgFile), getImg(altFile), getImg(quotFile)])
        
def getGfxInfo(mw, path, itemId, quotId, suffix, altSuffix, scale):
    """
    根据传来的页面ID/引用ID/俩后缀/缩放比例返回信息;
    返回文件名/alt文件名/quot文件名/宽/高
    """
    imgFile = None
    quotFile = None
    altFile = None
    width = None
    height = None
    def getSize(file, scale):
        """
        根据缩放比例计算图片宽和高
        """
        if QtCore.QFile.exists(file):
            im = Image.open(file)
            (w, h) = im.size #read image size
#                image = QtGui.QImage(fileName)
#                return str(int(int(size) * x / y))
#                img = QtGui.QImage(file)
            width =  int(w) * 1024 / int(scale)
            height = int(h) * 1024 / int(scale)
            return [int(width), int(height)]
        else:
            return [320, 320]
#    if self.type == "smpak":
#        imgFile, altFile, quotFile = getPakImg(mw, itemId, quotId, suffix, altSuffix)
#    else:
    imgFile, altFile, quotFile = getImgFile(path, itemId, quotId, suffix, altSuffix)
    if scale:
        if quotFile:
            width, height = getSize(quotFile, scale)
        elif imgFile:
            width, height = getSize(imgFile, scale)
    return [imgFile, altFile, quotFile, width, height]
    
def gfx(mw, num, tag, itemId, coursePath):
    '''图片题型处理,attrDict的写法可以优化,直接用get,至少可省一半行数''' 
    attrDict = tag.attrs  
    quotId = attrDict.get("item-id")
    float = attrDict.get("float")
    altSuffix = attrDict.get("altfile")
    suffix = attrDict.get("file")
    scale  = attrDict.get("scale-base")
    hspace = attrDict.get("hspace")
    vspace = attrDict.get("vspace")
    border = attrDict.get("border")

    imgFile, altFile, quotFile, width, height = getGfxInfo(mw, coursePath, itemId, quotId, suffix, altSuffix, scale)
    content = """<IMG style=" """
    if float:
        content += """FLOAT:%s; """ % float
    if hspace:
        content += """MARGIN-LEFT: %spx; MARGIN-RIGHT: %spx; """ % (hspace, hspace)
    if vspace:
        content += """MARGIN-TOP: %spx; MARGIN-BOTTOM: %spx; """ % (vspace, vspace)
    content += """ " id=image%s """ % num
    if altFile:
        content += """class=gfxLink onclick="window.external.PreviewImage('file:///%s'); " alt="点击这里预览完整页面。" """ % altFile
    if border:
        content += """border:%s; """ % border
    if quotFile:
        content += """src="file:///%s"; """ % quotFile
    else:
        content += """src="file:///%s"; """ % imgFile
    if width:
        content += """width="%s" """ % width
    if height:
        content += """height="%s" """ % height
    content += """>"""
    return  (content, content)

def getSfxFile(mw, path, itemId, quotId, suffix):
    """
    根据传来的页面ID/引用ID/后缀获取音频文件信息;
    调用和不调用的只取一个;
    """
    '''basePath应该不放在这里创建!在预览一开始的时候即检查'''
    def getAudio(file):
        '''生成文件,返回全路径的文件名'''
        basePath = QtCore.QFileInfo("./template/temp").absoluteFilePath()
        if not os.path.exists(basePath):
            os.mkdir(basePath)
        if file:
            if not os.path.exists(file):
                try:
                    mw.smpak.unpack("""./template/temp/""", file)
                except:
                    pass
            return """%s/media/%s""" % (basePath, file[6:])
    sfxFile = None
    mediaPath = path + "/media/"
    extList = [".mp3", ".wav", ".wma", ".media"]
    if quotId:
        itemId = quotId
    sfxFile = getMediaName(mediaPath, itemId, suffix, extList)

    return sfxFile
    
def sfx(mw, num, tag, itemId, coursePath):
    """
    音频题型处理
    """
    attrDict = tag.attrs
    quotId = attrDict.get("item-id")
    suffix = attrDict.get("file")
    media = ""
    sfxFile = getSfxFile(mw, coursePath, itemId, quotId, suffix)
    if quotId:#当有引用ID时,则使用引用ID
        itemId = getId(quotId)
    if sfxFile:
        if QtCore.QFile.exists(sfxFile):
            copyFile(sfxFile, './template/temp/media/%s%s.mp3' % (getId(itemId), suffix))
    file = "temp/media/%s%s.mp3" %  (getId(itemId), suffix)
#        content = """<audio class="audio" src="%s" controls preload loop></audio>\n""" % media
    content = ""
    if os.path.exists("""./template/%s""" % file):
        content = """<IMG onclick="python.alert('%s' + python.message());"  onmouseup="sfxMouseOver('player%s', 18);" id=player%s class=sfx1L """\
            """onmouseover="sfxMouseOver('player%s', 18); onmouseout="sfxMouseOut('player%s'); onmousedown="sfxMouseDown2('player%s', 18, 14, event);" """\
            """ style="BACKGROUND-IMAGE: url(api/player1.png)">""" % (file, num, num, num, num, num)
    return (content, content)

def radio(mw, num, tag, itemId, coursePath):
    '''单选题处理;131125用新方法,传进来的是tag'''
    '''注意看下代码还能否精简'''
    def getTxt(tag):
        '''处理题肢和答案'''
        if tag.name == "gfx":
            txt = gfx(mw, num, tag, itemId, coursePath)[0]
        else:
            txt = str(tag)
        return txt
        
    attrDict = tag.attrs
    style = None
    if "orientation" in attrDict.keys():
        style = attrDict["orientation"]
    if "display" in attrDict.keys():
        style = attrDict["display"]
    optionList = tag.findAll({'option':True}, {'correct':None})
    keyList = tag.findAll({'option':True}, {'correct':True})
    
    trAllF = ''
    trAllB = ''
    trF = ''
    trB = ''
    br = ''
    results = []#用于出随机选择题
    #只有水平样式才需要加总的TR,其余都用分TR
    if style == "horizontal":
        trAllF = "<TR>\n"
        trAllB = "</TR>"
        br = '<br/>'
    else:
        trF = "<TR>\n"
        trB = "</TR>"
    content = """%s<INPUT id=rd%s value=-1 type=hidden><TABLE style="DISPLAY: inline-block;" class=cbNoBorder """\
              """ cellSpacing=2 cellPadding=2>\n<TBODY>\n%s""" % (br, num, trAllF)
#    basePath = getFileInfo("fullPath", "./template/")
    if keyList:
        for k, key in enumerate(keyList):
            id = """rd%s_%s""" % (num, str(k))
            for tag in key.contents:
                keyTxt = getTxt(tag)
            results.append("""%s<TD>\n<DIV style="BACKGROUND-IMAGE: url(api/radio.png)" id=%s class=rdGadget """\
                """onmouseover="rdMouseOver('%s');" onmouseout="rdMouseOut('%s');" onclick="rdClick('%s');"></DIV></TD>\n"""\
                """<TD class=cbQuestion><SPAN onmouseover="rdMouseOver('%s');" onmouseout="rdMouseOut('%s');" onclick="rdClick('%s');">"""\
                """%s</SPAN></TD>%s\n""" % (trF, id, id, id, id, id, id, id, keyTxt, trB))
#                content += """""" % 
    m = k
    if optionList:
        for option in optionList:
            m += 1 
            for tag in option.contents:
                optionTxt = getTxt(tag)
            id = """rd%s_%s""" % (num, str(m))
            results.append("""%s<TD>\n<DIV style="BACKGROUND-IMAGE: url(api/radio.png)" id=%s class=rdGadget """\
                """ onmouseover="rdMouseOver('%s');" onmouseout="rdMouseOut('%s');" onclick="rdClick('%s');"></DIV></TD>\n"""\
                """<TD class=cbQuestion><SPAN onmouseover="rdMouseOver('%s');" onmouseout="rdMouseOut('%s');" onclick="rdClick('%s');">"""\
                """%s</SPAN></TD>%s\n""" % (trF, id, id, id, id, id, id, id, optionTxt, trB))
#                content += """""" % 
            
    random.shuffle(results)
    data = """%s%s%s</TBODY></TABLE>\n""" % (content, " ".join(results), trAllB)
    result = ""
    for i in results:
        if re.search("""rd%s_0""" % num, i):
            #注意为了简化操作起见,不删除onmouseout,onclick,onmouseover等内容
            result += re.sub(r'<TD class=cbQuestion', r'<TD class=cbGoodAnswer', i)
        else:
            result += i
    aTxt = """%s%s%s</TBODY></TABLE>\n""" % (content, result, trAllB)

    return (data, aTxt)

def checkbox(mw, num, tag, itemId):
    """
    多选题处理;
    """
#    print("check")
    def getTxt(tag):
        '''处理题肢和答案'''
        if tag.name == "gfx":
            txt = gfx(mw, num, tag, itemId, coursePath)[0]
        else:
            txt = str(tag)
        return txt
    attrDict = tag.attrs
    style = None
    if "orientation" in attrDict.keys():
        style = attrDict["orientation"]
    if "display" in attrDict.keys():
        style = attrDict["display"]
    optionList = tag.findAll({'option':True}, {'correct':None})
    keyList = tag.findAll({'option':True}, {'correct':True})
    
    results = []#用于出随机选择题
    trAllF = ''
    trAllB = ''
    trF = ''
    trB = ''
    br = ''
    #只有水平样式才需要加总的TR,其余都用分TR
    if style == "horizontal":
        trAllF = "<TR>\n"
        trAllB = "</TR>"
        br = '<br/>'
    else:
        trF = "<TR>\n"
        trB = "</TR>"
    content = """%s<INPUT id=cb%s value=0 type=hidden><TABLE style="DISPLAY: inline-block;" class=cbNoBorder """\
              """ cellSpacing=2 cellPadding=2>\n<TBODY>\n%s""" % (br, num, trAllF)
    results = []#存放问题和答案,用于随机出选择题
    keyIds = []
    if keyList:
        for k, key in enumerate(keyList):
            id = """cb%s_%s""" % (num, str(k))
            for tag in key.contents:
                keyTxt = getTxt(tag)
                keyIds.append(k)
            results.append("""%s<TD>\n<DIV style="BACKGROUND-IMAGE: url(api/checkbox.png)" id=%s class=cbGadget """\
                """onmouseover="cbMouseOver('%s');" onmouseout="cbMouseOut('%s');" onclick="cbClick('%s');"></DIV></TD>\n"""\
                """<TD class=cbQuestion><SPAN onmouseover="cbMouseOver('%s');" onmouseout="cbMouseOut('%s');" onclick="cbClick('%s');">"""\
                """%s</SPAN></TD>%s\n""" % (trF, id, id, id, id, id, id, id, keyTxt, trB))
    m = k
    if optionList:
        for option in optionList:
            for tag in option.contents:
                optionTxt = getTxt(tag)
            m += 1 
            id = """cb%s_%s""" % (num, str(m))
            results.append("""%s<TD>\n<DIV style="BACKGROUND-IMAGE: url(api/checkbox.png)" id=%s class=cbGadget """\
                """ onmouseover="cbMouseOver('%s');" onmouseout="cbMouseOut('%s');" onclick="cbClick('%s');"></DIV></TD>\n"""\
                """<TD class=cbQuestion><SPAN onmouseover="cbMouseOver('%s');" onmouseout="cbMouseOut('%s');" onclick="cbClick('%s');">"""\
                """%s</TD>%s\n""" % (trF, id, id, id, id, id, id, id, optionTxt, trB))
    #设置答案列表
    answers = []
    for id, txt in enumerate(results):
        if id < len(keyIds):#答案总在前几个
#            if re.search("""cb%s_%s""" % (num, j), txt):
            #注意为了简化操作起见,不删除onmouseout,onclick,onmouseover等内容
            answers.append(re.sub(r'<TD class=cbQuestion', r'<TD class=cbGoodAnswer', txt))
        else:
            answers.append(txt)
    ranges = list(range(len(results)))
    randomList = random.sample(ranges, len(ranges))
    qTxt = ""
    aTxt = ""
    for n in randomList:
        qTxt += results[n]
        aTxt += answers[n]
    random.shuffle(results)
    data = """%s%s%s</TBODY></TABLE>\n""" % (content, qTxt, trAllB)
    aTxt = """%s%s%s</TBODY></TABLE>\n""" % (content, aTxt, trAllB)
    return (data, aTxt)

def droplist(num, tag, itemId):
    """
    处理下拉选择题
    """
#        soup = BeautifulSoup(data)
    optionList = tag.findAll({'option':True})
    keyList = tag.findAll({'option':True}, {'correct':True})
    content = ""
    results = []#用于出随机选择题
    if keyList:
        answer = mergeTxt(optionList[0].contents)          
    if optionList:
        content += """<INPUT id=dd%s_res value=-1 type=hidden><SPAN id=dd%s class=ddBox """\
            """onmouseover="ddMouseOverOut('dd%s_a', 'api/droplist2.png')" onmouseout="ddMouseOverOut('dd%s_a', 'api/droplist.png')" """\
            """onclick="ddMouseClick('dd%s', 'dd%s_answers', 361)">""" % (num, num, num, num, num, num)
        content += """<IMG id=dd%s_a align=absBottom src="api/droplist.png"><SPAN id=dd%s_f class=ddText> """\
            """<SPAN style="VISIBILITY: hidden">%s</SPAN></SPAN></SPAN><DIV style="DISPLAY: none" id=dd%s_answers>\n"""\
            """<TABLE cellSpacing=0 cellPadding=2>\n<TBODY>\n""" % (num, num, answer, num)             
        for k, option in enumerate(optionList):
            optionTxt = mergeTxt(option.contents)
            results.append("""<TR>\n<TD id=dd%s_a%s onmouseover=ddHighLight(this); onmouseout=ddDownLight(this); """\
                """onclick="ddSelect(this, 'dd%s');">%s</TD></TR>""" % (num, str(k), num, optionTxt))

        random.shuffle(results)
        data = """%s%s</TBODY></TABLE></DIV>\n""" % (content, " ".join(results))
        aTxt = """ [<SPAN class=spFrameWrong>(no answer)</SPAN> | <SPAN class=spFrameCorrect>%s</SPAN>]""" % answer
        return (data, aTxt)

def dragdrop(mw, num, tag, itemId, coursePath):
    """
    匹配题处理;
    """
    def getTxt(tag):
        '''处理题肢和答案'''
        if tag.name == "sfx":#为呈现按钮点击效果,将第一个参数作为音频播放ID
            attrs = tag.attrs
            id = attrs.get("item-id")
            txt = sfx(mw, id, tag, itemId, coursePath)[0]
        else:
            txt = str(tag)
        return txt
    attrDict = tag.attrs
    style = None
    dropsign = None
    if "orientation" in attrDict.keys():
        style = attrDict["orientation"]
    if "dropsign" in attrDict.keys():
        dropsize = attrDict["dropsign"]
        dropsign = int(dropsize) * "_"
    dragList = tag.findAll({'option':True})
    mw.PreviewDict['dragNum'] = len(dragList)
    dropList = tag.findAll({'drop-text':True})
    trF = ''
    trB = ''
    br = '<br/>'
    if style == "horizontal":
        trF = '<TR>\n'
        trB = '</TR>\n'
        br = ''
        
    content = """<TABLE style="WIDTH: 95%" border=0 cellPadding=5>\n<TBODY>\n<TR>\n"""\
        """<TD style="LINE-HEIGHT: 150%; HEIGHT: 25%; CURSOR: default" vAlign=top>"""
        
    for k, option in enumerate(dragList):
        dragTxt = mergeTxt(option.contents)
        content += """<INPUT id=dg%s_id value=dg%s type=hidden><SPAN style="MARGIN-RIGHT: 5px">\n"""\
            """[<SPAN id=dg%s class=dpDragDefault onmouseover=dpActivateDrag(this); """\
            """onmouseout=dpDeActivateDrag(this); onmousedown="return dpStartDrag(this, event);">"""\
            """%s</SPAN>]</SPAN>%s\n""" % (str(k), str(k), str(k), dragTxt, br)
    content += """</TD>%s%s<TD style="LINE-HEIGHT: 150%%" vAlign=top>\n""" % (trB, trF)
    
    if dropList:
        dropTxt = ""
        for option in dropList:
            for tag in option.contents:
                dropTxt += getTxt(tag)
        data = re.sub(r'\[(.*?)\]', r'<INPUT id=dp' + r'\1' +  r'_id type=hidden>\n<IMG style="DISPLAY: none; MARGIN-RIGHT: 5px" id=dp'\
            + r'\1' + r'_img onclick=dpReleaseDrop(this); align=middle src="api/drag.png"><SPAN id=dp' + r'\1'\
            + r' class=dpDropDefault>' + dropsign + '</SPAN>\n', dropTxt)
        content += """%s</TD></TR></TBODY></TABLE>\n""" % data

    aTxt = ""
    #开始制作答案
    for k, option in enumerate(dragList):
        dragTxt = mergeTxt(option.contents)
        dropTxt = re.sub(r'\[' + str(k) + '\]', r'<SPAN class=dpDropWrongAnswer>(no answer)</SPAN>'\
            + '| <INPUT id=dp0_0_id type=hidden><SPAN id=dp0_0 class=dpDropGoodAnswer>' + dragTxt + '</SPAN>', dropTxt)
    aTxt = dropTxt + "<br/>"
    return (content, aTxt)
    
def getOrderList(mw, num, tag):
    """
    获取随机的序号,用于排序题操作;
    此变量将用于头部脚本初始化;
    """
    optionList = tag.findAll({'option':True})
    orderList = list(range(len(optionList)))#这个只是序号
    random.shuffle(orderList)
    order = str(orderList).strip('[]')
    mw.PreviewDict['orderList'] = orderList
    mw.PreviewDict['optionList'] = optionList
    mw.PreviewDict['order'] = order
#        self.mw.PreviewDict['rlId'] = 'rl' + str(num)
    mw.orderDict['rl' + str(num)] = order
    
def order(mw, num, tag, itemId):
    """
    排序题处理;
    """        
    optionList = mw.PreviewDict['optionList']
    orderList = mw.PreviewDict['orderList']#这个只是序号
    order = mw.PreviewDict['order']
    width = 2
    #用width计算位置
    for k, option in enumerate(optionList):
        optionTxt = mergeTxt(option.contents)
        if optionTxt:
            optionTxt = optionTxt.strip(" ")
            optionTxt = optionTxt.replace("--", "-")
        optionList[k] = optionTxt#写回
        idx = orderList.index(k)
    widthList = [2]#开头空两px
    qList = []
    for n, i in enumerate(orderList):
        width = width + len(optionList[i]) * 13 + 2
        widthList.append(width)
        qList.append(optionList[i])
    content = """<DIV style="WIDTH: %spx; HEIGHT: 38px" id=rl%s_box class=reorderBox><INPUT id=rl%s value=%s type=hidden>\n""" % (width, num, num, order)
    answer = ""
    for k, txt in enumerate(optionList):
        idx = orderList.index(k)
        width = widthList[idx]
        content += """<DIV style="HEIGHT: 15px; LEFT: %spx" id=rl%s_%s onmouseup=rlMouseUp(true); """\
            """class=reorderObj onmouseover=rlMouseOver(this); onmouseout=rlMouseOut(this); """\
            """onmousedown="return rlMouseDown(this, event);">%s</DIV>\n""" % (width, num, str(k), txt)
    content += """</DIV>\n"""
    aTxt = """<DIV class=rlAnswer><SPAN class=rlWrongAnswer>%s</SPAN></DIV>\n"""\
        """<DIV class=rlAnswer><SPAN class=rlGoodAnswer>%s</SPAN></DIV><br/>""" % (" ".join(qList), " ".join(optionList))
    return (content, aTxt)

def selPh(num, tag, itemId):
    '''改错题处理;'''
    attrDict = tag.attrs
    style = "underline"
    if "mode" in attrDict.keys():
        style = "line-through"
    optionList = tag.findAll({'option':True})
    keyList = tag.findAll({'option':True}, {'correct':True})
    results = []
    content = """<INPUT id=ph%s value=0 type=hidden><SPAN class=phPhrase>\n""" % num
    m = 1
    if optionList:
        for option in optionList:
            if option in keyList:
                m = 0
            optionTxt = mergeTxt(option.contents)
            phId = """ph%s_%s""" % (num, m)
            results.append("""<A class=phPhrase id=%s onclick="phClick('%s', '%s');"""\
                """ return false;" href="#">%s</A>\n""" % (phId, phId, style, optionTxt))
            m += 1 

    data = """%s%s</SPAN>\n""" % (content, " ".join(results))
    result = ""
    for i in results:
        if re.search("""ph%s_0""" % num, i):
            #注意为了简化操作起见,不删除onmouseout,onclick,onmouseover等内容
            result += re.sub(r'<A class=phPhrase', r'<SPAN class=phGoodAnswer', i)
        else:
            result += re.sub(r'<A class=phPhrase', r'<SPAN class=phPhrase', i)
    aTxt = """%s%s</SPAN>\n""" % (content, result)
    
    return (data, aTxt)

def tf(num, tag, itemId):
    """
    是非题处理;
    """
    attrDict = tag.attrs
    tTxt = attrDict.get("true")
    fTxt = attrDict.get("false")
    key = attrDict.get("correct")
    tClass = "tfCorrect"
    fClass = "tfTrueFalse"
    if key == "false":
        tClass = "tfTrueFalse"
        fClass = "tfCorrect"
    content = """<INPUT id=tf%s value=-1 type=hidden>\n<TABLE class=tfTrueFalse cellSpacing=0 cellPadding=5>\n"""\
        """<TBODY>\n<TR>\n""" % num
    for k in range(2):
        tfId = """tf%s_%s""" % (num, k)
        data = """<DIV class=tfTrueFalse style="BACKGROUND-IMAGE: url(api/truefalse.png); BACKGROUND-POSITION: 0px 50%%" """\
            """id=%s onmouseover="tfOnMouseOver('%s');" onmouseout="tfOnMouseOut('%s');" """\
            """onclick="tfOnClick('%s');" div <></DIV></TD>\n""" % (tfId, tfId, tfId, tfId)
        if k == 0:
            content += """<TD>%s</TD><TD> %s""" % (tTxt, data)
        elif k == 1:
            content += """<TD>%s<TD>%s</TD>""" % (data, fTxt)
    content += """</TR></TBODY></TABLE>\n"""
    
    aTxt = """<TABLE class=tfTrueFalse cellSpacing=0 cellPadding=5>\n<TBODY>\n<TR>\n<TD>%s</TD>"""\
        """<TD>\n<DIV class=%s style="BACKGROUND-IMAGE: url(api/truefalse.png)"></DIV></TD>\n"""\
        """<TD><DIV class=%s style="BACKGROUND-IMAGE: url(api/truefalse.png)"></DIV></TD>\n"""\
        """<TD>%s</TD></TR></TBODY></TABLE>\n""" % (tTxt, tClass, fClass, fTxt)
    return (content, aTxt)

def parseExType(mw, itemId, tagList, coursePath):
    """
    对题型进行逆转换;
    """
    questionTxt = ''
    answerTxt = ''
    for num, tag in enumerate(tagList):
        data = str(tag)
        questionCheck = None
#            print(tag.name)
        if tag.name:
            if tag.name == "radio":#单选 已改
                data, questionCheck = radio(mw, num, tag, itemId, coursePath)
            elif tag.name == "checkbox":#多选 已改
                data, questionCheck = checkbox(mw, num, tag, itemId)
            elif tag.name == "droplist":#下拉选择 已改
                data, questionCheck = droplist(num, tag, itemId)
            elif tag.name == "drag-drop":#匹配 已改
                data, questionCheck = dragdrop(mw, num, tag, itemId, coursePath)
            elif tag.name == "ordering-list":#排序 已改
                getOrderList(mw, num, tag)
                data, questionCheck = order(mw, num, tag, itemId)
            elif tag.name == "select-phrases":#改错题 已改
                data, questionCheck = selPh(num, tag, itemId)
            elif tag.name == "true-false":#是非题 
                data, questionCheck = tf(num, tag, itemId)
            elif tag.name == "text":#提示题 已改
                data, questionCheck = hint(mw, num, tag)
            elif tag.name in ("big", "spellpad"):#拼写 已改
                data, questionCheck = spellpad(num, tag, itemId)
            elif tag.name == "gfx":#图片 已改
                data, questionCheck = gfx(mw, num, tag, itemId, coursePath)
            elif tag.name == "sfx":#音频 已改
                data, questionCheck = sfx(mw, num, tag, itemId, coursePath)
        if not questionCheck:#把非题型的内容取回来
            questionCheck = data
        questionTxt += data
        answerTxt += questionCheck
    return (questionTxt, answerTxt)
