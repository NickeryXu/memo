# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!
import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import sqlite3

# 按钮高度
BUTTON_HEIGHT = 30
# 按钮宽度
BUTTON_WIDTH = 30
# 标题栏高度
TITLE_HEIGHT = 30

import gc
import os
import sys
import traceback

this = os.path.abspath(os.path.dirname(__file__))
module = os.path.split(this)[0]
# print('sys.path.append("%s")' % module)
sys.path.append(module)
# for i, val in enumerate(sys.path):
#     print("[%s] %s" % (i + 1, val))


def delMEI():
    for index, path in enumerate(sys.path):
        basename = os.path.basename(path)
        if not basename.startswith("_MEI"):
            continue

        drive = os.path.splitdrive(path)[0]
        if "" == drive:
            path = os.getcwd() + "\\" + path
            path = path.replace("\\\\", "\\")

        if os.path.isdir(path):
            try:
                print("remove", path)
                os.remove(path)
            except:
                pass
            finally:
                break

# 生成资源文件目录访问路径
def resource_path(relative_path):
    base_path = os.path.dirname(os.path.realpath(sys.argv[0])) # os.path.dirname(__file__)+'' # os.path.abspath(".")
    return os.path.join(base_path, relative_path)

img_min = resource_path("image/min.png").replace('\\', '/')
img_max = resource_path("image/max.png").replace('\\', '/')
img_restore = resource_path("image/restore.png").replace('\\', '/')
img_close = resource_path("image/close.png").replace('\\', '/')
img_icon = resource_path("image/icon.png").replace('\\', '/')
img_icon_black = resource_path("image/icon_black.png").replace('\\', '/')
database_path = resource_path("memo.db").replace('\\', '/')

class InputDialog(QWidget):
    def __init__(self):
        super(InputDialog, self).__init__()
        self.initUi()
        self.id = 0
        self.show()

    def load_data(self, id, time, event, level):
        self.time.setText(time)
        self.event.setText(event)
        self.level.setText(level)
        self.id = id

    def initUi(self):
        self.setWindowTitle("新增/修改记录")
        titleIcon = QIcon(img_icon_black)
        self.setWindowIcon(titleIcon)
        self.resize(300, 200)
        self.center()
        label1 = QLabel("时    间：")
        label2 = QLabel("事    件：")
        label3 = QLabel("紧急程度：")

        self.time = QLineEdit()
        self.event = QLineEdit()
        self.level = QLineEdit()
        self.level.setPlaceholderText("输入数字，越大越紧急")
        self.ok_btn = QPushButton("确定")

        self.cancel_btn = QPushButton("取消")
        mainLayout = QVBoxLayout()
        topWidget = QWidget()
        botWidget = QWidget()
        btnLay = QHBoxLayout()
        glLay = QGridLayout()
        glLay.addWidget(label1, 0, 0)
        glLay.addWidget(self.time, 0, 1)
        glLay.addWidget(label2, 1, 0)
        glLay.addWidget(self.event, 1, 1)
        glLay.addWidget(label3, 2, 0)
        glLay.addWidget(self.level, 2, 1)
        btnLay.addWidget(self.ok_btn, 1)
        btnLay.addWidget(self.cancel_btn, 1)
        topWidget.setLayout(glLay)
        botWidget.setLayout(btnLay)
        mainLayout.addWidget(topWidget)
        mainLayout.addWidget(botWidget)
        self.setLayout(mainLayout)

    # 控制窗口显示在屏幕中心的方法
    def center(self):
        # 获得窗口
        qr = self.frameGeometry()
        # 获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        # 显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class myLabel(QLabel):
    _signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(myLabel, self).__init__(parent)

    def mousePressEvent(self, e):  ##重载一下鼠标点击事件
        self._signal.emit("")


