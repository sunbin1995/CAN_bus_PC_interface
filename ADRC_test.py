
from math import *
import numpy as np
import matplotlib.pyplot as plt


def fal(e, alfa, delta):

    s = (np.sign(e+delta)-np.sign(e-delta))/2.0
    fal_out = e * s/(pow(delta,1-alfa))+pow(abs(e),alfa)*np.sign(e)*(1-s)
    return fal_out


def fsg(x, d):

    fsg_out = (np.sign(x+d) - np.sign(x-d))/2.0
    return fsg_out


def fhan(x1, x2, r, h0):

    d = r * h0 * h0
    a0 =h0 * x2
    y =x1+a0
    a1 = sqrt(d * (d + 8 * abs(y)))
    a2 = a0 + np.sign(y) * (a1-d)/2.0
    a = (a0 + y) * fsg(y, d) + a2 * (1 - fsg(y, d))
    fhan_out = -1 * r * (a / d) * fsg(a, d) - r * np.sign(a) * (1 - fsg(a, d))
    return fhan_out


h = 0.001
N = 10000
x1 = np.zeros(N)
x2 = np.zeros(N)
xx1 = np.zeros(N)
xx2 = np.zeros(N)
v11 = np.zeros(N)
v12 = np.zeros(N)
v21 = np.zeros(N)
v22 = np.zeros(N)
z11 = np.zeros(N)
z12 = np.zeros(N)
z13 = np.zeros(N)
z21 = np.zeros(N)
z22 = np.zeros(N)
z23 = np.zeros(N)
t = np.zeros(N)
u1 = np.zeros(N)
u2 = np.zeros(N)
uu1 = np.zeros(N)
uu2 = np.zeros(N)
y1 = np.zeros(N)
y2 = np.zeros(N)
f1 = np.zeros(N)
f2 = np.zeros(N)
y1_set = np.zeros(N)
y2_set = np.zeros(N)

BB = np.zeros([2, 2])

b11 = 3
b12 = 1
b21 = 3
b22 = 2

r = 100
r0 = 2

b01 = 100
b02 = 500
b03 = 3000


h1 = 0.1
c = 1.0


y1_star = 2
y2_star = 1



for i in range(N-1):
    t[i] = i * h    # 时间轴

    #y1_set[i] = cos(t[i])
    #y2_set[i] = 2 * sin(t[i])

    fh = fhan(v11[i] - y1_star, v12[i], r0, h)
    # fh = fhan[v11[i] - y1_set[i], v12[i], r0, h]
    v11[i + 1] = v11[i] + h * v12[i]
    v12[i + 1] = v12[i] + h * fh

    e = z11[i] - y1[i]
    fe = fal(e, 0.5, h)
    fe1 = fal(e, 0.25, h)

    z11[i + 1] = z11[i] + h * (z12[i] - b01 * e)
    z12[i + 1] = z12[i] + h * (z13[i] - b02 * fe + u1[i])
    z13[i + 1] = z13[i] + h * (-b03 * fe1)

    e1 = v11[i] - z11[i]
    e2 = v12[i] - z12[i]

    u1[i + 1] = -fhan(e1, c * e2, r, h1) - z13[i]
