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
                            QDoubleSpinBox
from PyQt5.QtGui import *
from can import CANalyser
import read
import oscilloscope

canControl = CANalyser()


class ApplicationWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        QMainWindow.resize(self, 2000, 2000)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
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
        self.label1.setGeometry(25, 200, 120, 50)

        self.label2 = QLabel(self)
        self.label2.setText("电机启停状态：")
        self.label2.setGeometry(180, 200, 120, 50)

        #  文字
        self.text1 = QTextEdit(self)
        self.text1.setTextColor(QColor(255, 0, 0))
        self.text1.setGeometry(30, 260, 100, 40)
        self.text1.setPlainText("   未连接")
        self.text1.setReadOnly(True)

        self.text2 = QTextEdit(self)
        self.text2.setTextColor(QColor(255, 0, 0))
        self.text2.setGeometry(180, 260, 100, 40)
        self.text2.setPlainText("     关停")
        self.text2.setReadOnly(True)

        # 选值框
        self.sp = QSpinBox(self)
        self.sp.setMaximum(2000)
        self.sp.setMinimum(-2000)
        self.sp.setGeometry(180, 330, 100, 50)

        self.sp1 = QSpinBox(self)
        self.sp1.setMaximum(9999)
        self.sp1.setMinimum(0)
        self.sp1.setGeometry(180, 730, 100, 50)

        self.sp2 = QDoubleSpinBox(self)
        self.sp2.setSingleStep(0.01)
        self.sp2.setGeometry(180, 570, 100, 50)

        self.sp3 = QSpinBox(self)
        self.sp3.setMaximum(9999)
        self.sp3.setMinimum(0)
        self.sp3.setGeometry(180, 490, 100, 50)

        self.sp4 = QDoubleSpinBox(self)
        self.sp4.setSingleStep(0.01)
        self.sp4.setGeometry(180, 650, 100, 50)

        self.sp5 = QSpinBox(self)
        self.sp5.setMaximum(3600)
        self.sp5.setMinimum(-3600)
        self.sp5.setGeometry(180, 410, 100, 50)
        #  按钮
        self.start_can = QPushButton('启动CAN', self)
        self.start_can.setGeometry(30, 60, 100, 50)
        self.start_can.clicked.connect(self.openCAN)
        self.start_can.clicked.connect(self.press_button_text1)

        self.delete_file = QPushButton('清空数据', self)
        self.delete_file.setGeometry(30, 140, 100, 50)
        self.delete_file.clicked.connect(self.remove_txt)

        self.start_motor = QPushButton('启动电机', self)
        self.start_motor.setGeometry(180, 60, 100, 50)
        self.start_motor.clicked.connect(self.sendmessage_startmotor)
        self.start_motor.clicked.connect(self.press_button_text2)

        self.close_motor = QPushButton('关停电机', self)
        self.close_motor.setGeometry(180, 140, 100, 50)
        self.close_motor.clicked.connect(self.sendmessage_closemotor)
        self.close_motor.clicked.connect(self.press_button_text3)

        self.change_speed = QPushButton('给定转速', self)
        self.change_speed.setGeometry(30, 330, 100, 50)
        self.change_speed.clicked.connect(self.send_message_change_speed)

        self.change_position = QPushButton('给定位置', self)
        self.change_position.setGeometry(30, 410, 100, 50)
        self.change_position.clicked.connect(self.send_message_change_position)

        self.change_B = QPushButton('设定参数kp', self)
        self.change_B.setGeometry(30, 570, 100, 50)
        self.change_B.clicked.connect(self.send_message_change_b)

        self.change_C = QPushButton('设定参数β', self)
        self.change_C.setGeometry(30, 490, 100, 50)
        self.change_C.clicked.connect(self.send_message_change_c)

        self.change_D = QPushButton('设定参数Ki', self)
        self.change_D.setGeometry(30, 650, 100, 50)
        self.change_D.clicked.connect(self.send_message_change_d)

        self.change_A = QPushButton('设定参数r', self)
        self.change_A.setGeometry(30, 730, 100, 50)
        self.change_A.clicked.connect(self.send_message_change_a)

        self.quit = QPushButton('退出界面', self)
        self.quit.setGeometry(30, 830, 100, 65)
        self.quit.clicked.connect(self.close)

    def plotter(self):
        self.plot = oscilloscope.animationClass(self.canvas, self)  # 实时更新画布

    def press_button_text1(self):
        if canControl.alive == 1:
            self.text1.setTextColor(QColor(0, 255, 0))
            self.text1.setPlainText("   已连接")
            self.text2.setTextColor(QColor(255, 120, 0))
            self.text2.setPlainText("     待机")
        else:
            self.text1.setTextColor(QColor(255, 0, 0))
            self.text1.setPlainText("   关停")
            self.text1.setTextColor(QColor(255, 0, 0))

    def press_button_text2(self):
        if canControl.alive == 1:
            self.text2.setTextColor(QColor(0, 255, 0))
            self.text2.setPlainText("     启动")

    def press_button_text3(self):
        if canControl.alive == 1:
            self.text2.setTextColor(QColor(255, 120, 0))
            self.text2.setPlainText("     待机")
        else:
            self.text2.setTextColor(QColor(255, 0, 0))
            self.text2.setPlainText("     关停")

    def openCAN(self):
        canControl.opendevice()
        canControl.initdevice()
        canControl.startcan()

    def send_message_change_speed(self):
        canControl.transmit(id=0x01, send_type=1, len=8, InputData=((self.sp.value() & 0xff00) >> 8,
                                                                    self.sp.value() & 0x00ff, 13, 13, 13, 13, 13, 13))
    def send_message_change_position(self):
        canControl.transmit(id=0x01, send_type=1, len=8, InputData=((self.sp5.value() & 0xff00) >> 8,
                                                                    self.sp5.value() & 0x00ff, 18, 18, 18, 18, 18, 18))

    def send_message_change_a(self):
        canControl.transmit(id=0x01, send_type=1, len=8, InputData=((self.sp1.value() & 0xff00) >> 8,
                                                                    self.sp1.value() & 0x00ff, 14, 14, 14, 14, 14, 14))

    def send_message_change_b(self):
        canControl.transmit(id=0x01, send_type=1, len=8, InputData=((int(self.sp2.value()*100) & 0xff00) >> 8,
                                                                    int(self.sp2.value()*100) & 0x00ff, 15, 15, 15, 15,
                                                                    15, 15))
    def send_message_change_c(self):
        canControl.transmit(id=0x01, send_type=1, len=8, InputData=((self.sp3.value() & 0xff00) >> 8,
                                                                    self.sp3.value() & 0x00ff, 16, 16, 16, 16, 16, 16))

    def send_message_change_d(self):
        canControl.transmit(id=0x01, send_type=1, len=8, InputData=((int(self.sp4.value()*100) & 0xff00) >> 8,
                                                                    int(self.sp4.value()*100) & 0x00ff, 17, 17, 17, 17,
                                                                    17, 17))
    def sendmessage_startmotor(self):
        canControl.transmit(id=0x01, send_type=1, len=8, InputData=(99, 99, 99, 99, 99, 99, 99, 99))
        # send type=0正常发送 send_type=1单次发送，send_type=2自发自收，

    def sendmessage_closemotor(self):
        canControl.transmit(id=0x01, send_type=1, len=8, InputData=(2, 2, 2, 2, 2, 2, 2, 2))

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
        self.fig.subplots_adjust(left=0.2, bottom=0.05, right=0.95, top=0.95, wspace=0.12, hspace=0.25)
        #plt.style.use("classic")
        self.ax1 = self.fig.add_subplot(221)
        self.ax2 = self.fig.add_subplot(222, sharex=self.ax1)
        self.ax3 = self.fig.add_subplot(223, sharex=self.ax1)
        self.ax4 = self.fig.add_subplot(224, sharex=self.ax1)
        # self.ax5 = self.fig.add_axes([0.3,0.7,0.1,0.1])#添加小图操作
        self.ax1.set_xlabel('时间（s）')
        self.ax1.set_ylabel('电流（A）')
        self.ax1.set_title('电流/转速')
        self.ax1.set_ylim(-11, 11)
        self.ax2.set_xlabel('时间（s）')
        self.ax2.set_ylabel('电压（V）')
        self.ax2.set_title('母线俩电容电压')

        self.ax2.set_ylim(0, 200)
        self.ax3.set_xlabel('时间（s）')
        self.ax3.set_ylabel('转速（r/min）')
        self.ax3.set_title('转速')
        #  self.ax3 = self.ax1.twinx()  # 与ax1镜像

        self.ax4.set_xlabel('时间（s）')
        self.ax4.set_ylabel('角度')
        self.ax4.set_title('位置')

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
