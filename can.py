from ctypes import *


class _VCI_INIT_CONFIG(Structure):
    _fields_ = [('AccCode', c_ulong),
                ('AccMask', c_ulong),
                ('Reserved', c_ulong),
                ('Filter', c_ubyte),
                ('Timing0', c_ubyte),
                ('Timing1', c_ubyte),
                ('Mode', c_ubyte)]


class VCI_CAN_OBJ(Structure):
    count = 0
    _fields_ = [('ID', c_uint),
                ("TimeStamp", c_uint),
                ("TimeFlag", c_byte),
                ('SendType', c_byte),
                ('RemoteFlag', c_byte),
                ('ExternFlag', c_byte),
                ('DataLen', c_byte),
                ('Data', c_ubyte * 8),
                ('Reserved', c_byte * 3)]


class CANalyser():

    def __init__(self):
        try:
            self.canlib = windll.LoadLibrary('./ECanVci64.dll')
            print("load DLL success")
        except Exception as e:
            print("ERROR:Exception in load ControlCan.dll", e)

        self.deviceType = 3
        self.deviceIndex = 0
        self.canIndex = 0

        self.alive = False    #判断CAN总线是否在线

        self.vic = _VCI_INIT_CONFIG()
        self.vic.AccCode = 0x00000000
        self.vic.AccMask = 0xFFFFFFFF
        self.vic.Filter = 0
        self.vic.Timing0 = 0x00
        self.vic.Timing1 = 0x1c
        self.vic.Mode = 0
        self.vco_send = VCI_CAN_OBJ()
        self.vco_rec = VCI_CAN_OBJ()

    def opendevice(self):
        self.canlib.OpenDevice(self.deviceType, self.deviceIndex, self.canIndex)
        if self.canlib.OpenDevice(self.deviceType, self.deviceIndex, self.canIndex) == 1:
            print('Device open Success')
        else:
            print('Device open ERROR')

    def closedevice(self):
        self.canlib.CloseDevice(self.deviceType, self.deviceIndex)
        if self.canlib.CloseDevice(self.deviceType, self.deviceIndex) == 1:
            self.alive = False
            print('Device close Success')
        else:
            print('Device close ERROR')

    def initdevice(self):
        try:
            self.canlib.InitCAN(self.deviceType, self.deviceIndex, self.canIndex, pointer(self.vic))
            if self.canlib.InitCAN(self.deviceType, self.deviceIndex, self.canIndex, pointer(self.vic)) == 1:
                print('Device init success')
            else:
                print('Device init fail')
        except  Exception as e:
            print(e)

    def startcan(self):
        try:
            self.canlib.StartCAN(self.deviceType, self.deviceIndex, self.canIndex)
            if self.canlib.StartCAN(self.deviceType, self.deviceIndex, self.canIndex) == 1:
                self.alive = True
                print('CAN start success')
            else:
                print('CAN start fail')
        except Exception as e:
            print(e)

    def resetcan(self):
        try:
            self.canlib.ResetCAN(self.deviceType, self.deviceIndex, self.canIndex)
            if self.canlib.ResetCAN(self.deviceType, self.deviceIndex, self.canIndex) == 1:
                print('CAN reset success')
            else:
                print('CAN reset fail')
        except Exception as e:
            print(e)

    def transmit(self, id, send_type, len, InputData):
        self.vco_send.ID = id
        self.vco_send.RemoteFlag = 0
        self.vco_send.ExternFlag = 0
        self.vco_send.SendType = send_type
        self.vco_send.DataLen = len
        self.vco_send.Data = InputData
        pointer(self.vco_send)

        try:
            self.canlib.Transmit(self.deviceType, self.deviceIndex, self.canIndex,byref(self.vco_send), self.vco_send.DataLen)
            if self.canlib.Transmit(self.deviceType, self.deviceIndex, self.canIndex,byref(self.vco_send), self.vco_send.DataLen) == 0:
                print('Transmit data fail')
            else:
                print('Transmit data success')
        except Exception as e:
            print(e)








