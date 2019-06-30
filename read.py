from PyQt5.QtCore import QThread, pyqtSignal
from ctypes import *

class _VCI_INIT_CONFIG(Structure):
    _fields_ = [('AccCode', c_ulong),
                ('AccMask', c_ulong),
                ('Reserved', c_ulong),
                ('Filter', c_ubyte),
                ('Timing0', c_ubyte),
                ('Timing1', c_ubyte),
                ('Mode', c_ubyte)]

class _VCI_CAN_OBJ(Structure):
    _fields_ = [('ID', c_uint),
                ('TimeStamp', c_uint),
                ('TimeFlag', c_ubyte),
                ('SendType', c_ubyte),
                ('RemoteFlag', c_ubyte),
                ('ExternFlag', c_ubyte),
                ('DataLen', c_ubyte),
                ('Data', c_ubyte*8),
                ('Reserved', c_ubyte*3)]

class readClass(QThread):
    trigger = pyqtSignal()
    def __init__(self):
        super(readClass, self).__init__()
        self.canLib = windll.LoadLibrary('./ECanVci64.dll')
        self.vic = _VCI_INIT_CONFIG()
        self.vic.AccCode = 0x00000000
        self.vic.AccMask = 0xffffffff
        self.vic.Filter = 0
        self.vic.Timing0 = 0x00
        self.vic.Timing1 = 0x1c   #波特率500K
        self.vic.Mode = 0
        self.vco = _VCI_CAN_OBJ()

        self.speed1 = []
        self.speed2 = []

        self.currentA = []
        self.currentB = []
        self.currentC = []

        self.dc1 = []
        self.dc2 = []

        self.position1 = []
        self.position2 = []

        self.time = []
        self.time1 = []
        self.time2 = []
        self.time3 = []

        self.frame = []
        self.frame1 = []
        self.frame2 = []
        self.frame3 = []

        self.id = 0
        self.id1 = 0
        self.id2 = 0
        self.id3 = 0

    def run(self):
        while True:
            num = self.canLib.GetReceiveNum(3, 0, 0)
            if num:
                flag = self.canLib.Receive(3, 0, 0, pointer(self.vco), 1, 0)
                if flag <= 0:
                    print('调用 VCI_Receive 出错\r\n')
                elif flag > 0:
                    if self.vco.ID == 0x280:
                        self.id = hex(self.vco.ID)
                        self.frame = list(self.vco.Data)
                        self.currentA = float(((self.frame[0] * 256 + self.frame[1]) / 32768) - 1) * 15.6
                        self.currentB = float(((self.frame[2] * 256 + self.frame[3])/32768)-1)*15.6  #15.6为电流标幺基准值
                        self.currentC = float(((self.frame[4] * 256 + self.frame[5]) / 32768) - 1) * 15.6
                        self.time = float((self.frame[6] * 256 +self.frame[7])/1000)
                        with open('current.txt', 'a') as f:  # a = append
                            f.write('{},{},{},{}\n'.format(self.currentA, self.currentB, self.currentC, self.time))
                    elif self.vco.ID == 0x380:
                        self.id1 = hex(self.vco.ID)
                        self.frame1 = list(self.vco.Data)
                        self.speed1 = float(((self.frame1[0] * 256 + self.frame1[1]) / 32768) - 1) * 2000
                        self.speed2 = float(((self.frame1[2] * 256 + self.frame1[3])/32768)-1) * 2000  #2000为转速标幺基准值
                        self.time1 = float((self.frame1[6] * 256 + self.frame1[7])/1000)
                        with open('speed.txt', 'a') as f2:
                            f2.write('{},{},{}\n'.format(self.speed1, self.speed2, self.time1))
                    elif self.vco.ID == 0x480:
                        self.id2 = hex(self.vco.ID)
                        self.frame2 = list(self.vco.Data)
                        self.dc1 = float(((self.frame2[0] * 256 + self.frame2[1]) / 32768) - 1) * 167
                        self.dc2 = float(((self.frame2[2] * 256 + self.frame2[3])/32768)-1) * 167
                        self.time2 = float((self.frame2[6] * 256 + self.frame2[7]) / 1000)
                        with open('dc.txt', 'a') as f3:
                            f3.write('{},{},{}\n'.format(self.dc1, self.dc2, self.time2))
                    elif self.vco.ID == 0x580:
                        self.id3 = hex(self.vco.ID)
                        self.frame3 = list(self.vco.Data)
                        self.position1 = float(((self.frame3[0] * 256 + self.frame3[1]) / 32768) - 1) * 10*360
                        self.position2 = float(((self.frame3[2] * 256 + self.frame3[3]) / 32768) - 1) * 10*360  # 360为角度标幺基准值
                        self.time3 = float((self.frame3[6] * 256 + self.frame3[7]) / 1000)
                        with open('position.txt', 'a') as f4:
                            f4.write('{},{},{}\n'.format(self.position1, self.position2, self.time3))
            #elif num == 0:
               #self.trigger.emit()