'''
    fh = fhan(v21[i] - y2_star, v22[i], r0, h)
    # fh = fhan(v21[i] - y2_set[i], v22[i], r0, h)
    v21[i + 1] = v21[i] + h * v22[i]
    v22[i + 1] = v22[i] + h * fh

    e = z21[i] - y2[i]
    fe = fal(e, 0.5, h)
    fe1 = fal(e, 0.25, h)

    z21[i + 1] = z21[i] + h * (z22[i] - b01 * e)
    z22[i + 1] = z22[i] + h * (z23[i] - b02 * fe + u2[i])
    z23[i + 1] = z23[i] + h * (-b03 * fe1)

    e1 = v21[i] - z21[i]
    e2 = v22[i] - z22[i]
    u2[i + 1] = -fhan(e1, c * e2, r, h1) - z23[i]

    b11 = b11 + 0.5 * cos(t[i])
    b12 = b12 + 0.2 * sin(0.8 * t[i])
    b21 = b21 - 0.6 * sin(0.6 * t[i])
    b22 = b22 + 0.5 * cos(0.7 * t[i])

    bb = b11 * b22 - b12 * b21

    if bb == 0:
        bb = bb + h
    BB = np.array([[b22, -b12],[-b21, b11]])
    BB = BB / float(bb)
    uu1[i] = BB[0, 0] * u1[i] + BB[0, 1] * u2[i]
    uu2[i] = BB[1, 0] * u1[i] + BB[1, 1] * u2[i]

    f1[i] = pow(x1[i] , 2) + pow(x2[i] , 2) + xx1[i] * xx2[i] + np.sign(cos(0.9 * t[i]))
    f2[i] = x1[i] * x2[i] + pow(xx1[i] , 2) + pow(xx2[i] , 2) + sin(0.7 * t[i])
    xx1[i + 1] = xx1[i] + h * (f1[i] + b11 * uu1[i] + b12 * uu2[i])
    xx2[i + 1] = xx2[i] + h * (f2[i] + b21 * uu1[i] + b22 * uu2[i])
    #print f1[i],f2[i]
    x1[i + 1] = x1[i] + h * xx1[i]
    x2[i + 1] = x2[i] + h * xx2[i]
    y1[i + 1] = x1[i + 1]
    y2[i + 1] = x2[i + 1]

i = N-1
t[i] = i * h
f1[i] = pow(x1[i] , 2) + pow(x2[i] , 2) + xx1[i] * xx2[i] + np.sign(cos(0.9 * t[i]))
f2[i] = x1[i] * x2[i] + pow(xx1[i] , 2) + pow(xx2[i] , 2) + sin(0.7 * t[i])
y1_set[i] = cos(t[i])
y2_set[i] = 2 * sin(t[i])
'''
plt.figure('Tarcking_Show')
p1 = plt.subplot(111)
#p2 = plt.subplot(222)
#p3 = plt.subplot(223)
#p4 = plt.subplot(224)

#p1.plot(t,y1,'m',t,v11,'g',linewidth=0.5)
p1.plot(t, v11,'g',t,v12,'b',linewidth=1)
p1.grid(True)
p1.set_xlabel('t',fontsize = 14)
p1.set_ylabel('y',fontsize = 14)
p1.set_title('TD',fontsize = 14)
p1.legend()

'''
p2.plot(t,y2,'m',t,v21,'g',linewidth=0.5)
p2.grid(True)
p2.set_xlabel('t',fontsize = 14)
p2.set_ylabel('y',fontsize = 14)
p2.set_title('Tarcking Performance v22',fontsize = 14)

p3.plot(t,f1,'m',t,z13,'g',linewidth=2)
p3.grid(True)
p3.set_xlabel('t',fontsize = 14)
p3.set_ylabel('y',fontsize = 14)
p3.set_title('ESO Tracking Performance f1',fontsize = 14)


p4.plot(t,f2,'m',t,z23,'g',linewidth=2)
p4.grid(True)
p4.set_xlabel('t',fontsize = 14)
p4.set_ylabel('y',fontsize = 14)
p4.set_title('ESO Tracking Performance f2',fontsize = 14)

plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9,hspace=0.35, wspace=0.3)




dt = 0.001
t = np.arange(0.0, 10.0, dt)
r = np.exp(-t[:1000]/0.05)               # impulse response
x = np.random.randn(len(t))
s = np.convolve(x, r)[:len(x)]*dt  # colored noise

plt.figure('New_test')
# the main axes is subplot(111) by default
plt.plot(t, s)
plt.axis([0, 1, 1.1*np.amin(s), 2*np.amax(s)])
plt.xlabel('time (s)')
plt.ylabel('current (nA)')
plt.title('Gaussian colored noise')
'''
# this is an inset axes over the main axes
'''
a = plt.axes([.65, .6, .2, .2], axisbg='w')
n, bins, patches = plt.hist(s, 400, normed=1)
plt.title('Probability')
plt.xticks([])
plt.yticks([])

# this is another inset axes over the main axes
a = plt.axes([0.2, 0.6, .2, .2], axisbg='w')
plt.plot(t[:len(r)], r)
plt.title('Impulse response')
plt.xlim(0, 0.2)
plt.xticks([])
plt.yticks([])
'''

plt.show()
