
import tkinter as tk
from tkinter import ttk, messagebox
from modulos.registro import abrir_ventana_registro
from modulos.consultas import abrir_ventana_consulta
from modulos.registro_voluntarios import abrir_ventana_voluntarios



def main():
    ventana = tk.Tk()
    ventana.title("Sistema Albergue Fronterizo")
    ventana.geometry("400x300")
    ventana.config(bg="#f0f0f0")

    ttk.Label(ventana, text="Menú Principal", font=("Arial", 16)).pack(pady=20)

    ttk.Button(ventana, text="Registro de Huéspedes", command=lambda: abrir_ventana_registro(ventana)).pack(pady=10)
    ttk.Button(ventana, text="Consultar Huéspedes", command=lambda: abrir_ventana_consulta(ventana)).pack(pady=10)
    ttk.Button(ventana, text="Registrar Voluntarios", command=lambda: abrir_ventana_voluntarios(ventana)).pack(pady=10)


    ttk.Button(ventana, text="Salir", command=ventana.quit).pack(pady=10)

    ventana.mainloop()

if __name__ == "__main__":
    main()
