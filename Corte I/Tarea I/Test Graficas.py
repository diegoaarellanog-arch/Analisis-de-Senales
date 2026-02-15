#%%
 
import numpy as np
#import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plot
#plot.ion() # "Interactive ON" - Activa el modo interactivo


class Graficar:         
    @staticmethod
    def s_temp(array, ax): 
        media = np.mean(array)
        std = np.std(array)
        ax.plot(array, color="thistle")
        ax.axhline(media, color="darkmagenta", label=f"media: {media:.2f}", linestyle="dotted")
        ax.set_title("Serie Temporal")
        ax.legend()

    @staticmethod
    def hist(array, ax):
        media = np.mean(array)
        ax.hist(array, bins=10, color="thistle")
        ax.axvline(media, color="darkmagenta", label=f"media: {media:.2f}", linestyle="dotted")
        ax.set_title("Histograma")
        ax.legend()

    @staticmethod
    def cja_big(array, ax):
        ax.boxplot(array, patch_artist=True, 
                   boxprops=dict(facecolor="thistle", color="darkmagenta"))
        ax.set_title("Cajas y Bigotes")

    @staticmethod
    def FFT(array, ax):
        FFT_señal = np.fft.fft(array)
        FFT_señal = np.fft.fftshift(FFT_señal / np.abs(FFT_señal).max())
        frecuencias = np.fft.fftshift(np.fft.fftfreq(len(array), 1))
        ax.plot(frecuencias, np.abs(FFT_señal), color="thistle")
        ax.set_title("FFT")

# =============================================================================
# MAIN con Subplots
# =============================================================================

rng = np.random.default_rng()
array = rng.normal(loc=50, scale=30, size=1000)

# Creamos una cuadrícula de 2 filas y 2 columnas
fig, axes = plot.subplots(2, 2, figsize=(12, 8))

# Pasamos cada "eje" (ax) a las funciones
Graficar.hist(array, axes[0, 0])
Graficar.s_temp(array, axes[0, 1])
Graficar.cja_big(array, axes[1, 0])
Graficar.FFT(array, axes[1, 1])

plot.tight_layout() # Para que no se encimen los títulos

plot.show(block=False)

# print("Graficando... El script no se cerrará hasta que presiones Ctrl+C o cierres la terminal.")

# # Este es el "Ancla": un bucle infinito ligero que mantiene el proceso vivo
# try:
#     while True:
#         plot.pause(0.1) # Mantiene las ventanas vivas y respondiendo (zoom, mover, etc.)
# except KeyboardInterrupt:
#     print("Script finalizado por el usuario.")
# %%
