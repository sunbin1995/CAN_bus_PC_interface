import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# 设置三维坐标
fig = plt.figure()
ax = Axes3D(fig)
ax1 = fig
bandwidth1 = []
z1 = []
x_time = []

bandwidth2 = []
z2 = []
x_time1 = []

bandwidth3 = []
z3 = []
x_time2 = []
with open('speed1.txt', 'r') as f, open('speed2.txt', 'r') as f2, open('speed3.txt', 'r') as f3:
    data = f.read()
    data1 = f2.read()
    data2 = f3.read()
    lines = data.split('\n')
    lines2 = data1.split('\n')
    lines3 = data2.split('\n')
    for line in lines:
        if len(line) > 1:
            x1, speed,  time = line.split(',')
            bandwidth1.append(300)
            z1.append(float(speed))
            x_time.append(float(time))

    for line in lines2:
        if len(line) > 1:
            x2, speed1, time1 = line.split(',')
            bandwidth2.append(200)
            z2.append(float(speed1))
            x_time1.append(float(time1))
    for line in lines3:
        if len(line) > 1:
            x3, speed2, time2 = line.split(',')
            bandwidth3.append(100)
            z3.append(float(speed2))
            x_time2.append(float(time2))


# 生成数据
X1 = bandwidth1
X2 = bandwidth2
X3 = bandwidth3

Y1 = x_time
Y2 = x_time1
Y3 = x_time2

Z1 = z1
Z2 = z2
Z3 = z3

# 画3d图
ax.plot(X1, Y1, Z1, 'r', linewidth=2)
ax.plot(X2, Y2, Z2, 'g', linewidth=2)
ax.plot(X3, Y3, Z3, 'b', linewidth=2)
plt.show()

# 画2d图
plt.figure()
plt.plot(Y1, Z1, 'r', linewidth=1, label='ESO bandwidth=300Hz,')
plt.plot(Y2, Z2, 'g', linewidth=1, label='ESO bandwidth=200Hz')
plt.plot(Y3, Z3, 'b', linewidth=1, label='ESO bandwidth=100Hz')
plt.legend(loc='lower right')
plt.show()