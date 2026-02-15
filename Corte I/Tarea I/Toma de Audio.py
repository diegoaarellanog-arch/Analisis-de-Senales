import sys
import numpy as np
import sounddevice as sd
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PySide6.QtCore import QThread, Signal

# --- CLASE QUE CAPTURA EL AUDIO (HILO) ---
class Audio(QThread):
    # Definimos una señal que enviará los datos (un array de numpy) a la interfaz
    datos_listos = Signal(np.ndarray)

    def __init__(self):
        super().__init__()
        self.corriendo = False
        self.fs = 44100  # Frecuencia de muestreo (44.1kHz)

    def run(self):
        self.corriendo = True
        # Iniciamos el stream de entrada
        with sd.InputStream(samplerate=self.fs, channels=1, callback=self.audio_callback):
            while self.corriendo:
                self.msleep(100) # Mantener el hilo vivo

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status)
        # Enviamos una copia de los datos capturados a la interfaz
        self.datos_listos.emit(indata.copy())

    def stop(self):
        self.corriendo = False

# --- VENTANA PRINCIPAL ---
class InterfazAudio(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Capturador de Audio HMI")

        # UI Básica
        self.widget_central = QWidget()
        self.setCentralWidget(self.widget_central)
        self.layout = QVBoxLayout(self.widget_central)

        self.label_estado = QLabel("Estado: Esperando...")
        self.btn_capturar = QPushButton("Iniciar Captura")
        self.btn_capturar.setCheckable(True) # Se queda hundido
        self.btn_capturar.clicked.connect(self.toggle_audio)

        self.layout.addWidget(self.label_estado)
        self.layout.addWidget(self.btn_capturar)

        # Instanciar el hilo de audio
        self.hilo_audio = Audio()
        self.hilo_audio.datos_listos.connect(self.actualizar_grafica)

    def toggle_audio(self, checked):
        if checked:
            self.btn_capturar.setText("Detener Captura")
            self.label_estado.setText("Estado: Capturando...")
            self.hilo_audio.start()
        else:
            self.btn_capturar.setText("Iniciar Captura")
            self.label_estado.setText("Estado: Detenido")
            self.hilo_audio.stop()

    def actualizar_grafica(self, data):
        # Aquí es donde recibes el audio en tiempo real
        volumen = np.linalg.norm(data) * 10 
        print(f"Capturando nivel: {volumen:.2f}")
        # Aquí podrías actualizar una barra de progreso o tu gráfica

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = InterfazAudio()
    ventana.show()
    sys.exit(app.exec())