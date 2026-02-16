# ----------------------------------------------------------------------------------------------------
# Librerías necesarias
# ----------------------------------------------------------------------------------------------------

import sys
import numpy as np
import sounddevice as sd
from PyQt6.QtCore import QThread, pyqtSignal as Signal, Qt 
from PyQt6.QtWidgets import (QFrame, QApplication, QMainWindow, QWidget, 
                             QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QSlider)
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
        self.grabacion = [] # Lista para acumular los trozos de audio

    def run(self):
        self.corriendo = True
        self.grabacion = [] # Limpiar grabación anterior al iniciar
        # Volvemos a InputStream porque ya no queremos reproducir mientras grabamos
        with sd.InputStream(samplerate=self.fs, channels=1, callback=self.audio_callback):
            while self.corriendo:
                self.msleep(10)

    def audio_callback(self, indata, frames, time, status):
        if self.corriendo:
            self.grabacion.append(indata.copy()) # Guardamos el bloque
            self.datos_listos.emit(indata.copy())

    def obtener_audio_completo(self):
        # Concatena todos los trozos guardados en un solo array de numpy
        if len(self.grabacion) > 0:
            return np.concatenate(self.grabacion, axis=0)
        return None

    def stop(self):
        self.corriendo = False
        self.wait() # Esperamos a que el hilo cierre limpio

# ----------------------------------------------------------------------------------------------------
# Clase de la Ventana Principal
# ----------------------------------------------------------------------------------------------------
# Heredamos de QMainWindow para tener una ventana completa
class MiVentana(QMainWindow):
    

    def __init__(self):
        super().__init__()
        # Parametros de configuración (colores, tamaños, etc.)
        self.Ancho = 900
        self.Alto = 600
        self.max_muestras = 480000  # Guardaremos 1 segundo de audio para ver
        self.datos_historial = np.zeros(self.max_muestras) # Empezamos con silencio

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

        self.slider_velocidad = QSlider(Qt.Orientation.Horizontal)
        self.slider_velocidad.setMinimum(5)   # Representa 0.5x
        self.slider_velocidad.setMaximum(20)  # Representa 2.0x
        self.slider_velocidad.setValue(10)    # Representa 1.0x
        self.slider_velocidad.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider_velocidad.valueChanged.connect(lambda v: self.etiqueta_velocidad.setText(f"Velocidad: {v/10}x"))

        self.etiqueta_1 = QLabel("Estado: Esperando...") # Aquí mostraremos el estado de la captura
        
        self.etiqueta_2 = QLabel("Pendiente Grafica")

        self.etiqueta_velocidad = QLabel("Velocidad: 1.0x")
    
        self.boton = QPushButton("Iniciar Captura")
        self.boton.setCheckable(True) # Se queda hundido

        self.boton_reproducir = QPushButton("Reproducir Grabación")
        self.boton_reproducir.setEnabled(False) # Desactivado hasta que haya algo grabado
        self.boton_reproducir.clicked.connect(self.reproducir_audio)

        self.boton_reversa = QPushButton("Reproducir f(-t) (Reversa)")
        self.boton_reversa.setEnabled(False) # Desactivado inicialmente
        self.boton_reversa.clicked.connect(self.reproducir_reversa)
        
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
        self.layout_1I.addWidget(self.boton_reproducir)
        self.layout_1I.addWidget(self.boton_reversa)
        self.layout_1I.addWidget(self.etiqueta_velocidad)
        self.layout_1I.addWidget(self.slider_velocidad)
        self.layout_1I.addStretch() # Empuja los botones hacia arriba
        self.layout_1.addWidget(self.grafica, 1)
        
        #self.layout_central.addWidget(self.layout_I)        
        #self.layout.addWidget(self.boton)


        # 7. Instanciar el hilo de audio
        self.hilo_audio = Audio()
        self.hilo_audio.datos_listos.connect(self.actualizar_grafica)


    def toggle_audio(self, checked):
        if checked:
            sd.stop()
            self.boton.setText("Detener Captura")
            self.etiqueta_1.setText("Estado: Capturando...")
            
            # Limpiamos visualmente la gráfica
            self.datos_historial.fill(0)
            self.curva.setData(self.datos_historial)
            
            # Bloqueamos botones de reproducción mientras grabamos
            self.boton_reproducir.setEnabled(False)
            self.boton_reversa.setEnabled(False)
            
            self.hilo_audio.start()
        else:
            self.hilo_audio.stop()
            self.boton.setText("Iniciar Captura")
            self.etiqueta_1.setText("Estado: Detenido")
            
            # Habilitamos ambos botones al terminar la grabación
            self.boton_reproducir.setEnabled(True)
            self.boton_reversa.setEnabled(True)

    def reproducir_audio(self):
        if self.boton_reproducir.text() == "Reproducir Grabación":
            audio_total = self.hilo_audio.obtener_audio_completo()
            
            if audio_total is not None:
                # Obtenemos el factor de escala desde el slider (ej: 1.5)
                factor_a = self.slider_velocidad.value() / 10.0
                
                self.etiqueta_1.setText(f"Estado: Reproduciendo a {factor_a}x...")
                self.boton_reproducir.setText("Parar Reproducción")
                
                # --- ESCALAMIENTO TEMPORAL f(at) ---
                # Al multiplicar fs por factor_a, alteramos la velocidad de lectura
                sd.play(audio_total, int(self.hilo_audio.fs * factor_a))
            else:
                self.etiqueta_1.setText("Estado: Sin datos")
        else:
            sd.stop()
            self.boton_reproducir.setText("Reproducir Grabación")
            
    def reproducir_reversa(self):
        audio_total = self.hilo_audio.obtener_audio_completo()
        
        if audio_total is not None:
            # 1. Obtenemos el factor de velocidad del slider (Escalamiento)
            factor_a = self.slider_velocidad.value() / 10.0
            self.etiqueta_1.setText(f"Estado: Reversa a {factor_a}x...")
            
            # 2. Aplicamos la reflexión: f(-t)
            audio_reversa = np.flip(audio_total)
            
            # 3. Reproducimos con el escalamiento aplicado a la frecuencia
            # Esto resulta en la transformación combinada f(-at)
            sd.play(audio_reversa, int(self.hilo_audio.fs * factor_a))
        else:
            self.etiqueta_1.setText("Estado: No hay datos")

    def actualizar_grafica(self, data):
        # 1. Aplanar los datos que llegan (de nx1 a n)
        nuevo_bloque = data.flatten()
        tamano_nuevo = len(nuevo_bloque)

        # 2. Desplazar los datos viejos a la izquierda
        # Los datos del índice [tamano_nuevo:] pasan a ser los primeros
        self.datos_historial[:-tamano_nuevo] = self.datos_historial[tamano_nuevo:]

        # 3. Insertar el nuevo bloque al final (derecha)
        self.datos_historial[-tamano_nuevo:] = nuevo_bloque

        # 4. Actualizar la curva con todo el historial
        self.curva.setData(self.datos_historial)


# Ejecución estándar de PyQt6
if __name__ == "__main__":
    app = QApplication(sys.argv) # Instancia el cerebro
    ventana = MiVentana()        # Crea tu ventana
    ventana.show()               # La muestra
    sys.exit(app.exec())         # Inicia el bucle de eventos