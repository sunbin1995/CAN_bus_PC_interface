import sys
import os
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtWidgets
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QSizePolicy, QLabel, QTextEdit, QSpinBox,\
                            QDoubleSpinBox, QComboBox
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from can import CANalyser
import read
import oscilloscope

canControl = CANalyser()


class ApplicationWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        QMainWindow.resize(self, 2000, 2000)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        ##self.setWindowOpacity(0.9)
       ## self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowTitle("电机控制系统操作界面")

        #  添加画布
        self.main_widget = QtWidgets.QWidget(self)
        vbox = QtWidgets.QVBoxLayout(self.main_widget)
        self.canvas = MyMplCanvas(self.main_widget)
        self.canvas_ntb = NavigationToolbar(self.canvas, self)  # 添加完整的 toolbar
        vbox.addWidget(self.canvas)
        vbox.addWidget(self.canvas_ntb)
        self.setLayout(vbox)
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        #  标签
        self.label1 = QLabel(self)
        self.setFont(QFont('微软雅黑', 11))
        self.label1.setText("CAN连接状态:")
        self.label1.setGeometry(330, 60, 120, 50)

        self.label2 = QLabel(self)
        self.label2.setText("永磁同步电机\n   启停状态：")
        self.label2.setGeometry(180, 170, 120, 50)

        self.label2.setStyleSheet(
            '''
               QLabel{color:black;}
            ''')
        self.label3 = QLabel(self)
        self.label3.setText("感应电机\n启停状态：")
        self.label3.setGeometry(490, 170, 120, 50)
        self.label3.setStyleSheet(
            '''
               QLabel{color:black;}
            ''')

        #  文字
        self.text1 = QTextEdit(self)
        self.text1.setTextColor(QColor(255, 0, 0))
        self.text1.setGeometry(480, 65, 100, 40)
        self.text1.setPlainText("    未连接")
        self.text1.setStyleSheet('''QTextEdit{
                background:#ffffff;
                border:2px solid gray;
                border-radius:10px;}''')
        self.text1.setReadOnly(True)

        self.text2 = QTextEdit(self)
        self.text2.setTextColor(QColor(255, 0, 0))
        self.text2.setGeometry(180, 255, 100, 40)
        self.text2.setPlainText("     关停")
        self.text2.setStyleSheet('''QTextEdit{
                background:#ffffff;
                border:2px solid gray;
                border-radius:10px;}''')
        self.text2.setReadOnly(True)

        self.text3 = QTextEdit(self)
        self.text3.setTextColor(QColor(255, 0, 0))
        self.text3.setGeometry(480, 255, 100, 40)
        self.text3.setPlainText("     关停")
        self.text3.setStyleSheet('''QTextEdit{
                background:#ffffff;
                border:2px solid gray;
                border-radius:10px;}''')
        self.text3.setReadOnly(True)

        self.frame1 = QTextEdit(self)
        self.frame1.setGeometry(20, 40, 580, 90)
        self.frame1.setStyleSheet('''QTextEdit{
                border:2px dotted;
                border-radius:8px;}''')
        self.frame1.setReadOnly(True)
        self.label1.raise_()
        self.text1.raise_()

        self.frame2 = QTextEdit(self)
        self.frame2.setGeometry(20, 150, 280, 650)
        self.frame2.setStyleSheet('''QTextEdit{
                border:2px dotted;
                border-radius:8px;}''')
        self.frame2.setReadOnly(True)
        self.label2.raise_()
        self.text2.raise_()

        self.frame3 = QTextEdit(self)
        self.frame3.setGeometry(320, 150, 280, 650)
        self.frame3.setStyleSheet('''QTextEdit{
                border:2px dotted;
                border-radius:8px;}''')
        self.frame3.setReadOnly(True)
        self.label3.raise_()
        self.text3.raise_()

        self.frame4 = QTextEdit(self)
        self.frame4.setGeometry(20, 815, 580, 90)
        self.frame4.setReadOnly(True)
        self.frame4.setStyleSheet('''QTextEdit{
                border:2px dotted;
                border-radius:8px;}''')

        # 选值框
        self.sp = QSpinBox(self)
        self.sp.setMaximum(2000)
        self.sp.setMinimum(-2000)
        self.sp.setSuffix("rpm")
        self.sp.setGeometry(180, 410, 100, 50)
        self.sp.setStyleSheet('''QSpinBox{
               border:2px solid gray;
               border-radius:10px;
               font-size:20px;
               font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}''')

        self.sp1 = QSpinBox(self)
        self.sp1.setMaximum(9999)
        self.sp1.setMinimum(0)
        self.sp1.setGeometry(180, 730, 100, 50)
        self.sp1.setStyleSheet('''QSpinBox{
               border:2px solid gray;
               border-radius:10px;
               font-size:20px;
               font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}''')

        self.sp2 = QDoubleSpinBox(self)
        self.sp2.setSingleStep(0.01)
        self.sp2.setGeometry(180, 650, 100, 50)
        self.sp2.setStyleSheet('''QDoubleSpinBox{
               border:2px solid gray;
               border-radius:10px;
               font-size:20px;
               font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}''')

        self.sp3 = QSpinBox(self)
        self.sp3.setMaximum(9999)
        self.sp3.setMinimum(0)
        self.sp3.setGeometry(180, 570, 100, 50)
        self.sp3.setStyleSheet('''QSpinBox{
               border:2px solid gray;
               border-radius:10px;
               font-size:20px;
               font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}''')

        self.sp4 = QDoubleSpinBox(self)
        self.sp4.setSingleStep(0.01)
        self.sp4.setGeometry(480, 730, 100, 50)
        self.sp4.setStyleSheet('''QDoubleSpinBox{
               border:2px solid gray;
               border-radius:10px;
               font-size:20px;
               font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}''')

        self.sp5 = QSpinBox(self)
        self.sp5.setMaximum(3600)
        self.sp5.setMinimum(-3600)
        self.sp5.setSuffix("°")
        self.sp5.setGeometry(180, 490, 100, 50)
        self.sp5.setStyleSheet('''QSpinBox{
               border:2px solid gray;
               border-radius:10px;
               font-size:20px;
               font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}''')

        self.sp6 = QComboBox(self)       #PMSM的控制模式选择
        self.sp6.setGeometry(180, 330, 100, 50)
        self.sp6.addItem("VF控制")
        self.sp6.addItem("矢量控制")
        self.sp6.addItem("IF控制")
        self.sp6.addItem("无感矢量控制")
        self.sp6.addItem("二阶自抗扰控制")
        self.sp6.addItem("位置控制")
        self.sp6.setStyleSheet('''QComboBox{
               border:2px solid gray;
               border-radius:10px;
               font-size:15px;
               font-family: "微软雅黑", Helvetica, Arial, sans-serif;}''')

        self.sp7 = QComboBox(self)   #异步电机的控制模式
        self.sp7.setGeometry(480, 330, 100, 50)
        self.sp7.addItem("VF控制")
        self.sp7.addItem("矢量控制")
        self.sp7.setStyleSheet('''QComboBox{
               border:2px solid gray;
               border-radius:10px;
               font-size:15px;
               font-family: "微软雅黑", Helvetica, Arial, sans-serif;}''')

        self.sp8 = QSpinBox(self)   #异步电机的给定转速
        self.sp8.setMaximum(2000)
        self.sp8.setMinimum(-2000)
        self.sp8.setSuffix("rpm")
        self.sp8.setGeometry(480, 410, 100, 50)
        self.sp8.setStyleSheet('''QSpinBox{
               border:2px solid gray;
               border-radius:10px;
               font-size:20px;
               font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}''')

        self.sp9 = QSpinBox(self)  #异步电机的参数A
        self.sp9.setMaximum(9999)
        self.sp9.setMinimum(0)
        self.sp9.setGeometry(480, 490, 100, 50)
        self.sp9.setStyleSheet('''QSpinBox{
               border:2px solid gray;
               border-radius:10px;
               font-size:20px;
               font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}''')

        self.sp10 = QDoubleSpinBox(self)
        self.sp10.setSingleStep(0.01)
        self.sp10.setGeometry(480, 570, 100, 50)
        self.sp10.setStyleSheet('''QDoubleSpinBox{
               border:2px solid gray;
               border-radius:10px;
               font-size:20px;
               font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}''')

        self.sp11 = QSpinBox(self)
        self.sp11.setMaximum(9999)
        self.sp11.setMinimum(0)
        self.sp11.setGeometry(480, 650, 100, 50)
        self.sp11.setStyleSheet('''QSpinBox{
               border:2px solid gray;
               border-radius:10px;
               font-size:20px;
               font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}''')

        self.start_can = QPushButton('启动CAN', self)
        self.start_can.setGeometry(30, 60, 100, 50)
        self.start_can.setStyleSheet(
            '''QPushButton{background:#6DDF6D;
               border-radius:10px;}
               QPushButton:hover{background:green;}
            ''')
        self.start_can.clicked.connect(self.openCAN)
        self.start_can.clicked.connect(self.press_button_text1)

        self.delete_file = QPushButton('清空数据', self)
        self.delete_file.setGeometry(180, 60, 100, 50)
        self.delete_file.setStyleSheet(
            '''QPushButton{background:#F7D674;
               border-radius:10px;}
               QPushButton:hover{background:yellow;}
            ''')
        self.delete_file.clicked.connect(self.remove_txt)

        self.start_motor = QPushButton('启动电机', self)
        self.start_motor.setGeometry(30, 170, 100, 50)
        self.start_motor.setStyleSheet(
            '''QPushButton{background:#6DDF6D;
               border-radius:10px;}
               QPushButton:hover{background:green;}
            ''')
        self.start_motor.clicked.connect(self.sendmessage_startmotor)
        self.start_motor.clicked.connect(self.press_button_text2)

        self.start_motor1 = QPushButton('启动电机', self)
        self.start_motor1.setGeometry(330, 170, 100, 50)
        self.start_motor1.setStyleSheet(
            '''QPushButton{background:#6DDF6D;
               border-radius:10px;}
               QPushButton:hover{background:green;}
            ''')
        self.start_motor1.clicked.connect(self.sendmessage_startmotor1)
        self.start_motor1.clicked.connect(self.press_button_text4)

        self.close_motor = QPushButton('关停电机', self)
        self.close_motor.setGeometry(30, 250, 100, 50)
        self.close_motor.setStyleSheet(
            '''QPushButton{background:#F76677;
               border-radius:10px;
               font-}
               QPushButton:hover{background:red;}
            ''')
        self.close_motor.clicked.connect(self.sendmessage_closemotor)
        self.close_motor.clicked.connect(self.press_button_text3)

        self.close_motor1 = QPushButton('关停电机', self)
        self.close_motor1.setGeometry(330, 250, 100, 50)
        self.close_motor1.setStyleSheet(
            '''QPushButton{background:#F76677;
               border-radius:10px;
               font-}
               QPushButton:hover{background:red;}
            ''')
        self.close_motor1.clicked.connect(self.sendmessage_closemotor1)
        self.close_motor1.clicked.connect(self.press_button_text5)

        self.change_speed = QPushButton('给定转速', self)
        self.change_speed.setGeometry(30, 410, 100, 50)
        self.change_speed.clicked.connect(self.send_message_change_speed)
        self.change_speed.setStyleSheet(
            '''QPushButton{background:#c0c0c0;
               border-radius:10px;}
               QPushButton:hover{background:grey;}
            '''
        )

        self.change_speed1 = QPushButton('给定转速', self)
        self.change_speed1.setGeometry(330, 410, 100, 50)
        self.change_speed1.clicked.connect(self.send_message_change_speed1)
        self.change_speed1.setStyleSheet(
            '''QPushButton{background:#c0c0c0;
               border-radius:10px;}
               QPushButton:hover{background:grey;}
            '''
        )

        self.change_position = QPushButton('给定位置', self)
        self.change_position.setGeometry(30, 490, 100, 50)
        self.change_position.clicked.connect(self.send_message_change_position)
        self.change_position.setStyleSheet(
            '''QPushButton{background:#c0c0c0;
               border-radius:10px;}
               QPushButton:hover{background:grey;}
            '''
        )

        self.change_B = QPushButton('设定参数kp', self)
        self.change_B.setGeometry(30, 650, 100, 50)
        self.change_B.clicked.connect(self.send_message_change_b)
        self.change_B.setStyleSheet(
            '''QPushButton{background:#c0c0c0;
               border-radius:10px;}
               QPushButton:hover{background:grey;}
            '''
        )

        self.change_B1 = QPushButton('设定参数B', self)
        self.change_B1.setGeometry(330, 570, 100, 50)
        self.change_B1.clicked.connect(self.send_message_change_b1)
        self.change_B1.setStyleSheet(
            '''QPushButton{background:#c0c0c0;
               border-radius:10px;}
               QPushButton:hover{background:grey;}
            '''
        )

        self.change_C = QPushButton('设定参数β', self)
        self.change_C.setGeometry(30, 570, 100, 50)
        self.change_C.clicked.connect(self.send_message_change_c)
        self.change_C.setStyleSheet(
            '''QPushButton{background:#c0c0c0;
               border-radius:10px;}
               QPushButton:hover{background:grey;}
            '''
        )

        self.change_C1 = QPushButton('设定参数A', self)
        self.change_C1.setGeometry(330, 490, 100, 50)
        self.change_C1.clicked.connect(self.send_message_change_c1)
        self.change_C1.setStyleSheet(
            '''QPushButton{background:#c0c0c0;
               border-radius:10px;}
               QPushButton:hover{background:grey;}
            '''
        )

        self.change_D = QPushButton('设定参数Ki', self)
        self.change_D.setGeometry(330, 730, 100, 50)
        self.change_D.clicked.connect(self.send_message_change_d)
        self.change_D.setStyleSheet(
            '''QPushButton{background:#c0c0c0;
               border-radius:10px;}
               QPushButton:hover{background:grey;}
            '''
        )

        self.change_A = QPushButton('设定参数r', self)
        self.change_A.setGeometry(30, 730, 100, 50)
        self.change_A.clicked.connect(self.send_message_change_a)
        self.change_A.setStyleSheet(
            '''QPushButton{background:#c0c0c0;
               border-radius:10px;}
               QPushButton:hover{background:grey;}
            '''
        )
        self.change_A1 = QPushButton('设定参数C', self)
        self.change_A1.setGeometry(330, 650, 100, 50)
        self.change_A1.clicked.connect(self.send_message_change_a1)
        self.change_A1.setStyleSheet(
            '''QPushButton{background:#c0c0c0;
               border-radius:10px;}
               QPushButton:hover{background:grey;}
            '''
        )

        self.change_control_mode = QPushButton('控制模式', self)
        self.change_control_mode.setGeometry(30, 330, 100, 50)
        self.change_control_mode.clicked.connect(self.send_message_change_mode)
        self.change_control_mode.setStyleSheet(
            '''QPushButton{background:#c0c0c0;
               border-radius:10px;}
               QPushButton:hover{background:grey;}
            '''
        )

        self.change_control_mode = QPushButton('控制模式', self)
        self.change_control_mode.setGeometry(330, 330, 100, 50)
        self.change_control_mode.clicked.connect(self.send_message_change_mode1)
        self.change_control_mode.setStyleSheet(
            '''QPushButton{background:#c0c0c0;
               border-radius:10px;}
               QPushButton:hover{background:grey;}
            '''
        )

        self.quit = QPushButton('退出界面', self)
        self.quit.setGeometry(460, 830, 120, 60)
        self.quit.clicked.connect(self.close)
        self.quit.setStyleSheet(
            '''QPushButton{background:#F76677;
               border-radius:10px;}
               QPushButton:hover{background:red;}
            '''
        )

        self.run_sync = QPushButton('双机同步运行', self)
        self.run_sync.setGeometry(30, 830, 120, 60)
        self.run_sync.clicked.connect(self.sendmessage_run_sync)
        self.run_sync.setStyleSheet(
            '''QPushButton{background:#60DF60;
               border-radius:10px;}
               QPushButton:hover{background:green;}
            '''
        )

        self.close_sync = QPushButton('双机同步关停', self)
        self.close_sync.setGeometry(240, 830, 120, 60)
        self.close_sync.clicked.connect(self.sendmessage_close_sync)
        self.close_sync.setStyleSheet(
            '''QPushButton{background:#F7D674;
               border-radius:10px;}
               QPushButton:hover{background:yellow;}
            '''
        )

    def plotter(self):
        self.plot = oscilloscope.animationClass(self.canvas, self)  # 实时更新画布

    def press_button_text1(self):
        if canControl.alive == 1:
            self.text1.setTextColor(QColor(0, 255, 0))
            self.text1.setPlainText("   已连接")

            self.text2.setTextColor(QColor(255, 120, 0))
            self.text2.setPlainText("     待机")

            self.text3.setTextColor(QColor(255, 120, 0))
            self.text3.setPlainText("     待机")

        else:
            self.text1.setTextColor(QColor(0, 0, 0))
            self.text1.setPlainText("    关停")
            self.text1.setTextColor(QColor(255, 0, 0))

    def press_button_text2(self):
        if canControl.alive == 1:
            self.text2.setTextColor(QColor(0, 255, 0))
            self.text2.setPlainText("     启动")

    def press_button_text4(self):
        if canControl.alive == 1:
            self.text3.setTextColor(QColor(0, 255, 0))
            self.text3.setPlainText("     启动")

    def press_button_text3(self):
        if canControl.alive == 1:
            self.text2.setTextColor(QColor(255, 120, 0))
            self.text2.setPlainText("     待机")
        else:
            self.text2.setTextColor(QColor(255, 0, 0))
            self.text2.setPlainText("     关停")

    def press_button_text5(self):
        if canControl.alive == 1:
            self.text3.setTextColor(QColor(255, 120, 0))
            self.text3.setPlainText("     待机")
        else:
            self.text3.setTextColor(QColor(255, 0, 0))
            self.text3.setPlainText("     关停")

    def openCAN(self):
        canControl.opendevice()
        canControl.initdevice()
        canControl.startcan()
    '''
    上下位机通信自订协议：
        CAN总线报文最后一位是命令位。前两位是数据位。下面为命令位list
        99：使能PMSM
        98; 使能IM
        
        2： 关停PMSM·
        3： 关停IM·
        10: 双机同步运行·
        11： 双机同步关停·
        
        13： 给定转速
        14： 改变参数a
        15:  改变参数b
        16： 改变参数c
        17:  改变参数d
        18： 给定位置
        19： 改变PMSM控制模式
        
        20： 改变IM控制模式·
        21：给定转速·
        22：改变参数c·
        23：改变参数b·
        24：改变参数a·
        
    '''

    def send_message_change_speed(self):
        canControl.transmit(id=0x01, send_type=1, len=8, InputData=((self.sp.value() & 0xff00) >> 8,
                                                                    self.sp.value() & 0x00ff, 13, 13, 13, 13, 13, 13))

    def send_message_change_speed1(self):
        canControl.transmit(id=0x01, send_type=1, len=8, InputData=((self.sp8.value() & 0xff00) >> 8,
                                                                    self.sp8.value() & 0x00ff, 21, 21, 21, 21, 21, 21))

    def send_message_change_position(self):
        canControl.transmit(id=0x01, send_type=1, len=8, InputData=((self.sp5.value() & 0xff00) >> 8,
                                                                    self.sp5.value() & 0x00ff, 18, 18, 18, 18, 18, 18))

    def send_message_change_a(self):
        canControl.transmit(id=0x01, send_type=1, len=8, InputData=((self.sp1.value() & 0xff00) >> 8,
                                                                    self.sp1.value() & 0x00ff, 14, 14, 14, 14, 14, 14))

    def send_message_change_a1(self):
        canControl.transmit(id=0x01, send_type=1, len=8, InputData=((self.sp11.value() & 0xff00) >> 8,
                                                                    self.sp11.value() & 0x00ff, 24, 24, 24, 24, 24, 24))

    def send_message_change_b(self):
        canControl.transmit(id=0x01, send_type=1, len=8, InputData=((int(self.sp2.value()*100) & 0xff00) >> 8,
                                                                    int(self.sp2.value()*100) & 0x00ff, 15, 15, 15, 15,
                                                                    15, 15))

    def send_message_change_b1(self):
        canControl.transmit(id=0x01, send_type=1, len=8, InputData=((int(self.sp2.value()*100) & 0xff00) >> 8,
                                                                    int(self.sp2.value()*100) & 0x00ff, 23, 23, 23, 23,
                                                                    23, 23))

    def send_message_change_c(self):
        canControl.transmit(id=0x01, send_type=1, len=8, InputData=((self.sp3.value() & 0xff00) >> 8,
                                                                    self.sp3.value() & 0x00ff, 16, 16, 16, 16, 16, 16))

    def send_message_change_c1(self):
        canControl.transmit(id=0x01, send_type=1, len=8, InputData=((self.sp9.value() & 0xff00) >> 8,
                                                                    self.sp9.value() & 0x00ff, 22, 22, 22, 22, 22, 22))

    def send_message_change_d(self):
        canControl.transmit(id=0x01, send_type=1, len=8, InputData=((int(self.sp4.value()*100) & 0xff00) >> 8,
                                                                    int(self.sp4.value()*100) & 0x00ff, 17, 17, 17, 17,
                                                                    17, 17))

    def send_message_change_mode(self):
        canControl.transmit(id=0x01, send_type=1, len=8, InputData=(self.sp6.currentIndex(), 19, 19, 19, 19, 19, 19, 19))

    def send_message_change_mode1(self):
        canControl.transmit(id=0x01, send_type=1, len=8, InputData=(self.sp7.currentIndex(), 20, 20, 20, 20, 20, 20, 20))

    def sendmessage_startmotor(self):
        canControl.transmit(id=0x01, send_type=1, len=8, InputData=(99, 99, 99, 99, 99, 99, 99, 99))
        # send type=0正常发送 send_type=1单次发送，send_type=2自发自收，

    def sendmessage_startmotor1(self):
        canControl.transmit(id=0x01, send_type=1, len=8, InputData=(98, 98, 98, 98, 98, 98, 98, 98))
        # send type=0正常发送 send_type=1单次发送，send_type=2自发自收，

    def sendmessage_closemotor(self):
        canControl.transmit(id=0x01, send_type=1, len=8, InputData=(2, 2, 2, 2, 2, 2, 2, 2))

    def sendmessage_closemotor1(self):
        canControl.transmit(id=0x01, send_type=1, len=8, InputData=(3, 3, 3, 3, 3, 3, 3, 3))

    def sendmessage_run_sync(self):   #双机同步运行
        canControl.transmit(id=0x01, send_type=1, len=8, InputData=(10, 10, 10, 10, 10, 10, 10, 10))

    def sendmessage_close_sync(self):
        canControl.transmit(id=0x01, send_type=1, len=8, InputData=(11, 11, 11, 11, 11, 11, 11, 11))

    def remove_txt(self):
        filename1 = r'./speed.txt'
        filename2 = r'./current.txt'
        filename3 = r'./dc.txt'
        filename4 = r'./position.txt'
        if os.path.exists(filename1) and os.path.exists(filename2) and os.path.exists(filename3)\
                and os.path.exists(filename4):
            os.remove(filename1)
            os.remove(filename2)
            os.remove(filename3)
            os.remove(filename4)
            self.canvas.ax1.clear()
            self.canvas.ax2.clear()
            self.canvas.ax3.clear()
            self.canvas.ax4.clear()
        else:
            pass


