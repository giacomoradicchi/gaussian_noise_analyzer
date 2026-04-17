"""
%%%%%%%%%*%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%!
% FILE ........... noise_analyzer.py                                         %
% LANGUAGE ....... Python                                                    %
% DESCRIPTION .... extract signal's data from a .txt file and plots it.      %
                   It then verifies if signal has gaussian distribution.     %
% PLATFORM ....... Arduino UNO R4 Wi-Fi                                      %
% LINK-FILEs ..... none                                                      %
% DATE ........... Apr/17/2024                                               %
% LAST-MFD ....... Apr/17/2024                                               %
% CREATED by ..... Group A1                                                 %
%%%%%%%%%*%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%!
"""

import matplotlib.pyplot as plt
import numpy as np

# parameters
num_bins = 20

def analyze_data(file):
    noise = np.loadtxt(file)
    noise = noise[1::] # first value could be wrong (really high) due to buffer problems

    print("Number of samples:", len(noise))
    noise_mean = np.mean(noise)
    print("Offset:", noise_mean)
    #noise = noise - noise_mean

    plt.hist(noise, bins=num_bins)
    plt.title("Signal's histogram")
    plt.show()

