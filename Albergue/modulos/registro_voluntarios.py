import tkinter as tk
from tkinter import ttk, messagebox
from conexion import conectar_bd

def abrir_ventana_voluntarios(padre):
    ventana = tk.Toplevel(padre)
    ventana.title("Registro de Voluntarios")
    ventana.geometry("400x450")

    # --- Campos del formulario ---
    ttk.Label(ventana, text="Nombre").pack(pady=5)
    entrada_nombre = ttk.Entry(ventana, width=40)
    entrada_nombre.pack()

    ttk.Label(ventana, text="Apellidos").pack(pady=5)
    entrada_apellidos = ttk.Entry(ventana, width=40)
    entrada_apellidos.pack()

    ttk.Label(ventana, text="Teléfono").pack(pady=5)
    entrada_telefono = ttk.Entry(ventana, width=40)
    entrada_telefono.pack()

    ttk.Label(ventana, text="Correo electrónico").pack(pady=5)
    entrada_correo = ttk.Entry(ventana, width=40)
    entrada_correo.pack()

    ttk.Label(ventana, text="Rol").pack(pady=5)
    combo_rol = ttk.Combobox(ventana, values=["Médico", "Apoyo General", "Asistente Social", "Cocinero", "Seguridad"])
    combo_rol.pack()

    ttk.Label(ventana, text="Horario asignado").pack(pady=5)
    entrada_horario = ttk.Entry(ventana, width=40)
    entrada_horario.pack()

    def registrar_voluntario():
        nombre = entrada_nombre.get()
        apellidos = entrada_apellidos.get()
        telefono = entrada_telefono.get()
        correo = entrada_correo.get()
        rol = combo_rol.get()
        horario = entrada_horario.get()

        if not nombre or not apellidos or not rol or not horario:
            messagebox.showwarning("Campos requeridos", "Por favor, complete todos los campos obligatorios.")
            return

        conn = conectar_bd()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO Voluntarios 
                    (nombre, apellidos, telefono, correo, rol, horario_trabajo, activo)
                    VALUES (?, ?, ?, ?, ?, ?, 1)
                """, (nombre, apellidos, telefono, correo, rol, horario))
                conn.commit()
                messagebox.showinfo("Éxito", "Voluntario registrado correctamente.")
                ventana.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo registrar:\n{e}")
            finally:
                conn.close()

    ttk.Button(ventana, text="Registrar voluntario", command=registrar_voluntario).pack(pady=20)
