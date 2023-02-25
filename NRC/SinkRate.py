import numpy as np  
import matplotlib.pyplot as plt
import csv

w = 1.4
p = 1.225
s = 0.036
Cla = 0.62
Ar = 10
a = 3.01
a0 = 3
Cd = 0
Cl =  0
angle = []
speed = []
d = 0.016

a0 = a0 * np.pi/180

for i in range(1000):

    a = 0
    a = 3.3 + i * 0.01
    angle.append(a)
    print(a)

    a = a * np.pi/180

    if(a != a0):

        Cl = Cla * (a - a0)

        Cd = ((1+d)*(Cl**2))/(np.pi*Ar)

        Cd = Cd + 0.0325

        v = np.sqrt(2*w/p*s) * (Cd/(Cl**(3/2)))

        speed.append(v)
        print(Cl)
        print(Cd)
        print(v)

    else:

        a = angle.pop()


plt.plot(angle,speed)
plt.show()