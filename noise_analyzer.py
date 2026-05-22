"""
%%%%%%%%%*%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%!
% FILE ........... noise_analyzer.py                                         %
% LANGUAGE ....... Python                                                    %
% DESCRIPTION .... extract signal's data from a .txt file and verifies if    %
                   signal has gaussian distribution.                         %
% PLATFORM ....... Arduino UNO R4 Wi-Fi                                      %
% LINK-FILEs ..... none                                                      %
% DATE ........... Apr/17/2026                                               %
% LAST-MFD ....... May/19/2026                                               %
% CREATED by ..... Group A1                                                  %
%%%%%%%%%*%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%!
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats, fft

# parameters
num_bins = 20


def generate_and_show_password(noise_signal, length=20):
    import hashlib
    import secrets
    import string

    # 1. Generazione (Logica invariata)
    noise_data_bytes = noise_signal.tobytes()
    seed = hashlib.sha256(noise_data_bytes).digest()
    rng = secrets.SystemRandom(seed)
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(rng.choice(chars) for _ in range(length))

    # 2. Output Console ad alta visibilità
    print("\n" + "!" * 60)
    print(" G E N E R A T E D   P A S S W O R D ")
    print("!" * 60)
    print(f"\n   {password}\n")
    print("!" * 60 + "\n")

def plot_noise(noise, noise_duration_in_sec, block_size=500):
    # Parameters
    noise_length = len(noise)
    t = np.linspace(0, noise_duration_in_sec, noise_length)
    fs = noise_length / noise_duration_in_sec  # Frequenza di campionamento reale

    # Configurazione Grafici (3 sotto-grafici anziché 2 per mostrarti la differenza)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7))

    # 1. TIME DOMAIN
    ax1.plot(t, noise, color='royalblue', lw=0.8)
    # NOTA: Se l'asse X usa il tempo 't', l'etichetta corretta è 'Time (s)', non 'Samples'
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Amplitude')
    ax1.set_title('Noise in Time Domain')
    ax1.grid(True, alpha=0.4)

    # 2. FREQUENCY DOMAIN (FFT Standard intera - per confronto)
    # Corretta la normalizzazione: la divisione per fs nel calcolo della FFT non serve per lo spettro di ampiezza.
    fft_signal = fft.fft(noise)
    freqs = fft.fftfreq(noise_length, 1 / fs)

    half_len = noise_length // 2
    positive_freqs = freqs[:half_len]
    # La normalizzazione corretta per l'ampiezza è dividere per il numero di punti N
    magnitude = 2 * np.abs(fft_signal[:half_len]) / noise_length

    ax2.plot(positive_freqs, magnitude, color='indianred', lw=0.6)
    ax2.set_xlabel('Frequency (Hz)')
    ax2.set_ylabel('Magnitude')
    ax2.set_title('Standard FFT (Full Signal - Very Noisy)')
    ax2.grid(True, alpha=0.4)

    plt.tight_layout()
    plt.show()

def analyze_data(file, noise_duration_in_sec):
    try:
        noise = np.loadtxt(file)
    except Exception as e:
        print(f"Error loading file: {e}")
        return

    noise = noise[1::] # first value could be wrong (really high) due to buffer problems
    plot_noise(noise, noise_duration_in_sec)

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

    generate_and_show_password(noise, length=20)

if __name__ == "__main__":
    analyze_data('data.txt', 5)
