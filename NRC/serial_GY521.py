import serial
import time
import matplotlib.pyplot as plt

#establish serial connection to Arduino/GY521
ser1 = serial.Serial('COM26', 38400) #Baud rate 38400 Hz, COM port must match.
ser1.flushInput()
for i in range(0,3):
    print(ser1.readline(100).decode("utf-8","ignore").replace('\r\n',''))

res = 2**16;
# sensitivity setting
a_sen = 2* 9.81; #m/s^2
g_sen = 250 ; #deg/s

ax = []
ay = []
az = []
gx = []
gy = []
gz = []
t  = []

#main loop
try:
    print("Capturing data, press ctrl+C to finish")

    #obtain data
    while 1:
        s = ser1.readline(100)
        #print(s)
        ss = s.decode("utf-8","ignore").replace('\r\n','').split('\t')
        ss = ss[1:]
        ax.append(ss[0])
        ay.append(ss[1])
        az.append(ss[2])
        gx.append(ss[3])
        gy.append(ss[4])
        gz.append(ss[5])
        t.append(ss[6])

        
except KeyboardInterrupt:
    print('Stopping...')

    #convert the read values into physical values
    ax = [int(i)*a_sen*2 / res for i in ax]
    ay = [int(ay[i])*a_sen*2 / res if i < len(ay) else int(ss[1])*a_sen*2 / res for i in range(len(ax))]
    az = [int(az[i])*a_sen*2 / res if i < len(az) else int(ss[2])*a_sen*2 / res for i in range(len(ax))]
    gx = [int(gx[i])*g_sen*2 / res if i < len(gx) else int(ss[3])*g_sen*2 / res for i in range(len(ax))]
    gy = [int(gy[i])*g_sen*2 / res if i < len(gy) else int(ss[4])*g_sen*2 / res for i in range(len(ax))]
    gz = [int(gz[i])*g_sen*2 / res if i < len(gz) else int(ss[5])*g_sen*2 / res for i in range(len(ax))]
    t = [int(t[tm])/1000 if i < len(t) else int(ss[6])/1000 for tm in range(len(ax))]

    #write the data to a text file
    timestr = time.strftime("%Y%m%d_%H%M%S")    
    f = open(timestr + '_Data.txt','w')
    f.write('Time\tax\tay\taz\tgx\gy\gz\n')
    for i in range(len(ax)):
        f.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (t[i],ax[i],ay[i],az[i],gx[i],gy[i],gz[i]))
    f.close()

    ser1.close()
    
    
    plt.figure(1)
    plt.subplot(211)
    plt.plot(t,ax,'r',t,ay,'g',t,az,'b')
    plt.ylabel('Accel (m/s^2)')
    plt.legend(['x','y','z'],loc = 'center left',bbox_to_anchor=(1.0, 0.5))
        
    plt.subplot(212)
    plt.plot(t,gx,'r',t,gy,'g',t,gz,'b')
    plt.xlabel('Time s')
    plt.ylabel('Ang vel (deg/s)')
    plt.legend(['x','y','z'],loc = 'center left',bbox_to_anchor=(1.0, 0.5))

    
    print('Done')
    plt.show()

