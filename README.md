# Noise Analyzer — Group A1

A two-part project that acquires an analog noise signal from an Arduino UNO R4 Wi-Fi, streams it to a PC via serial port, and analyzes its statistical distribution in Python.

[Click here to watch video](https://youtu.be/NcE-0FtHAWY)

---

## Project Structure

```
noise_analyzer/
├── noise_reader.ino      # Arduino sketch — acquires and streams ADC samples
├── noise_writer.py       # Python script — records samples from serial port to file, then triggers analysis
├── noise_analyzer.py     # Python module — loads data from file, plots histogram
├── data.txt              # Auto-generated — raw voltage samples
└── README.md
```

---

## How It Works

```
Arduino UNO R4 Wi-Fi          USB / Serial (2 Mbaud)          PC (Python)
        │                                                           │
  analogRead(A0)  ──────────────── voltage string ───────────►  noise_writer.py
  convert to V                                                   saves to data.txt
  Serial.println()                                                    │
                                                               noise_analyzer.py
                                                                plots histogram
```

1. Arduino samples pin **A0** at 14-bit resolution and converts the raw integer to voltage.
2. Each sample is sent as a decimal string over the serial port at **2 000 000 baud**.
3. `noise_writer.py` reads the serial stream for a configurable duration and saves the samples to `data.txt`. Once acquisition is complete, it automatically calls `analyze_data()` from `noise_analyzer.py`.
4. `noise_analyzer.py` loads the file, removes the DC offset, and plots a histogram to verify whether the noise follows a **Gaussian distribution**.

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
  pip install pyserial matplotlib numpy scipy
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
Look for something like `/dev/tty.usbmodemXXXXXX` and update `serial_port` in `noise_writer.py`.

On **Windows** the port will be `COM3`, `COM4`, etc. (visible in Device Manager).

### 3 — Configure parameters

**`noise_writer.py`**

| Parameter | Default | Description |
|---|---|---|
| `input_duration` | `10` | Acquisition time in seconds |
| `serial_port` | `/dev/tty.usbmodemB081849E6E302` | Serial port of the Arduino |
| `output_file` | `data.txt` | Output file path |

**`noise_analyzer.py`**

| Parameter | Default | Description |
|---|---|---|
| `num_bins` | `20` | Number of histogram bins |

### 4 — Run

Only `noise_writer.py` needs to be launched — it automatically calls the analyzer when acquisition is complete:

```bash
python3 noise_writer.py
```

The script will:
1. Acquire samples for `input_duration` seconds
2. Save them to `data.txt`
3. Print the number of samples and the DC offset
4. Display a histogram of the signal

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
- **Histogram plot** — distribution of the signal; a bell curve indicates Gaussian distribution

---

## Notes

- The first sample in `data.txt` is discarded inside `analyze_data()` (`noise[1::]`) to avoid a corrupted reading at startup.
- The high baud rate (2 Mbaud) maximizes the sampling rate. Make sure your USB driver supports it.
- On macOS, if Python throws `[Errno 16] Resource busy`, the Arduino IDE is still holding the port — close it completely before running the script.
- `noise_analyzer.py` can also be used standalone by calling `analyze_data("your_file.txt")` directly, making it reusable with any previously recorded dataset.

---

## Authors

Group A1 — April 2024
