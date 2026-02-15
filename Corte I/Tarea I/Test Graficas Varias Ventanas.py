#%%
import numpy as np
import matplotlib.pyplot as plot

class Graficar:         
    @staticmethod
    def s_temp(array): 
        plot.figure("Serie Temporal") # Crea ventana 1
        media = np.mean(array)
        plot.plot(array, color="thistle")
        plot.axhline(media, color="darkmagenta", linestyle="dotted", label=f"media: {media:.2f}")
        plot.title("Serie Temporal")
        plot.legend()
        # IMPORTANTE: No ponemos plot.show() aquí

    @staticmethod
    def hist(array):
        plot.figure("Histograma") # Crea ventana 2
        plot.hist(array, bins=10, color="thistle")
        plot.title("Histograma")
        # IMPORTANTE: No ponemos plot.show() aquí

    @staticmethod
    def cja_big(array):
        plot.figure("Cajas y Bigotes") # Crea ventana 3
        plot.boxplot(array, patch_artist=True, 
                     boxprops=dict(facecolor="thistle"))
        plot.title("Cajas y Bigotes")

    @staticmethod
    def FFT(array):
        plot.figure("FFT") # Crea ventana 4
        FFT_señal = np.fft.fft(array)
        FFT_señal = np.fft.fftshift(FFT_señal / np.abs(FFT_señal).max())
        frecuencias = np.fft.fftshift(np.fft.fftfreq(len(array), 1))
        plot.plot(frecuencias, np.abs(FFT_señal), color="thistle")
        plot.title("Transformada de Fourier")

# =============================================================================
# MAIN
# =============================================================================
rng = np.random.default_rng()
array = rng.normal(loc=50, scale=30, size=1000)

# Llamamos a los métodos: esto "prepara" las ventanas en la memoria
Graficar.hist(array)
Graficar.s_temp(array)
Graficar.cja_big(array)
Graficar.FFT(array)

# Esta única línea abre TODAS las ventanas preparadas anteriormente
print("Abriendo todas las ventanas...")
plot.show(block=False)
# %%
