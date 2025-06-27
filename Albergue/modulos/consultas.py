import tkinter as tk
from tkinter import ttk, messagebox
from conexion import conectar_bd

def abrir_ventana_consulta(padre):
    ventana = tk.Toplevel(padre)
    ventana.title("Consulta de Huéspedes")
    ventana.geometry("1000x600")
    ventana.configure(bg="#f8f9fa")

    # --- HEADER AZUL ---
    header_frame = tk.Frame(ventana, bg="#3498db", height=70)
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)
    
    tk.Label(header_frame, text="🔍 CONSULTA DE HUÉSPEDES", 
             font=("Arial", 16, "bold"), fg="white", bg="#3498db").pack(side="left", padx=20, pady=20)
    
    # Contador de registros
    contador_label = tk.Label(header_frame, text="Total: 0 registros", 
                             font=("Arial", 12), fg="#d6eaf8", bg="#3498db")
    contador_label.pack(side="right", padx=20, pady=25)

    # --- CONTENEDOR PRINCIPAL ---
    main_container = tk.Frame(ventana, bg="#f8f9fa")
    main_container.pack(fill="both", expand=True, padx=20, pady=20)

    # --- BARRA DE BÚSQUEDA ---
    busqueda_frame = tk.Frame(main_container, bg="#ffffff", relief="raised", bd=2)
    busqueda_frame.pack(fill="x", pady=(0, 20))

    search_container = tk.Frame(busqueda_frame, bg="#ffffff")
    search_container.pack(fill="x", padx=20, pady=15)

    tk.Label(search_container, text="🔍", font=("Arial", 16), 
             bg="#ffffff", fg="#3498db").pack(side="left", padx=(0, 10))
    
    tk.Label(search_container, text="Buscar por nombre o nacionalidad:", 
             font=("Arial", 11, "bold"), bg="#ffffff", fg="#2c3e50").pack(side="left")
    
    entrada_busqueda = tk.Entry(search_container, font=("Arial", 11), relief="solid", 
                               bd=2, bg="#ffffff", fg="#2c3e50", width=40)
    entrada_busqueda.pack(side="left", padx=10)

    def crear_boton_busqueda(texto, comando, color):
        btn = tk.Button(search_container, text=texto, command=comando,
                       bg=color, fg="white", font=("Arial", 10, "bold"),
                       relief="flat", cursor="hand2", width=12)
        btn.pack(side="left", padx=5)
        
        def on_enter(e): btn.configure(relief="raised")
        def on_leave(e): btn.configure(relief="flat")
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    crear_boton_busqueda("🔍 Buscar", buscar, "#3498db")
    crear_boton_busqueda("📋 Mostrar Todo", lambda: cargar_datos(), "#17a2b8")

    # --- TABLA PRINCIPAL ---
    tabla_frame = tk.Frame(main_container, bg="#ffffff", relief="raised", bd=2)
    tabla_frame.pack(fill="both", expand=True, pady=(0, 20))

    # Configuración de la tabla
    columnas = ("ID", "Nombre", "Apellidos", "Nacionalidad", "FechaIngreso", "Estado")
    tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=15)

    # Headers de la tabla
    headers_config = {
        "ID": {"text": "ID", "width": 80},
        "Nombre": {"text": "Nombre", "width": 150},
        "Apellidos": {"text": "Apellidos", "width": 150},
        "Nacionalidad": {"text": "Nacionalidad", "width": 130},
        "FechaIngreso": {"text": "Fecha Ingreso", "width": 120},
        "Estado": {"text": "Estado", "width": 100}
    }

    for col, config in headers_config.items():
        tabla.heading(col, text=config["text"])
        tabla.column(col, width=config["width"], anchor="center")

    # Scrollbars
    scrollbar_v = ttk.Scrollbar(tabla_frame, orient="vertical", command=tabla.yview)
    scrollbar_h = ttk.Scrollbar(tabla_frame, orient="horizontal", command=tabla.xview)
    tabla.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)

    tabla.pack(side="left", fill="both", expand=True, padx=15, pady=15)
    scrollbar_v.pack(side="right", fill="y")
    scrollbar_h.pack(side="bottom", fill="x")

    # --- Acciones de la BD --- #
    def buscar():
        valor = entrada_busqueda.get()
        cargar_datos(filtro=valor)
    
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


    # --- PANEL DE ACCIONES ---
    acciones_frame = tk.Frame(main_container, bg="#ffffff", relief="raised", bd=2)
    acciones_frame.pack(fill="x")

    botones_container = tk.Frame(acciones_frame, bg="#ffffff")
    botones_container.pack(fill="x", padx=20, pady=15)

    def crear_boton_accion(texto, comando, color, side="left"):
        btn = tk.Button(botones_container, text=texto, command=comando,
                       bg=color, fg="white", font=("Arial", 11, "bold"),
                       relief="flat", cursor="hand2", width=15, height=2)
        btn.pack(side=side, padx=10)
        
        def on_enter(e): btn.configure(relief="raised")
        def on_leave(e): btn.configure(relief="flat")
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn
    

    crear_boton_accion("👁️ Ver Detalles", ver_detalles, "#f39c12", "left")
    #crear_boton_accion("📝 Editar", editar, "#17a2b8", "left")#
    crear_boton_accion("🗑️ Eliminar", eliminar, "#e74c3c", "left")
    crear_boton_accion("❌ Cerrar", ventana.destroy, "#95a5a6", "right")


