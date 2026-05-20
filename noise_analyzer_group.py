"""
%%%%%%%%%*%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%!
% FILE ........... noise_analyzer.py                                         %
% LANGUAGE ....... Python                                                    %
% DESCRIPTION .... extract signal's data from a .txt file and verifies if    %
                   the partitions of the signal (groups) have gaussian       %
                   distribution.                                             %
% PLATFORM ....... Arduino UNO R4 Wi-Fi                                      %
% LINK-FILEs ..... none                                                      %
% DATE ........... Apr/17/2026                                               %
% LAST-MFD ....... May/19/2026                                               %
% CREATED by ..... Group A1                                                  %
%%%%%%%%%*%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%!
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from noise_analyzer import plot_noise

# parameters
num_bins = 20

def compute_group_analysis(noise):
    # parameters
    numSamples = 500
    noiseLength = len(noise)
    numGroups = noiseLength // numSamples

    print("\n" + "=" * 40)
    print("       STATISTICAL ANALYSIS RESULTS")
    print("=" * 40)
    print(f"Number of samples per group: {numSamples}")
    print(f"Number of groups: {numGroups}")

    bestStartIndex = 0
    bestEndIndex = 0
    best_sw_p = 0

    for group in range(numGroups):
        startIndex = group * numSamples
        endIndex = min(startIndex + numSamples, noiseLength-1)

        if startIndex == endIndex:
            continue

        noise_portion = noise[startIndex : endIndex]

        print(f"Group: {group}")

        noise_mean = np.mean(noise_portion)
        noise_std = np.std(noise_portion)
        print(f"Mean (Offset):    {noise_mean:.4f}")
        print(f"Std Deviation:    {noise_std:.4f}")
        print("-" * 40)

        # Shapiro-Wilk Test
        sw_stat, sw_p = stats.shapiro(noise_portion)
        print(f"Shapiro-Wilk:     p-value = {sw_p:.4e}")
        sw_result = "Gaussian" if sw_p > 0.05 else "Not Gaussian"
        print(f"Result (SW):      {sw_result}")
        # update shapiro test
        if sw_p > best_sw_p:
            best_sw_p = sw_p
            bestStartIndex = startIndex
            bestEndIndex = endIndex


        # Chi-Square Normality Test (D'Agostino's K-squared)
        chi_stat, chi_p = stats.normaltest(noise_portion)
        print(f"Chi-Square:       p-value = {chi_p:.4e}")
        chi_result = "Gaussian" if chi_p > 0.05 else "Not Gaussian"
        print(f"Result (Chi2):    {chi_result}")
        print("=" * 40 + "\n")

    return [bestStartIndex, bestEndIndex]

def analyze_data(file, noise_duration_in_sec):
    try:
        noise = np.loadtxt(file)
    except Exception as e:
        print(f"Error loading file: {e}")
        return

    noise = noise[1::] # first value could be wrong (really high) due to buffer problems
    #noise = np.random.normal(loc = 2.5, scale = 2.0, size=len(noise))
    #noise = np.random.uniform(0, 5, size=len(noise))
    plot_noise(noise, noise_duration_in_sec)

    [start, end] = compute_group_analysis(noise)
    noise = noise[start:end]

    print("\n" + "="*40)
    print("       STATISTICAL ANALYSIS RESULTS")
    print("="*40)
    print(f"Number of samples: {len(noise)}")
    
    noise_mean = np.mean(noise)
    noise_std = np.std(noise)
    print(f"Mean (Offset):    {noise_mean:.4f}")
    print(f"Std Deviation:    {noise_std:.4f}")
    print("-" * 40)

    # Shapiro-Wilk Test
    sw_stat, sw_p = stats.shapiro(noise)
    print(f"Shapiro-Wilk:     p-value = {sw_p:.4e}")
    sw_result = "Gaussian" if sw_p > 0.05 else "Not Gaussian"
    print(f"Result (SW):      {sw_result}")

    # Chi-Square Normality Test (D'Agostino's K-squared)
    chi_stat, chi_p = stats.normaltest(noise)
    print(f"Chi-Square:       p-value = {chi_p:.4e}")
    chi_result = "Gaussian" if chi_p > 0.05 else "Not Gaussian"
    print(f"Result (Chi2):    {chi_result}")
    print("="*40 + "\n")

    # Plotting
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    
    # --- SUBPLOT 1: Histogram ---
    # Histogram with density=True to overlay the normal curve
    ax1.hist(noise, bins=num_bins, color='#3498db', edgecolor='white', 
                                alpha=0.7, density=True, label='Observed Data')
    
    # Normal distribution curve for reference
    xmin, xmax = ax1.get_xlim()
    x = np.linspace(xmin, xmax, 500)
    p = stats.norm.pdf(x, noise_mean, noise_std)
    ax1.plot(x, p, color='#e74c3c', linewidth=3, label='Expected Normal Distribution')

    ax1.set_title("Signal Histogram and Normality Analysis", fontsize=14, fontweight='bold')
    ax1.set_xlabel("Amplitude", fontsize=12)
    ax1.set_ylabel("Probability Density", fontsize=12)
    
    # Info text box with results
    info_text = (f"Samples: {len(noise)}\n"
                 f"Mean: {noise_mean:.4f}\n"
                 f"Std Dev: {noise_std:.4f}\n\n"
                 f"Shapiro-Wilk p: {sw_p:.2e}\n"
                 f"({sw_result})\n\n"
                 f"Chi-Square p: {chi_p:.2e}\n"
                 f"({chi_result})")
    
    props = dict(boxstyle='round', facecolor='white', alpha=0.8)
    ax1.text(0.95, 0.95, info_text, transform=ax1.transAxes, fontsize=10,
                   verticalalignment='top', horizontalalignment='right', bbox=props)

    ax1.legend(loc='upper left')
    ax1.grid(True, linestyle='--', alpha=0.5)

    # --- SUBPLOT 2: Normal Probability Plot ---
    stats.probplot(noise, dist="norm", plot=ax2)
    ax2.set_title("Normal Probability Plot", fontsize=14, fontweight='bold')
    ax2.set_xlabel("Theoretical Quantiles", fontsize=12)
    ax2.set_ylabel("Ordered Values", fontsize=12)
    ax2.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    analyze_data('data.txt', 1)
