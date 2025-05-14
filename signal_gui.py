import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def generate_signal(A, f, phase, t, signal_type='cos'):
    """Generate a sine or cosine signal."""
    w = 2 * np.pi * f
    if signal_type == 'sin':
        return A * np.sin(w * t + phase)
    return A * np.cos(w * t + phase)

# Main window
form = tk.Tk()
form.geometry("1300x750")
form.title("Signal Synthesizer and Fourier Series GUI")

# Frame for plots
graphics_frame = tk.Frame(form)
graphics_frame.grid(row=0, column=0, rowspan=5, padx=10, pady=10, sticky="nsew")

# Create input frames for 3 signals
signal_frames = []
for i in range(3):
    frame = tk.LabelFrame(form, text=f"{i+1}. Sinyal Değerleri", bg="#f0f0f0")
    frame.grid(row=i, column=1, padx=10, pady=5, sticky="n")
    signal_frames.append(frame)

# Frame for sum signal and DC component
signal_sum = tk.LabelFrame(form, text="Toplam Sinyal ve DC Bileşeni", bg="#f0f0f0")
signal_sum.grid(row=3, column=1, padx=10, pady=5, sticky="n")

# Entries and dropdowns for each signal
entries = []     # list of (amp_entry, freq_entry, phase_entry)
var_types = []   # list of StringVar for 'sin'/'cos'
for frame in signal_frames:
    tk.Label(frame, text="Genlik:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
    amp = tk.Entry(frame, width=10)
    amp.grid(row=0, column=1, padx=5, pady=2)
    amp.insert(0, "0")

    tk.Label(frame, text="Frekans (Hz):").grid(row=1, column=0, sticky="w", padx=5, pady=2)
    freq = tk.Entry(frame, width=10)
    freq.grid(row=1, column=1, padx=5, pady=2)
    freq.insert(0, "0")

    tk.Label(frame, text="Faz (°):").grid(row=2, column=0, sticky="w", padx=5, pady=2)
    ph = tk.Entry(frame, width=10)
    ph.grid(row=2, column=1, padx=5, pady=2)
    ph.insert(0, "0")

    tk.Label(frame, text="Tip:").grid(row=0, column=2, sticky="w", padx=5, pady=2)
    var = tk.StringVar(value='cos')
    ttk.OptionMenu(frame, var, 'cos', 'sin', 'cos').grid(row=0, column=3, padx=5, pady=2)

    entries.append((amp, freq, ph))
    var_types.append(var)

# DC component input
tk.Label(signal_sum, text="DC Bileşen (a0):").grid(row=0, column=0, sticky="w", padx=5, pady=2)
entry_a0 = tk.Entry(signal_sum, width=10)
entry_a0.grid(row=0, column=1, padx=5, pady=2)
entry_a0.insert(0, "0")

# Labels to display sum signal properties
tk.Label(signal_sum, text="Genlik:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
sumA = tk.Label(signal_sum, text="0")
sumA.grid(row=1, column=1, sticky="w")

tk.Label(signal_sum, text="Frekans:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
sumf = tk.Label(signal_sum, text="0")
sumf.grid(row=2, column=1, sticky="w")

tk.Label(signal_sum, text="Faz:").grid(row=3, column=0, sticky="w", padx=5, pady=2)
sumtheta = tk.Label(signal_sum, text="0")
sumtheta.grid(row=3, column=1, sticky="w")

def draw():
    # Read inputs
    amps, freqs, phases, types = [], [], [], []
    for (amp_e, freq_e, ph_e), var in zip(entries, var_types):
        amps.append(float(amp_e.get()))
        freqs.append(float(freq_e.get()))
        # convert degrees to radians
        phases.append(float(ph_e.get()) * np.pi / 180)
        types.append(var.get())

    a0_val = float(entry_a0.get())
    # Time axis
    t = np.linspace(-2, 2, 1000)

    # Generate individual signals
    y_list = [
        generate_signal(A, f, phi, t, signal_type=typ)
        for A, f, phi, typ in zip(amps, freqs, phases, types)
    ]

    # Sum with DC component
    y_sum = a0_val + sum(y_list)

    # Compute sum properties
    ampl_sum = (np.max(y_sum) - np.min(y_sum)) / 2
    freq_sum = freqs[0] if freqs else 0
    phase_sum = np.arctan2(
        sum(A * np.sin(phi) for A, phi in zip(amps, phases)),
        sum(A * np.cos(phi) for A, phi in zip(amps, phases))
    )
    phase_sum_deg = np.degrees(phase_sum)

    # Update labels
    sumA.config(text=f"{ampl_sum:.2f}")
    sumf.config(text=f"{freq_sum:.2f}")
    sumtheta.config(text=f"{phase_sum_deg:.2f}")

    # Clear previous plot
    for widget in graphics_frame.winfo_children():
        widget.destroy()

    # Create figure & subplots
    fig = Figure(figsize=(10, 6), dpi=100)
    ax1 = fig.add_subplot(411)
    ax1.plot(t, y_list[0]); ax1.set_title("Sinyal 1"); ax1.grid(True)
    ax2 = fig.add_subplot(412)
    ax2.plot(t, y_list[1]); ax2.set_title("Sinyal 2"); ax2.grid(True)
    ax3 = fig.add_subplot(413)
    ax3.plot(t, y_list[2]); ax3.set_title("Sinyal 3"); ax3.grid(True)
    ax4 = fig.add_subplot(414)
    ax4.plot(t, y_sum, color="red"); ax4.set_title("Toplam Sinyal"); ax4.grid(True)

    # Embed in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=graphics_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

# Draw button
tk.Button(form, text="Çizdir", command=draw).grid(row=5, column=1, pady=10)

def open_fourier():
    win = tk.Toplevel(form)
    win.title("Fourier Serisi Girdileri")

    ent_a, ent_b = [], []
    for i in range(3):
        tk.Label(win, text=f"a{i+1}:").grid(row=i, column=0, padx=5, pady=2)
        ea = tk.Entry(win, width=10); ea.grid(row=i, column=1); ea.insert(0, "0")
        ent_a.append(ea)

        tk.Label(win, text=f"b{i+1}:").grid(row=i, column=2, padx=5, pady=2)
        eb = tk.Entry(win, width=10); eb.grid(row=i, column=3); eb.insert(0, "0")
        ent_b.append(eb)

    tk.Label(win, text="a0:").grid(row=3, column=0, padx=5, pady=2)
    ea0 = tk.Entry(win, width=10); ea0.grid(row=3, column=1); ea0.insert(0, "0")

    tk.Label(win, text="ω0 (rad/s):").grid(row=3, column=2, padx=5, pady=2)
    ew0 = tk.Entry(win, width=10); ew0.grid(row=3, column=3); ew0.insert(0, "6.28")

    def convert():
        a0c = float(ea0.get())
        w0c = float(ew0.get())

        # Convert coefficients to amplitude/phase and update main GUI
        for i, (ea, eb) in enumerate(zip(ent_a, ent_b)):
            ak = float(ea.get()); bk = float(eb.get())
            A_val = np.hypot(ak, bk)
            phi = np.arctan2(-bk, ak)
            # Update entries
            entries[i][0].delete(0, tk.END)
            entries[i][0].insert(0, f"{A_val:.2f}")
            entries[i][1].delete(0, tk.END)
            entries[i][1].insert(0, f"{w0c:.2f}")
            entries[i][2].delete(0, tk.END)
            entries[i][2].insert(0, f"{np.degrees(phi):.2f}")

        # Update DC component
        entry_a0.delete(0, tk.END)
        entry_a0.insert(0, f"{a0c:.2f}")
        win.destroy()

    tk.Button(win, text="Fourier Dönüştür", command=convert).grid(row=4, columnspan=4, pady=10)

# Button to open Fourier input window
fourier_btn_frame = tk.Frame(form)
fourier_btn_frame.grid(row=4, column=1, pady=10)
tk.Button(fourier_btn_frame, text="Sin-Cos Formu", command=open_fourier).pack()

# Start GUI event loop
form.mainloop()
