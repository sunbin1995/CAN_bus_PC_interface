import matplotlib.pyplot as plt

# 设置三维坐标

b1 = []
z1 = []
x_time = []

b2 = []
z2 = []
x_time1 = []

b3 = []
z3 = []
x_time2 = []

b4 = []
z4 = []
x_time3 = []

b5 = []
z5 = []
x_time4 = []
with open('data/position1.txt', 'r') as f, open('data/position2.txt', 'r') as f2, \
        open('data/position3.txt', 'r') as f3,open('data/position4.txt','r')as f4,open('data/position5.txt','r')as f5:
    data = f.read()
    data1 = f2.read()
    data2 = f3.read()
    data3 = f4.read()
    data4 = f5.read()
    lines = data.split('\n')
    lines2 = data1.split('\n')
    lines3 = data2.split('\n')
    lines4 = data3.split('\n')
    lines5 = data4.split('\n')
    for line in lines:
        if len(line) > 1:
            x1, position,  time = line.split(',')
            b1.append(300)
            z1.append(float(position))
            x_time.append(float(time))

    for line in lines2:
        if len(line) > 1:
            x2, position1, time1 = line.split(',')
            b2.append(200)
            z2.append(float(position1))
            x_time1.append(float(time1))
    for line in lines3:
        if len(line) > 1:
            x3, position2, time2 = line.split(',')
            b3.append(100)
            z3.append(float(position2))
            x_time2.append(float(time2))
    for line in lines4:
        if len(line) > 1:
            x4, position3, time3 = line.split(',')
            b4.append(100)
            z4.append(float(position3))
            x_time3.append(float(time3))
    for line in lines5:
        if len(line) > 1:
            x5, position4, time4 = line.split(',')
            b5.append(100)
            z5.append(float(position4))
            x_time4.append(float(time4))



Y1 = x_time
Y2 = x_time1
Y3 = x_time2
Y4 = x_time3
Y5 = x_time4

Z1 = z1
Z2 = z2
Z3 = z3
Z4 = z4
Z5 = z5

# 画2d图
plt.figure()
plt.set_ylim=(0,500)
plt.grid(True)
plt.plot(Y1, Z1, 'r', linewidth=2, label='b0 = 0.5b')
plt.plot(Y2, Z2, 'g', linewidth=2, label='b0 = b')
plt.plot(Y3, Z3, 'b', linewidth=2, label='b0 = 2b')
#plt.plot(Y4, Z4, 'y', linewidth=2, label='b0 = 3b')
#plt.plot(Y5, Z5, 'pink', linewidth=2, label='b0 = 4b')
plt.legend(loc='lower right')
plt.show()