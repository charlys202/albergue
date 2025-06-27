import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from conexion import conectar_bd

def abrir_ventana_registro(padre):
    ventana = tk.Toplevel(padre)
    ventana.title("Registro de Huésped")
    ventana.geometry("400x400")

    ttk.Label(ventana, text="Nombre completo").pack()
    entrada_nombre = ttk.Entry(ventana, width=30)
    entrada_nombre.pack()

    ttk.Label(ventana, text="Apellidos").pack()
    entrada_apellidos = ttk.Entry(ventana, width=30)
    entrada_apellidos.pack()

    ttk.Label(ventana, text="Nacionalidad").pack()
    entrada_nacionalidad = ttk.Entry(ventana, width=30)
    entrada_nacionalidad.pack()

    ttk.Label(ventana, text="Género").pack()
    combo_genero = ttk.Combobox(ventana, values=["Masculino", "Femenino", "Otro"])
    combo_genero.pack()

    ttk.Label(ventana, text="Edad").pack()
    entrada_edad = ttk.Entry(ventana, width=10)
    entrada_edad.pack()

    ttk.Label(ventana, text="Fecha de ingreso").pack()
    entrada_fecha = DateEntry(ventana)
    entrada_fecha.pack()

    ttk.Label(ventana, text="Estado de salud").pack()
    entrada_salud = ttk.Entry(ventana, width=30)
    entrada_salud.pack()

    def registrar():
        try:
            edad = int(entrada_edad.get())
        except ValueError:
            messagebox.showerror("Error", "Edad inválida.")
            return

        datos = (
            entrada_nombre.get(),
            entrada_apellidos.get(),
            combo_genero.get(),
            edad,
            entrada_nacionalidad.get(),
            entrada_fecha.get_date(),
            entrada_salud.get(),
            ""
        )
        conn = conectar_bd()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO PersonasAlbergadas 
                    (nombre, apellidos, genero, edad, nacionalidad, fecha_ingreso, estado_salud, observaciones)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, datos)
                conn.commit()
                messagebox.showinfo("Registro exitoso", "Huésped registrado correctamente.")
                ventana.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Fallo al registrar:\n{e}")
            finally:
                conn.close()

    ttk.Button(ventana, text="Registrar", command=registrar).pack(pady=15)
