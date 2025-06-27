import tkinter as tk
from tkinter import ttk, messagebox
from conexion import conectar_bd

def abrir_ventana_consulta(padre):
    ventana = tk.Toplevel(padre)
    ventana.title("Consulta de Huéspedes")
    ventana.geometry("800x400")

    # --- Filtros ---
    marco_filtros = tk.Frame(ventana)
    marco_filtros.pack(pady=10)

    tk.Label(marco_filtros, text="Buscar por nombre o nacionalidad:").pack(side="left", padx=5)
    entrada_busqueda = tk.Entry(marco_filtros, width=40)
    entrada_busqueda.pack(side="left", padx=5)

    def buscar():
        valor = entrada_busqueda.get()
        cargar_datos(filtro=valor)

    tk.Button(marco_filtros, text="Buscar", command=buscar).pack(side="left", padx=5)
    tk.Button(marco_filtros, text="Mostrar todo", command=lambda: cargar_datos()).pack(side="left")

    # --- Tabla ---
    columnas = ("ID", "Nombre", "Apellidos", "Nacionalidad", "FechaIngreso")
    tabla = ttk.Treeview(ventana, columns=columnas, show="headings", height=10)

    tabla.heading("ID", text="ID")
    tabla.heading("Nombre", text="Nombre")
    tabla.heading("Apellidos", text="Apellidos")
    tabla.heading("Nacionalidad", text="Nacionalidad")
    tabla.heading("FechaIngreso", text="Fecha de ingreso")

    for col in columnas:
        tabla.column(col, width=140, anchor="center")

    tabla.pack(fill="both", expand=True, padx=10)

    # --- Botones de acción ---
    def ver_detalles():
        item = tabla.focus()
        if not item:
            messagebox.showwarning("Atención", "Seleccione un registro.")
            return
        datos = tabla.item(item, "values")
        messagebox.showinfo("Detalles del Huésped", f"""
ID: {datos[0]}
Nombre: {datos[1]} {datos[2]}
Nacionalidad: {datos[3]}
Fecha de ingreso: {datos[4]}
""")

    def eliminar():
        item = tabla.focus()
        if not item:
            messagebox.showwarning("Atención", "Seleccione un registro.")
            return
        datos = tabla.item(item, "values")
        confirmacion = messagebox.askyesno("Confirmar", f"¿Desea eliminar el registro de {datos[1]}?")
        if confirmacion:
            conn = conectar_bd()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM PersonasAlbergadas WHERE id_persona = ?", (datos[0],))
                    conn.commit()
                    messagebox.showinfo("Eliminado", "Registro eliminado correctamente.")
                    cargar_datos()
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo eliminar:\n{e}")
                finally:
                    conn.close()

    marco_botones = tk.Frame(ventana)
    marco_botones.pack(pady=10)

    tk.Button(marco_botones, text="Ver detalles", command=ver_detalles).pack(side="left", padx=10)
    tk.Button(marco_botones, text="Eliminar", command=eliminar).pack(side="left", padx=10)
    tk.Button(marco_botones, text="Cerrar", command=ventana.destroy).pack(side="right", padx=10)

    # --- Cargar datos ---
    def cargar_datos(filtro=None):
        for row in tabla.get_children():
            tabla.delete(row)
        conn = conectar_bd()
        if conn:
            try:
                cursor = conn.cursor()
                if filtro:
                    consulta = """
                    SELECT id_persona, nombre, apellidos, nacionalidad, fecha_ingreso
                    FROM PersonasAlbergadas
                    WHERE nombre LIKE ? OR nacionalidad LIKE ?
                    """
                    cursor.execute(consulta, (f"%{filtro}%", f"%{filtro}%"))
                else:
                    cursor.execute("""
                    SELECT id_persona, nombre, apellidos, nacionalidad, fecha_ingreso
                    FROM PersonasAlbergadas
                    """)
                for fila in cursor.fetchall():
                    id_persona, nombre, apellidos, nacionalidad, fecha_ingreso = fila
                    tabla.insert("", "end", values=(id_persona, nombre, apellidos, nacionalidad, fecha_ingreso))
            except Exception as e:
                messagebox.showerror("Error", f"Error al consultar la base de datos:\n{e}")
            finally:
                conn.close()

    cargar_datos()