class TitleWidget(QWidget):
    def __init__(self):
        super().__init__()
        # self.setStyleSheet("background-color:blue")
        titleIcon = QPixmap(img_icon)
        self.Icon = myLabel()
        self.Icon.setPixmap(titleIcon.scaled(20, 20))
        titleContent = QLabel("备忘录")
        titleContent.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        titleContent.setFixedHeight(TITLE_HEIGHT)
        titleContent.setObjectName("TitleContent")
        self.ButtonMin = QPushButton()
        self.ButtonMin.setFixedSize(QSize(BUTTON_WIDTH, BUTTON_HEIGHT))
        self.ButtonMin.setObjectName("ButtonMin")
        self.ButtonMax = QPushButton()
        self.ButtonMax.setFixedSize(QSize(BUTTON_WIDTH, BUTTON_HEIGHT))
        self.ButtonMax.setObjectName("ButtonMax")
        self.ButtonRestore = QPushButton()
        self.ButtonRestore.setFixedSize(QSize(BUTTON_WIDTH, BUTTON_HEIGHT))
        self.ButtonRestore.setObjectName("ButtonRestore")
        self.ButtonRestore.setVisible(False)
        self.ButtonClose = QPushButton()
        self.ButtonClose.setFixedSize(QSize(BUTTON_WIDTH, BUTTON_HEIGHT))
        self.ButtonClose.setObjectName("ButtonClose")
        mylayout = QHBoxLayout()
        mylayout.setSpacing(0)
        mylayout.setContentsMargins(5, 5, 5, 5)
        mylayout.addWidget(self.Icon)

        mylayout.addWidget(titleContent)
        mylayout.addWidget(self.ButtonMin)
        mylayout.addWidget(self.ButtonMax)
        mylayout.addWidget(self.ButtonRestore)
        mylayout.addWidget(self.ButtonClose)

        self.setLayout(mylayout)
        # QSS可写在文件中 读文件使用 这里方便大家使用直接写在代码里吧
        Qss = '''

            QLabel#TitleContent
            {
                color: #FFFFFF;
            }

            QPushButton#ButtonMin
            {
                border-image:url(%s) 0 81 0 0 ;

            }

            QPushButton#ButtonMin:hover
            {
                border-image:url(%s) 0 54 0 27 ;
            }

            QPushButton#ButtonMin:pressed
            {
                border-image:url(%s) 0 27 0 54 ;
            }

            QPushButton#ButtonMax
            {
                border-image:url(%s) 0 81 0 0 ;
            }

            QPushButton#ButtonMax:hover
            {
                border-image:url(%s) 0 54 0 27 ;
            }

            QPushButton#ButtonMax:pressed
            {
                border-image:url(%s) 0 27 0 54 ;
            }

            QPushButton#ButtonRestore
            {
                border-image:url(%s) 0 81 0 0 ;
            }

            QPushButton#ButtonRestore:hover
            {
                border-image:url(%s) 0 54 0 27 ;
            }

            QPushButton#ButtonRestore:pressed
            {
                border-image:url(%s) 0 27 0 54 ;
            }

            QPushButton#ButtonClose
            {
                border-image:url(%s) 0 81 0 0 ;
                border-top-right-radius:3 ;
            }

            QPushButton#ButtonClose:hover
            {
                border-image:url(%s) 0 54 0 27 ;
                border-top-right-radius:3 ;
            }

            QPushButton#ButtonClose:pressed
            {
                border-image:url(%s) 0 27 0 54 ;
                border-top-right-radius:3 ;
            }

            ''' % (
        img_min, img_min, img_min, img_max, img_max, img_max, img_restore, img_restore, img_restore, img_close,
        img_close, img_close)
        self.setStyleSheet(Qss)

        self.restorePos = None
        self.restoreSize = None
        self.startMovePos = None

    def saveRestoreInfo(self, point, size):
        self.restorePos = point
        self.restoreSize = size

    def getRestoreInfo(self):
        return self.restorePos, self.restoreSize


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowMinimizeButtonHint | Qt.WindowStaysOnTopHint)
        self.resize(350, 500)
        self.center()
        AllWidget = QWidget()
        # AllWidget.setStyleSheet("color:white;")
        Alllayout = QVBoxLayout()
        Alllayout.setSpacing(0)
        Alllayout.setContentsMargins(0, 0, 0, 0)
        AllWidget.setLayout(Alllayout)
        self.title = TitleWidget()
        self.title.setFixedWidth(self.width())
        self.title.setFixedHeight(TITLE_HEIGHT)
        self.setWindowOpacity(0.7)  # 设置窗口透明度
        # self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.title.ButtonMin.clicked.connect(self.ButtonMinSlot)
        self.title.ButtonMax.clicked.connect(self.ButtonMaxSlot)
        self.title.ButtonRestore.clicked.connect(self.ButtonRestoreSlot)
        self.title.ButtonClose.clicked.connect(self.ButtonCloseSlot)
        self.title.Icon._signal.connect(self.ButtonAddNew)
        centerWidget = QWidget()
        ver_layout = QVBoxLayout(centerWidget)

        self.list_view = QListView()
        self.load_record()
        self.list_view.setContextMenuPolicy(3)
        self.list_view.customContextMenuRequested[QPoint].connect(self.listWidgetContext)
        self.list_view.doubleClicked.connect(self.clickedlist)  # listview 的点击事件
        self.list_view.setStyleSheet('''
            QListView{font-family:"微软雅黑"; text-size:16px;color:#005AB5; font-weight:bold;}
            QListView::item{margin-top:5px;margin-bottom:5px;}
            ''')
        self.list_view.setWordWrap(True)
        ver_layout.addWidget(self.list_view)
        # centerWidget 中可以随意添加自己想用的控件
        # centerWidget.setStyleSheet("background-color:red")
        self.Qss = '''
            QMainWindow{
                background:qlineargradient(spread:pad,x1:1,y1:0,x2:0,y2:0,stop:0 #3d3d3d,stop:1 #4d4d4d);  

            }
        '''

        Alllayout.addWidget(self.title)
        Alllayout.addWidget(centerWidget)
        self.setCentralWidget(AllWidget)
        self.setStyleSheet(self.Qss)

    def load_record(self):
        global data_source
        data_source = []
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        # 执行一条语句,创建 user表
        sql = "create table if not exists record (id integer primary key autoincrement not null , memo_time varchar(30), " \
              "memo_event varchar(255), memo_level integer(5))"
        cursor.execute(sql)
        sql = "select * from record order by memo_level desc"
        result = cursor.execute(sql)
        slm = QStringListModel()  # 创建mode
        self.qList = []  # 添加的数组数据
        for row in result:
            data_source.append([str(row[0]), str(row[1]), str(row[2]), str(row[3])])
            self.qList.append("时间:" + str(row[1]) + "   事件：" + str(row[2]) + "   紧急程度：" + str(row[3]) + "级")
        if len(data_source) == 0:
            self.qList.append("还没有记录哦，点击左上角图标添加！")
        conn.commit()
        slm.setStringList(self.qList)  # 将数据设置到model
        self.list_view.setModel(slm)  ##绑定 listView 和 model
        cursor.close()
        conn.close()

    def update_record(self, time='', event='', level=1, id=0):
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        # 执行一条语句,创建 user表
        sql = "update record set memo_time = ?, memo_event = ?, memo_level = ? where id = ?"
        cursor.execute(sql, (time, event, level, id,))
        conn.commit()
        cursor.close()
        conn.close()
        self.load_record()

    def add_record(self, time='', event='', level=1):
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        # 执行一条语句,创建 user表
        sql = "insert into record values (NULL, ?, ?, ?)"
        cursor.execute(sql, (time, event, level,))
        conn.commit()
        cursor.close()
        conn.close()
        self.load_record()

    def delete_record(self, id=0):
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        # 执行一条语句,创建 user表
        sql = "delete from record where id = ?"
        cursor.execute(sql, (id,))
        conn.commit()
        cursor.close()
        conn.close()
        self.load_record()

    def ButtonMinSlot(self):
        self.showMinimized()

    def ButtonMaxSlot(self):
        self.title.ButtonMax.setVisible(False)
        self.title.ButtonRestore.setVisible(True)
        self.title.saveRestoreInfo(self.pos(), QSize(self.width(), self.height()))
        desktopRect = QApplication.desktop().availableGeometry()
        FactRect = QRect(desktopRect.x() - 3, desktopRect.y() - 3, desktopRect.width() + 6, desktopRect.height() + 6)
        print(FactRect)
        self.setGeometry(FactRect)
        self.setFixedSize(desktopRect.width() + 6, desktopRect.height() + 6)

    def ButtonRestoreSlot(self):
        self.title.ButtonMax.setVisible(True)
        self.title.ButtonRestore.setVisible(False)
        windowPos, windowSize = self.title.getRestoreInfo()
        # print(windowPos,windowSize.width(),windowSize.height())
        self.setGeometry(windowPos.x(), windowPos.y(), windowSize.width(), windowSize.height())
        self.setFixedSize(windowSize.width(), windowSize.height())

    def ButtonCloseSlot(self):
        self.close()

    def clickedlist(self, qModelIndex):
        global data_source
        self.dlg = InputDialog()
        index = qModelIndex.row()
        self.dlg.setStyleSheet(self.Qss)
        self.dlg.load_data(data_source[index][0], data_source[index][1], data_source[index][2], data_source[index][3])
        self.dlg.ok_btn.clicked.connect(self.prepare_update_data)
        self.dlg.cancel_btn.clicked.connect(self.dlg.close)
        pass

    def click_menu_to_update(self):
        global data_source, operate_index
        self.dlg = InputDialog()
        self.dlg.setStyleSheet(self.Qss)
        self.dlg.load_data(data_source[operate_index][0], data_source[operate_index][1],
                           data_source[operate_index][2], data_source[operate_index][3])
        self.dlg.ok_btn.clicked.connect(self.prepare_update_data)
        self.dlg.cancel_btn.clicked.connect(self.dlg.close)

    def prepare_delete_data(self):
        global operate_index, data_source
        reply = QMessageBox.question(self,
                                     "提示",
                                     "确定要删除吗？",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            print('yes')
            self.delete_record(data_source[operate_index][0])
        else:
            pass

    def prepare_update_data(self):
        time = self.dlg.time.text()
        event = self.dlg.event.text().replace(" ", "")
        level = self.dlg.level.text().replace(" ", "")
        if len(time.replace(" ", "")) == 0 or len(event) == 0 or len(level) == 0:
            QMessageBox.information(self, '提示', '请输入正确的信息！', QMessageBox.Yes, QMessageBox.Yes)
            return
        self.update_record(time, event, level, self.dlg.id)
        self.dlg.close()

    def prepare_add_data(self):
        time = self.dlg.time.text()
        event = self.dlg.event.text().replace(" ", "")
        level = self.dlg.level.text().replace(" ", "")
        if len(time.replace(" ", "")) == 0 or len(event) == 0 or len(level) == 0:
            QMessageBox.information(self, '提示', '请输入正确的信息！', QMessageBox.Yes, QMessageBox.Yes)
            return
        self.add_record(time, event, level)
        self.dlg.close()

    def ButtonAddNew(self):
        self.dlg = InputDialog()
        self.dlg.setStyleSheet(self.Qss)
        self.dlg.ok_btn.clicked.connect(self.prepare_add_data)
        self.dlg.cancel_btn.clicked.connect(self.dlg.close)
        pass

    def paintEvent(self, event):
        self.title.setFixedWidth(self.width())

    def listWidgetContext(self, point):
        global operate_index
        operate_index = self.list_view.indexAt(point).row()
        popMenu = QMenu()
        actionA = QAction('修改', self)
        actionB = QAction('删除', self)
        popMenu.addAction(actionA)
        popMenu.addAction(actionB)
        actionA.triggered.connect(self.click_menu_to_update)
        actionB.triggered.connect(self.prepare_delete_data)
        popMenu.exec_(QCursor.pos())

    def center(self):
        desktop = QApplication.desktop()
        self.move(desktop.width() - 400, (desktop.height() - self.height()) / 2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    try:
        ex = MainWindow()
        ex.show()
    except:
        traceback.print_exc()
    finally:
        gc.collect()
        delMEI()
    sys.exit(app.exec_())