from pylab import *
from matplotlib.animation import FuncAnimation

class animationClass():
    def __init__(self, canvas, ui):
        self.ui = ui
        self.canvas = canvas
        self.y_speed1 = []
        self.y_speed2 = []
        self.y_currentA = []
        self.y_currentB = []
        self.y_currentC = []
        self.dc1 = []
        self.dc2 = []
        self.x_time = []
        self.x_time1 = []
        self.x_time2 = []
        self.on_start()

    def update_line(self, i):
        self.y_speed1 = []
        self.y_speed2 = []
        self.y_currentA = []
        self.y_currentB = []
        self.y_currentC = []
        self.dc1 = []
        self.dc2 = []
        self.x_time = []
        self.x_time1 = []
        self.x_time2 = []
        try:
            with open('current.txt', 'r') as f,  open('speed.txt', 'r') as f2, open('dc.txt', 'r') as f3:
                data = f.read()
                data1 = f2.read()
                data2 = f3.read()
                lines = data.split('\n')
                lines2 = data1.split('\n')
                lines3 = data2.split('\n')
                for line in lines:
                    if len(line) > 1:
                        current_a, current_b, current_c, time = line.split(',')
                        self.y_currentA.append(float(current_a))
                        self.y_currentB.append(float(current_b))
                        self.y_currentC.append(float(current_c))
                        self.x_time.append(float(time))
                for line in lines2:
                    if len(line) > 1:
                        speed1, speed2, time1 = line.split(',')
                        self.y_speed1.append(float(speed1))
                        self.y_speed2.append(float(speed2))
                        self.x_time1.append(float(time1))
                for line in lines3:
                    if len(line) > 1:
                        dc1, dc2, time2 = line.split(',')
                        self.dc1.append(float(dc1))
                        self.dc2.append(float(dc2))
                        self.x_time2.append(float(time2))
        except:
            pass

        self.canvas.ax1.plot(self.x_time, self.y_currentA, 'r', linewidth=0.5)#label='A相'
        #self.canvas.ax1.legend(loc='best')#loc='best'
        #self.canvas.ax1.plot(self.x_time, self.y_currentB, 'g', linewidth=0.5)
        #self.canvas.ax1.plot(self.x_time, self.y_currentC, 'y', linewidth=0.5)

        self.canvas.ax2.plot(self.x_time2, self.dc1, 'r', linewidth=1)
        self.canvas.ax2.plot(self.x_time2, self.dc2, 'b', linewidth=1)

        self.canvas.ax3.plot(self.x_time1, self.y_speed1, 'k', linewidth=1.5, linestyle='--')
        self.canvas.ax3.plot(self.x_time1, self.y_speed2, 'b', linewidth=1.5)

    def on_start(self):

        self.ani = FuncAnimation(self.canvas.figure, self.update_line, interval=800, repeat=False)