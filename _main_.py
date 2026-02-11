import tkinter as tk
from tkinter import filedialog, messagebox
import librosa
import numpy as np
import sounddevice as sd
import soundfile as sf

class AudioTransformerApp:
    def _init_(self, root):
        self.root = root
        self.root.title("Transformador de Variable Independiente (Tiempo)")
        self.root.geometry("400x350")

        self.file_path = None
        self.audio_data = None
        self.sr = None
        self.modified_audio = None

        # --- Interfaz Gráfica ---
        tk.Label(root, text="Procesamiento de Audio: f(t) -> f(αt + β)", font=("Arial", 12, "bold")).pack(pady=10)

        tk.Button(root, text="Cargar Archivo de Audio", command=self.load_audio).pack(pady=5)
        
        self.lbl_file = tk.Label(root, text="No hay archivo cargado", fg="gray")
        self.lbl_file.pack()

        # Control de Velocidad (Escalamiento temporal: αt)
        tk.Label(root, text="Factor de Velocidad (α):").pack(pady=5)
        self.speed_scale = tk.Scale(root, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL)
        self.speed_scale.set(1.0)
        self.speed_scale.pack()

        # Inversión Temporal (Reverso)
        self.reverse_var = tk.BooleanVar()
        tk.Checkbutton(root, text="Invertir Tiempo (f(-t))", variable=self.reverse_var).pack(pady=5)

        # Botones de Acción
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Procesar y Reproducir", command=self.process_audio, bg="lightblue").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Guardar Resultado", command=self.save_audio, bg="lightgreen").pack(side=tk.LEFT, padx=5)

    def load_audio(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3 *.flac")])
        if self.file_path:
            self.audio_data, self.sr = librosa.load(self.file_path, sr=None)
            self.lbl_file.config(text=f"Cargado: {self.file_path.split('/')[-1]}", fg="black")

    def process_audio(self):
        if self.audio_data is None:
            messagebox.showwarning("Error", "Primero carga un archivo de audio.")
            return

        # 1. Aplicar Escalamiento (Velocidad)
        # Nota: librosa.effects.time_stretch cambia la velocidad sin afectar el tono (pitch)
        factor = self.speed_scale.get()
        temp_audio = librosa.effects.time_stretch(y=self.audio_data, rate=factor)

        # 2. Aplicar Reflexión (Reverso)
        if self.reverse_var.get():
            temp_audio = np.flip(temp_audio)

        self.modified_audio = temp_audio
        
        # Reproducir
        sd.stop()
        sd.play(self.modified_audio, self.sr)

    def save_audio(self):
        if self.modified_audio is None:
            messagebox.showwarning("Error", "No hay audio procesado para guardar.")
            return
        
        save_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])
        if save_path:
            sf.write(save_path, self.modified_audio, self.sr)
            messagebox.showinfo("Éxito", "Archivo guardado correctamente.")

if _name_ == "_main_":
    root = tk.Tk()
    app = AudioTransformerApp(root)
    root.mainloop()