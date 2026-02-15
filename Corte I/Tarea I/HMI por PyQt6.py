import sys
import numpy as np
import serial
import serial.tools.list_ports
from PyQt6 import QtWidgets, QtCore
import pyqtgraph as pg

class MiHMI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # 1. Configuración de la Ventana
        self.setWindowTitle("Panel de Control HMI - Análisis de Señales")
        self.resize(1000, 600)
        self.setStyleSheet("background-color: #2b2b2b; color: #e0e0e0;")

        # 2. Layout Principal
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QtWidgets.QHBoxLayout(self.central_widget)

        # 3. Panel Lateral de Controles
        self.panel_control = QtWidgets.QVBoxLayout()
        self.btn_conectar = QtWidgets.QPushButton("Conectar Serial")
        self.btn_conectar.setStyleSheet("background-color: #4a4a4a; padding: 10px;")
        self.btn_conectar.clicked.connect(self.conectar_serial)
        
        self.label_status = QtWidgets.QLabel("Estado: Desconectado")
        
        self.panel_control.addWidget(self.btn_conectar)
        self.panel_control.addWidget(self.label_status)
        self.panel_control.addStretch() # Empuja todo hacia arriba

        # 4. Panel de Gráficas (Usando PyQtGraph)
        self.graph_widget = pg.PlotWidget()
        self.graph_widget.setBackground('#1e1e1e')
        self.graph_widget.showGrid(x=True, y=True)
        self.curve = self.graph_widget.plot(pen=pg.mkPen(color='m', width=2))
        
        self.data_buffer = np.zeros(200) # Buffer de datos

        # Unir paneles
        self.layout.addLayout(self.panel_control, 1)
        self.layout.addWidget(self.graph_widget, 4)

        # 5. Timer para actualizar la interfaz
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.actualizar_grafica)
        self.timer.start(50) # Actualiza cada 50ms (20 FPS)

    def conectar_serial(self):
        # Aquí iría tu lógica de pyserial
        self.label_status.setText("Estado: Conectado")
        self.label_status.setStyleSheet("color: #00ff00;")

    def actualizar_grafica(self):
        # Simulando datos (aquí pondrías los datos de tu sensor)
        self.data_buffer = np.roll(self.data_buffer, -1)
        self.data_buffer[-1] = np.random.normal(50, 5)
        self.curve.setData(self.data_buffer)

# Ejecución de la App
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MiHMI()
    window.show()
    sys.exit(app.exec())