# Gaussian Noise Analyzer — Group A1

A two-part project that acquires an analog noise signal from an Arduino UNO R4 Wi-Fi, streams it to a PC via serial port, and analyzes its statistical distribution in Python.

---

## Project Structure

```
noise_analyzer/
├── noise_reader.ino      # Arduino sketch — acquires and streams ADC samples
├── noise_analyzer.py     # Python script — records, plots, and analyzes the signal
├── data.txt              # Auto-generated — raw voltage samples
└── README.md
```

---

## How It Works

```
Arduino UNO R4 Wi-Fi          USB / Serial (2 Mbaud)          PC (Python)
        │                                                           │
  analogRead(A0)  ──────────────── voltage string ───────────►  readline()
  convert to V                                                  save to file
  Serial.println()                                              plot histogram
                                                                Gaussian check
```

1. Arduino samples pin **A0** at 14-bit resolution and converts the raw integer to voltage.
2. Each sample is sent as a decimal string over the serial port at **2 000 000 baud**.
3. Python reads the serial stream for a configurable duration, saves the samples to `data.txt`, removes the DC offset, and plots a histogram to verify whether the noise follows a **Gaussian distribution**.

---

## Requirements

### Hardware
- Arduino UNO R4 Wi-Fi
- USB-A to USB-C cable
- Signal source connected to pin **A0**

### Software
- Arduino IDE (to compile and upload the sketch)
- Python 3.x
- Python libraries:
  ```bash
  pip install pyserial matplotlib numpy
  ```

---

## Setup & Usage

### 1 — Upload the Arduino sketch
1. Open `noise_reader.ino` in the Arduino IDE.
2. Select board: **Arduino UNO R4 Wi-Fi**.
3. Click **Upload**.
4. **Close the Arduino IDE completely** (or at least the Serial Monitor) — the serial port must be free for Python.

### 2 — Find the serial port (macOS / Linux)
```bash
ls /dev/tty.*
```
Look for something like `/dev/tty.usbmodemXXXXXX` and update `serial_port` in `noise_analyzer.py`.

On **Windows** the port will be `COM3`, `COM4`, etc. (visible in Device Manager).

### 3 — Configure Python parameters

Open `noise_analyzer.py` and adjust the parameters at the top of the file:

| Parameter | Default | Description |
|---|---|---|
| `input_duration` | `10` | Acquisition time in seconds |
| `bin_ratio` | `0.004` | Controls histogram bin count (`bins = bin_ratio × N_samples`) |
| `serial_port` | `/dev/tty.usbmodemB081849E6E302` | Serial port of the Arduino |

### 4 — Run Python
```bash
python3 noise_analyzer.py
```

The script will:
- Acquire samples for `input_duration` seconds
- Save them to `data.txt`
- Print the number of samples and the DC offset
- Display a histogram of the zero-mean signal

---

## Arduino Sketch — Key Parameters

| Constant | Value | Description |
|---|---|---|
| `PIN_READ` | `A0` | Analog input pin |
| `BAUD_RATE` | `2 000 000` | Serial baud rate |
| `DELAY_DURATION` | `1 ms` | Delay between samples |
| `ANALOG_READ_RESOLUTION` | `14 bit` | ADC resolution (0 – 16383) |
| `MAX_VOLTAGE` | `4.807 V` | Reference voltage for conversion |
| `DIGIT_PRECISION` | `10` | Decimal digits sent over serial |

Voltage conversion formula:

```
V = (raw_value / (2^14 - 1)) × 4.807
```

---

## Output

- **`data.txt`** — one voltage sample per line (overwritten at each run)
- **Histogram plot** — distribution of the zero-mean noise signal; a bell curve indicates Gaussian distribution

---

## Notes

- The first sample in `data.txt` is discarded (`noise = noise[1::]`) to avoid a corrupted reading at startup.
- The high baud rate (2 Mbaud) maximizes the sampling rate. Make sure your USB driver supports it.
- On macOS, if Python throws `[Errno 16] Resource busy`, the Arduino IDE is still holding the port — close it completely before running the script.

---

## Authors

Group A1 — April 2024
