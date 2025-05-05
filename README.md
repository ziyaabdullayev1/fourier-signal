# Fourier Signal Synthesizer GUI

This Python project visualizes:
1. Three user-defined sinusoidal/cosine signals and their synthesis.
2. A Fourier Series approximation using user-defined a₀, aₖ, bₖ coefficients.

Includes an interactive Tkinter-based GUI.

## Features
- Signal-by-signal input of amplitude, frequency, phase, type (sin/cos)
- Realtime plotting of individual signals + their sum
- Fourier series visualization using k=1..3 components

## Run Instructions
```bash
pip install -r requirements.txt
python signal_gui.py
