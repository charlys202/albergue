import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import pyodbc

def conectar_bd():
    try:
        conexion = pyodbc.connect(
            'DRIVER=;'
            'SERVER=localhost;'
            'DATABASE='
            'UID='
            'PWD='
        )
        return conexion
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo conectar a la base de datos:\n{e}")
        return None


def registrar_salida():
    nombre = entrada_nombre.get()
    nacionalidad = entrada_nacionalidad.get()
    telefono = entrada_telefono.get()
    fecha = entrada_fecha.get_date()
    motivo = texto_motivo.get("1.0", "end").strip()

    if not nombre or not nacionalidad:
        messagebox.showwarning("Campos requeridos", "Por favor, complete nombre y nacionalidad.")
        return

    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO Salidas (NombreCompleto, Nacionalidad, TelefonoContacto, FechaSalida, MotivoSalida) VALUES (?, ?, ?, ?, ?)",
                (nombre, nacionalidad, telefono, fecha, motivo)
            )
            conexion.commit()
            messagebox.showinfo("Éxito", "Salida registrada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar la salida:\n{e}")
        finally:
            conexion.close()

ventana = tk.Tk()
ventana.title("Salida de Huésped")
ventana.geometry("430x400")
ventana.config(bg="#e0e0e0")

tk.Label(ventana, text="Salida de Huésped", font=("Arial", 14), fg="purple", bg="#e0e0e0").pack(pady=10)


tk.Label(ventana, text="Nombre completo", bg="#e0e0e0").pack()
entrada_nombre = tk.Entry(ventana, width=40)
entrada_nombre.pack()


tk.Label(ventana, text="Nacionalidad", bg="#e0e0e0").pack()
entrada_nacionalidad = tk.Entry(ventana, width=40)
entrada_nacionalidad.pack()


tk.Label(ventana, text="Teléfono de contacto (opcional)", bg="#e0e0e0").pack()
entrada_telefono = tk.Entry(ventana, width=40)
entrada_telefono.pack()


tk.Label(ventana, text="Fecha de salida", bg="#e0e0e0").pack()
entrada_fecha = DateEntry(ventana, width=37, background='darkblue', foreground='white', borderwidth=2)
entrada_fecha.pack()


tk.Label(ventana, text="En caso de haber alguno, colocar el motivo de salida", bg="#ffffcc", width=45, anchor="w").pack(pady=5)
texto_motivo = tk.Text(ventana, height=4, width=45)
texto_motivo.pack()


boton = tk.Button(ventana, text="Registrar salida", command=registrar_salida, bg="purple", fg="white")
boton.pack(pady=15)

ventana.mainloop()