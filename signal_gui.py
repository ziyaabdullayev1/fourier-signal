import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

# Signal generation (sin or cos)
def generate_signal(A, f, phase, t, signal_type='sin'):
    w = 2 * np.pi * f
    return A * np.sin(w * t + phase) if signal_type == 'sin' else A * np.cos(w * t + phase)

# Fourier series signal from coefficients
def generate_fourier_series(a0, ak, bk, w0, t):
    signal = a0 * np.ones_like(t)
    for k in range(1, 4):
        signal += ak[k-1] * np.cos(k * w0 * t) + bk[k-1] * np.sin(k * w0 * t)
    return signal

# Button function: generate plots
def plot_signals():
    try:
        A_vals = [float(e.get()) for e in entries_A]
        f_vals = [float(e.get()) for e in entries_f]
        phase_vals = [float(e.get()) for e in entries_phase]
        signal_types = [v.get() for v in var_signal_type]

        a0 = float(entry_a0.get())
        ak = [float(e.get()) for e in entries_ak]
        bk = [float(e.get()) for e in entries_bk]
        w0 = float(entry_w0.get())

        t = np.linspace(0, 1, 1000)
        signals = []

        fig, axs = plt.subplots(5, 1, figsize=(7, 10))
        fig.tight_layout(pad=3.0)

        # Plot sin/cos signals
        for i in range(3):
            sig = generate_signal(A_vals[i], f_vals[i], phase_vals[i], t, signal_types[i])
            signals.append(sig)
            axs[i].plot(t, sig)
            axs[i].set_title(f'{signal_types[i].capitalize()} Signal {i+1}')
            axs[i].grid(True)

        # Synthesized signal
        synth = sum(signals)
        axs[3].plot(t, synth, color='purple')
        axs[3].set_title('Synthesized Signal (Sum of 3)')
        axs[3].grid(True)

        # Fourier Series
        fourier_signal = generate_fourier_series(a0, ak, bk, w0, t)
        axs[4].plot(t, fourier_signal, color='green')
        axs[4].set_title('Fourier Series Approximation (k=1..3)')
        axs[4].grid(True)

        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.get_tk_widget().grid(row=9, column=0, columnspan=6)
        canvas.draw()

    except ValueError:
        print("Please fill all inputs with valid numbers.")

# === GUI Setup ===
window = tk.Tk()
window.title("Signal Synthesizer and Fourier Series GUI")

entries_A, entries_f, entries_phase, var_signal_type = [], [], [], []

# Inputs for A, f, theta, and type
for i in range(3):
    tk.Label(window, text=f"Signal {i+1} - A, f, θ").grid(row=0, column=i*2, columnspan=2)
    a = tk.Entry(window); a.grid(row=1, column=i*2); entries_A.append(a)
    f = tk.Entry(window); f.grid(row=1, column=i*2 + 1); entries_f.append(f)
    p = tk.Entry(window); p.grid(row=2, column=i*2); entries_phase.append(p)

    var = tk.StringVar(value='sin')
    tk.OptionMenu(window, var, 'sin', 'cos').grid(row=2, column=i*2 + 1)
    var_signal_type.append(var)

# Fourier Coefficient inputs
tk.Label(window, text="Fourier Coefficients: a₀").grid(row=3, column=0)
entry_a0 = tk.Entry(window); entry_a0.grid(row=3, column=1)

entries_ak, entries_bk = [], []
for k in range(3):
    tk.Label(window, text=f"a{k+1}").grid(row=4, column=k)
    ak_entry = tk.Entry(window); ak_entry.grid(row=5, column=k); entries_ak.append(ak_entry)

    tk.Label(window, text=f"b{k+1}").grid(row=6, column=k)
    bk_entry = tk.Entry(window); bk_entry.grid(row=7, column=k); entries_bk.append(bk_entry)

tk.Label(window, text="ω₀").grid(row=4, column=3)
entry_w0 = tk.Entry(window); entry_w0.grid(row=5, column=3)

tk.Button(window, text="Plot Signals", command=plot_signals).grid(row=8, column=0, columnspan=6)

window.mainloop()