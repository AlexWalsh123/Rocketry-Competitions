import csv
import random
import time
import numpy as np
import scipy.integrate

start_time = time.time()

ax = [30]
vx = [0]
tt = [0]

deltaT = 0

x_value = 0
total_1 = 0
total_2 = 0

peaked = False

end_time = time.time()

Flying = True


#caculate with new daat
#make deltT deltT  can do that now?


fieldnames = ["x_value", "total_1", "total_2"]


with open('data.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

while Flying:

    with open('data.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)      

        try:
            info = {
                "x_value": tt[-1],  
                "total_1": px[-1],          
                "total_2": total_2
            }
        except:
            info = {
                "x_value": tt[-1],  
          
                "total_2": total_2
            }


        csv_writer.writerow(info)

        x_value += 1

        try:          
            if(px[-1] > 1000):

                peaked = True
        except:

            pass

        if(peaked == False):

            ax.append(ax[-1] + random.uniform(-1, 1))

        elif(peaked):

            ax.append(-9.81 + random.uniform(-1, 1))

        if(peaked and px[-1] < 0 ):

            Flying = False

        start_time1 = time.time()
        deltaT = start_time1 - end_time
        end_time = time.time()
        print(deltaT)
        vx = scipy.integrate.cumtrapz(ax, None, 0.01)
        px = scipy.integrate.cumtrapz(vx, None, 0.01)

        tt.append(time.time() - start_time)

    time.sleep(0.01)