import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel

# Heredamos de QMainWindow para tener una ventana completa
class MiVentana(QMainWindow):
    def __init__(self):
        super().__init__()

        # 1. Configuración de la ventana
        self.setWindowTitle("Clase Magistral PyQt6")
        self.setMinimumSize(300, 200)

        # 2. El "Central Widget" (PyQt6 necesita un widget base para el layout)
        self.widget_central = QWidget()
        self.setCentralWidget(self.widget_central)

        # 3. Definir el Layout
        self.layout = QVBoxLayout()
        self.widget_central.setLayout(self.layout)

        # 4. Crear Widgets
        self.etiqueta = QLabel("Presiona el botón para cambiar este texto")
        self.boton = QPushButton("¡Haz Click!")

        # 5. Conectar Señal con Slot (Lógica)
        self.boton.clicked.connect(self.al_hacer_click)

        # 6. Añadir widgets al layout
        self.layout.addWidget(self.etiqueta)
        self.layout.addWidget(self.boton)

    # El SLOT (la función que responde al evento)
    def al_hacer_click(self):
        self.etiqueta.setText("¡Señal recibida con éxito! ✅")
        print("El usuario interactuó con la HMI")

# Ejecución estándar de PyQt6
if __name__ == "__main__":
    app = QApplication(sys.argv) # Instancia el cerebro
    ventana = MiVentana()        # Crea tu ventana
    ventana.show()               # La muestra
    sys.exit(app.exec())         # Inicia el bucle de eventos



    