class MyMplCanvas(FigureCanvas):
    """FigureCanvas的最终的父类其实是QWidget。"""
    def __init__(self, parent=None, width=50, height=40, dpi=100):

        # 配置中文显示
        plt.rcParams['font.family'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor=(1, 1, 1))  # 新建一个figure
        self.fig.subplots_adjust(left=0.35, bottom=0.05, right=0.98, top=0.95, wspace=0.18, hspace=0.25)##调整坐标轴位置
        #plt.style.use("classic")
        self.ax1 = self.fig.add_subplot(221)
        self.ax2 = self.fig.add_subplot(222, sharex=self.ax1)
        self.ax3 = self.fig.add_subplot(223, sharex=self.ax1)
        self.ax4 = self.fig.add_subplot(224, sharex=self.ax1)
        # self.ax5 = self.fig.add_axes([0.3,0.7,0.1,0.1])#添加小图操作
        self.ax1.set_xlabel('时间（s）')
        self.ax1.set_ylabel('电流（A）')
        self.ax1.set_title('电流')
        self.ax1.grid(True)
        self.ax1.set_ylim(-11, 11)
        self.ax2.set_xlabel('时间（s）')
        self.ax2.set_ylabel('电压（V）')
        self.ax2.set_title('母线两电容电压')
        self.ax2.set_ylim(0, 200)
        self.ax2.grid(True)

        self.ax3.set_xlabel('时间（s）')
        self.ax3.set_ylabel('转速（r/min）')
        self.ax3.set_title('转速')
        #self.ax3.set_xlim(0, 1.5)
        #self.ax3.set_ylim(0, 300)
        #  self.ax3 = self.ax1.twinx()  # 与ax1镜像
        self.ax3.grid(True)

        self.ax4.set_xlabel('时间（s）')
        self.ax4.set_ylabel('机械角度（°）')
        self.ax4.set_title('位置')
        self.ax4.grid(True)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


def main():

    App = QApplication(sys.argv)
    aw = ApplicationWindow()
    aw.showMaximized()

    plot = threading.Thread(aw.plotter())
    plot.start()

    receive = read.readClass()
    receive.start()

    App.exit() 
    sys.exit(App.exec_())


if __name__ == "__main__":
    main()
