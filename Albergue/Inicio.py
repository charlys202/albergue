import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import pyodbc


def conectar_bd():
    try:
        conexion = pyodbc.connect(
            'DRIVER='
            'SERVER=localhost;'
            'DATABASE='
            'UID=sa'
            'PWD= '
        )
        return conexion
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo conectar a la base de datos:\n{e}")
        return None


def registrar():
    nombre = entrada_nombre.get()
    nacionalidad = entrada_nacionalidad.get()
    telefono = entrada_telefono.get()
    fecha = entrada_fecha.get_date()

    if not nombre or not nacionalidad:
        messagebox.showwarning("Campos requeridos", "Por favor, complete nombre y nacionalidad.")
        return

    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO H (NombreCompleto, Nacionalidad, TelefonoContacto, FechaIngreso) VALUES (?, ?, ?, ?)",
                (nombre, nacionalidad, telefono, fecha)
            )
            conexion.commit()
            messagebox.showinfo("Éxito", "Huésped registrado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al insertar datos:\n{e}")
        finally:
            conexion.close()


ventana = tk.Tk()
ventana.title("Registro de Huésped")
ventana.geometry("400x300")
ventana.config(bg="#e0e0e0")

tk.Label(ventana, text="Registre sus datos", font=("Arial", 14), fg="purple", bg="#e0e0e0").pack(pady=10)


tk.Label(ventana, text="Nombre completo", bg="#e0e0e0").pack()
entrada_nombre = tk.Entry(ventana, width=30)
entrada_nombre.pack()


tk.Label(ventana, text="Nacionalidad", bg="#e0e0e0").pack()
entrada_nacionalidad = tk.Entry(ventana, width=30)
entrada_nacionalidad.pack()

tk.Label(ventana, text="Teléfono de contacto (opcional)", bg="#e0e0e0").pack()
entrada_telefono = tk.Entry(ventana, width=30)
entrada_telefono.pack()


tk.Label(ventana, text="Fecha de ingreso", bg="#e0e0e0").pack()
entrada_fecha = DateEntry(ventana, width=27, background='darkblue', foreground='white', borderwidth=2)
entrada_fecha.pack()


boton = tk.Button(ventana, text="Registrar huésped", command=registrar, bg="purple", fg="white")
boton.pack(pady=15)

ventana.mainloop()
