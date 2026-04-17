"""
%%%%%%%%%*%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%!
% FILE ........... noise_analyzer.ino                                        %
% LANGUAGE ....... Python                                                    %
% DESCRIPTION .... reads a noise signal from serial port, writes it on       %
                   a .txt file, extract data and plots it. It then verifies  %
                   if signal has gaussian distribution.                      %
% PLATFORM ....... Arduino UNO R4 Wi-Fi                                      %
% LINK-FILEs ..... none                                                      %
% DATE ........... Apr/17/2024                                               %
% LAST-MFD ....... Apr/17/2024                                               %
% CREATED by ..... Group A1                                                 %
%%%%%%%%%*%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%!
"""

import serial
import matplotlib.pyplot as plt
import numpy as np
import time

# parameters
input_duration = 10 # secs
bin_ratio = 0.004
serial_port = '/dev/tty.usbmodemB081849E6E302'# to see the serial input, write on terminal 'ls /dev/tty.*'
ser = serial.Serial(serial_port, 2000000)

time.sleep(1)

t0 = time.time()
with open('data.txt', 'w', newline='') as f:
    while time.time() - t0 < input_duration:
        linea = ser.readline().decode('utf-8')
        f.write(linea)
        #print(linea)

noise = np.loadtxt("data.txt")
noise = noise[1::]

print(len(noise))
noise_mean = np.mean(noise)
print("Offset:", noise_mean)
noise = noise - noise_mean

plt.hist(noise, bins=round(bin_ratio * len(noise)))
plt.show()

