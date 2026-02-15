import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import serial.tools.list_ports

class HMI_Tkinter:
    def __init__(self, root):
        self.root = root
        self.root.title("HMI Analizador de Señales (Tkinter)")
        self.root.geometry("800x600")

        # --- 1. Panel de Controles (Izquierda) ---
        self.frame_controles = tk.Frame(self.root, width=200, bg="#f0f0f0", padx=10, pady=10)
        self.frame_controles.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(self.frame_controles, text="Configuración", font=("Arial", 12, "bold")).pack(pady=10)

        # Selector de Puertos
        tk.Label(self.frame_controles, text="Puerto COM:").pack()
        self.combo_puertos = ttk.Combobox(self.frame_controles)
        self.actualizar_puertos()
        self.combo_puertos.pack(pady=5)

        # Botón Conectar
        self.btn_conectar = tk.Button(self.frame_controles, text="Conectar", command=self.conectar, bg="#4caf50", fg="white")
        self.btn_conectar.pack(pady=10, fill=tk.X)

        # --- 2. Panel de Gráfica (Derecha) ---
        self.frame_grafica = tk.Frame(self.root, bg="white")
        self.frame_grafica.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Configurar Matplotlib dentro de Tkinter
        self.fig, self.ax = plt.subplots(figsize=(5, 4), dpi=100)
        self.x_data = np.arange(0, 100)
        self.y_data = np.zeros(100)
        self.line, = self.ax.plot(self.x_data, self.y_data, color='purple')
        self.ax.set_ylim(-10, 110) # Ajustar según tu sensor

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_grafica)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # --- 3. Inicio del ciclo de actualización ---
        self.update_loop()

    def actualizar_puertos(self):
        puertos = serial.tools.list_ports.comports()
        self.combo_puertos['values'] = [p.device for p in puertos]

    def conectar(self):
        puerto = self.combo_puertos.get()
        print(f"Conectando a {puerto}...")

    def update_loop(self):
        # Simulamos la lectura de un dato
        nuevo_dato = np.random.normal(50, 10)
        
        # Desplazamos los datos (Efecto osciloscopio)
        self.y_data = np.roll(self.y_data, -1)
        self.y_data[-1] = nuevo_dato
        
        # Actualizamos la línea de la gráfica
        self.line.set_ydata(self.y_data)
        
        # Redibujamos solo lo necesario para ganar velocidad
        self.canvas.draw_idle()

        # Aquí ocurre la magia: .after(milisegundos, función)
        # Llama a esta misma función cada 50ms sin bloquear la ventana
        self.root.after(50, self.update_loop)

# Lanzar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = HMI_Tkinter(root)
    root.mainloop()