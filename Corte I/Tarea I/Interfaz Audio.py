# ----------------------------------------------------------------------------------------------------
# Librerías necesarias
# ----------------------------------------------------------------------------------------------------

import sys
import numpy as np
import sounddevice as sd
from PyQt6.QtCore import QThread, pyqtSignal as Signal # En PyQt6 se llama pyqtSignal
from PyQt6.QtWidgets import QFrame, QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel
import pyqtgraph as pg

# ----------------------------------------------------------------------------------------------------
# Clase para capturar audio en un hilo separado (para no bloquear la interfaz)
# ----------------------------------------------------------------------------------------------------
class Audio(QThread):
    # Definimos una señal que enviará los datos (un array de numpy) a la interfaz
    datos_listos = Signal(np.ndarray)

    def __init__(self): # Init del hilo de audio
        super().__init__()
        self.corriendo = False # Bandera para controlar el hilo
        self.fs = 48000  # Frecuencia de muestreo (44.1kHz) 48000/44100/22050/16000/8000

    def run(self): # Este método se ejecuta cuando llamamos a hilo_audio.start()
        self.corriendo = True
        # Iniciamos el stream de entrada
        try:
            with sd.InputStream(samplerate=self.fs, channels=1, callback=self.audio_callback):
                while self.corriendo:
                    self.msleep(10) # Menos latencia que 100ms
        except Exception as e:
            print(f"Error de audio: {e}")

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status)
        # Enviamos una copia de los datos capturados a la interfaz
        self.datos_listos.emit(indata.copy())

    def stop(self):
        self.corriendo = False
        self.wait() # Esperamos a que el hilo cierre limpio

# ----------------------------------------------------------------------------------------------------
# Clase de la Ventana Principal
# ----------------------------------------------------------------------------------------------------
# Heredamos de QMainWindow para tener una ventana completa
class MiVentana(QMainWindow):
    # Parametros de configuración (colores, tamaños, etc.)
    Ancho = 900
    Alto = 600

    def __init__(self):
        super().__init__()

        # 1. Configuración de la ventana
        self.setWindowTitle("Transformacion de la Variable Independiente en una Pista de Audio")
        self.setMinimumSize(self.Ancho, self.Alto)
        # self.setMaximumSize(self.Ancho, self.Alto) # Para una ventana fija, descomentar esta línea


        # 2. El "Central Widget" (PyQt6 necesita un widget base para el layout)
        self.widget_central = QWidget()
        self.setCentralWidget(self.widget_central)


        # 3. Definir el Layout
        self.layout_central = QVBoxLayout()
        self.widget_central.setLayout(self.layout_central)


        # 4. Crear Widgets
        self.etiqueta_1 = QLabel("Estado: Esperando...") # Aquí mostraremos el estado de la captura
        self.etiqueta_2 = QLabel("Pendiente Grafica")
    
        self.boton = QPushButton("Iniciar Captura")
        self.boton.setCheckable(True) # Se queda hundido

        self.layout_1 = QHBoxLayout()
        self.marco_1 = QFrame()
        self.marco_1.setLayout(self.layout_1)

        self.layout_1I = QVBoxLayout()
        self.marco_1I = QFrame()
        self.marco_1I.setLayout(self.layout_1I)
        self.marco_1I.setFrameShape(QFrame.Shape.Box)
        self.marco_1I.setFrameShadow(QFrame.Shadow.Plain)
        self.marco_1I.setFixedWidth(200) # Ancho fijo para el panel de controles
        
        self.grafica = pg.PlotWidget()
        self.grafica.setBackground('k')  # Fondo negro como osciloscopio
        self.grafica.showGrid(x = True, y = True)
        self.grafica.setYRange(-0.3, 0.3) # Rango de amplitud (ajusta según tu micro)
        self.curva = self.grafica.plot(pen = 'c') # 'c' es color cian
    

        # 5. Conectar Señal con Slot (Lógica)
        self.boton.clicked.connect(self.toggle_audio)

        # 6. Añadir widgets al layout
        self.layout_central.addWidget(self.marco_1, 1) # (stretch = 1)
        self.layout_1.addWidget(self.marco_1I)
        self.layout_1I.addWidget(self.etiqueta_1, 0) # (stretch = 0)
        self.layout_1I.addWidget(self.boton, 1) # (stretch = 0)
        self.layout_1I.addStretch() # Empuja los botones hacia arriba
        self.layout_1.addWidget(self.grafica, 1)
        
        #self.layout_central.addWidget(self.layout_I)        
        #self.layout.addWidget(self.boton)


        # 7. Instanciar el hilo de audio
        self.hilo_audio = Audio()
        self.hilo_audio.datos_listos.connect(self.actualizar_grafica)


    def toggle_audio(self, checked):
        if checked:
            self.boton.setText("Detener Captura")
            self.etiqueta_1.setText("Estado: Capturando...")
            self.hilo_audio.start()
        else:
            self.boton.setText("Iniciar Captura")
            self.etiqueta_1.setText("Estado: Detenido")
            self.hilo_audio.stop()


    def actualizar_grafica(self, data):
        # Aquí es donde recibes el audio en tiempo real
        volumen = np.linalg.norm(data) * 10 
        print(f"Capturando nivel: {volumen:.2f}")
        self.curva.setData(data.flatten())

# Ejecución estándar de PyQt6
if __name__ == "__main__":
    app = QApplication(sys.argv) # Instancia el cerebro
    ventana = MiVentana()        # Crea tu ventana
    ventana.show()               # La muestra
    sys.exit(app.exec())         # Inicia el bucle de eventos