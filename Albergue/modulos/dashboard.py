import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from conexion import conectar_bd


def abrir_ventana_dashboard(padre):
    ventana = tk.Toplevel(padre)
    ventana.title("Dashboard - Albergue Fronterizo")
    ventana.geometry("1400x800")  # Aumenté el tamaño para acomodar más contenido
    ventana.configure(bg="#f5f5f5")

    # --- Header ---
    header_frame = tk.Frame(ventana, bg="#2c3e50", height=80)
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)

    # Título principal
    titulo_label = tk.Label(header_frame, text="ALBERGUE FRONTERIZO", 
                           font=("Arial", 20, "bold"), fg="white", bg="#2c3e50")
    titulo_label.pack(side="left", padx=20, pady=25)

    # Fecha actual
    fecha_actual = datetime.datetime.now().strftime("%d de %B, %Y")
    fecha_label = tk.Label(header_frame, text=fecha_actual, 
                          font=("Arial", 12), fg="#ecf0f1", bg="#2c3e50")
    fecha_label.pack(side="right", padx=20, pady=30)

    # --- Contenedor principal ---
    main_container = tk.Frame(ventana, bg="#f5f5f5")
    main_container.pack(fill="both", expand=True, padx=20, pady=20)

    # --- Panel izquierdo (estadísticas y huéspedes) ---
    left_panel = tk.Frame(main_container, bg="#f5f5f5")
    left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))

    # --- Panel de estadísticas ---
    stats_frame = tk.Frame(left_panel, bg="#ffffff", relief="raised", bd=1)
    stats_frame.pack(fill="x", pady=(0, 10))

    # Título de estadísticas
    tk.Label(stats_frame, text="Estadísticas Generales", 
             font=("Arial", 16, "bold"), bg="white", fg="#2c3e50").pack(pady=15)

    # Container para tarjetas de estadísticas
    cards_container = tk.Frame(stats_frame, bg="white")
    cards_container.pack(fill="x", padx=20, pady=(0, 20))

    # Función para crear tarjetas de estadísticas
    def crear_tarjeta_stat(parent, titulo, valor, color):
        card = tk.Frame(parent, bg=color, relief="raised", bd=2, height=80)
        card.pack(side="left", fill="x", expand=True, padx=5)
        card.pack_propagate(False)
        
        tk.Label(card, text=titulo, font=("Arial", 10, "bold"), 
                bg=color, fg="white").pack(pady=(10, 5))
        tk.Label(card, text=str(valor), font=("Arial", 18, "bold"), 
                bg=color, fg="white").pack()

    # Obtener estadísticas de la base de datos
    def obtener_estadisticas():
        conn = conectar_bd()
        stats = {"total_huespedes": 0, "huespedes_hoy": 0, "voluntarios_activos": 0, "total_suministros": 0}
        
        if conn:
            try:
                cursor = conn.cursor()
                
                # Total de huéspedes
                cursor.execute("SELECT COUNT(*) FROM PersonasAlbergadas")
                stats["total_huespedes"] = cursor.fetchone()[0]
                
                # Huéspedes ingresados hoy
                hoy = datetime.date.today()
                cursor.execute("SELECT COUNT(*) FROM PersonasAlbergadas WHERE fecha_ingreso = ?", (hoy,))
                stats["huespedes_hoy"] = cursor.fetchone()[0]
                
                # Voluntarios activos
                cursor.execute("SELECT COUNT(*) FROM Voluntarios WHERE activo = 1")
                stats["voluntarios_activos"] = cursor.fetchone()[0]
                
                # Total de tipos de suministros
                cursor.execute("SELECT COUNT(*) FROM Suministros")
                stats["total_suministros"] = cursor.fetchone()[0]
                
            except Exception as e:
                print(f"Error al obtener estadísticas: {e}")
            finally:
                conn.close()
        
        return stats

    # Crear tarjetas con estadísticas
    stats = obtener_estadisticas()
    crear_tarjeta_stat(cards_container, "Total Huéspedes", stats["total_huespedes"], "#3498db")
    crear_tarjeta_stat(cards_container, "Ingresos Hoy", stats["huespedes_hoy"], "#27ae60")
    crear_tarjeta_stat(cards_container, "Voluntarios Activos", stats["voluntarios_activos"], "#e67e22")
    crear_tarjeta_stat(cards_container, "Suministros", stats["total_suministros"], "#9b59b6")

    # --- Lista de huéspedes recientes ---
    recientes_frame = tk.Frame(left_panel, bg="white", relief="raised", bd=1)
    recientes_frame.pack(fill="both", expand=True)

    tk.Label(recientes_frame, text="Huéspedes Recientes", 
             font=("Arial", 14, "bold"), bg="white", fg="#2c3e50").pack(anchor="w", padx=20, pady=(15, 10))

    # Tabla de huéspedes recientes
    columnas_recientes = ("Nombre", "Nacionalidad", "Fecha")
    tabla_recientes = ttk.Treeview(recientes_frame, columns=columnas_recientes, show="headings", height=8)
    
    for col in columnas_recientes:
        tabla_recientes.heading(col, text=col)
        tabla_recientes.column(col, width=120)

    tabla_recientes.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    # Cargar huéspedes recientes
    def cargar_recientes():
        conn = conectar_bd()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT TOP 10 nombre + ' ' + ISNULL(apellidos, ''), 
                           ISNULL(nacionalidad, 'No especificada'), 
                           fecha_ingreso
                    FROM PersonasAlbergadas
                    ORDER BY fecha_ingreso DESC
                """)
                for fila in cursor.fetchall():
                    tabla_recientes.insert("", "end", values=fila)
            except Exception as e:
                print(f"Error al cargar recientes: {e}")
            finally:
                conn.close()

    cargar_recientes()

    # --- Panel derecho ---
    right_panel = tk.Frame(main_container, bg="#f5f5f5")
    right_panel.pack(side="right", fill="both", expand=True, padx=(10, 0))

    # --- Panel de suministros (parte superior derecha) ---
    suministros_frame = tk.Frame(right_panel, bg="#ffffff", relief="raised", bd=1)
    suministros_frame.pack(fill="both", expand=True, pady=(0, 10))

    tk.Label(suministros_frame, text="Estado de Suministros", 
             font=("Arial", 14, "bold"), bg="white", fg="#2c3e50").pack(anchor="w", padx=20, pady=(15, 10))

    # Tabla de suministros
    columnas_suministros = ("Tipo", "Descripción", "Cantidad", "Unidad", "Estado")
    tabla_suministros = ttk.Treeview(suministros_frame, columns=columnas_suministros, show="headings", height=10)
    
    # Configurar columnas
    anchos_columnas = {"Tipo": 100, "Descripción": 150, "Cantidad": 80, "Unidad": 80, "Estado": 100}
    for col in columnas_suministros:
        tabla_suministros.heading(col, text=col)
        tabla_suministros.column(col, width=anchos_columnas[col])

    # Scrollbar para la tabla de suministros
    scrollbar_suministros = ttk.Scrollbar(suministros_frame, orient="vertical", command=tabla_suministros.yview)
    tabla_suministros.configure(yscrollcommand=scrollbar_suministros.set)

    # Pack de la tabla y scrollbar
    tabla_frame = tk.Frame(suministros_frame, bg="white")
    tabla_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    tabla_suministros.pack(side="left", fill="both", expand=True)
    scrollbar_suministros.pack(side="right", fill="y")

    # Cargar datos de suministros
    def cargar_suministros():
        # Limpiar tabla existente
        for item in tabla_suministros.get_children():
            tabla_suministros.delete(item)
            
        conn = conectar_bd()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT tipo_suministro, 
                           ISNULL(descripcion, 'Sin descripción'), 
                           cantidad, 
                           ISNULL(unidad_medida, 'unidad'), 
                           ISNULL(estado, 'Disponible')
                    FROM Suministros
                    ORDER BY tipo_suministro
                """)
                
                for fila in cursor.fetchall():
                    # Determinar color de la fila según el estado y cantidad
                    tipo, desc, cantidad, unidad, estado = fila
                    
                    # Insertar en la tabla
                    item_id = tabla_suministros.insert("", "end", values=fila)
                    
                    # Colorear según el estado
                    if estado.lower() == 'agotado' or cantidad == 0:
                        tabla_suministros.set(item_id, "Estado", "⚠️ Agotado")
                    elif cantidad < 50:  # Umbral bajo
                        tabla_suministros.set(item_id, "Estado", "⚡ Bajo")
                    else:
                        tabla_suministros.set(item_id, "Estado", "✅ Disponible")
                        
            except Exception as e:
                print(f"Error al cargar suministros: {e}")
                # Insertar datos de ejemplo en caso de error
                datos_ejemplo = [
                    ("Alimentos", "Arroz, frijoles, aceite", 450, "kg", "✅ Disponible"),
                    ("Medicinas", "Medicamentos básicos", 250, "piezas", "✅ Disponible"),
                    ("Ropa", "Ropa de abrigo y básica", 200, "piezas", "✅ Disponible"),
                    ("Higiene", "Artículos de limpieza", 100, "piezas", "⚡ Bajo"),
                    ("Agua", "Agua potable", 1000, "litros", "✅ Disponible")
                ]
                for fila in datos_ejemplo:
                    tabla_suministros.insert("", "end", values=fila)
            finally:
                conn.close()

    cargar_suministros()

    # --- Panel de acciones rápidas (parte inferior derecha) ---
    actions_frame = tk.Frame(right_panel, bg="#ffffff", relief="raised", bd=1)
    actions_frame.pack(fill="x")

    tk.Label(actions_frame, text="Acciones Rápidas", 
             font=("Arial", 14, "bold"), bg="white", fg="#2c3e50").pack(pady=15)

    # Función para crear botones de acción
    def crear_boton_accion(parent, texto, comando, color):
        btn = tk.Button(parent, text=texto, command=comando, 
                       bg=color, fg="white", font=("Arial", 10, "bold"),
                       relief="flat", cursor="hand2", width=18, height=1)
        btn.pack(pady=5, padx=20)
        
        # Efectos hover
        def on_enter(e):
            btn.configure(relief="raised")
        def on_leave(e):
            btn.configure(relief="flat")
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    # Crear frame para botones en dos columnas
    botones_frame = tk.Frame(actions_frame, bg="white")
    botones_frame.pack(fill="x", padx=20, pady=10)

    # Columna izquierda de botones
    col_izq = tk.Frame(botones_frame, bg="white")
    col_izq.pack(side="left", fill="x", expand=True, padx=(0, 5))

    # Columna derecha de botones
    col_der = tk.Frame(botones_frame, bg="white")
    col_der.pack(side="right", fill="x", expand=True, padx=(5, 0))

    # Botones de acción
    crear_boton_accion(col_izq, "Nuevo Huésped", 
                      lambda: importar_y_ejecutar("modulos.registro", "abrir_ventana_registro", ventana), "#3498db")
    
    crear_boton_accion(col_der, "Consultar Huéspedes", 
                      lambda: importar_y_ejecutar("modulos.consultas", "abrir_ventana_consulta", ventana), "#27ae60")
    
    crear_boton_accion(col_izq, "Registrar Voluntario", 
                      lambda: importar_y_ejecutar("modulos.registro_voluntarios", "abrir_ventana_voluntarios", ventana), "#e67e22")
    
    crear_boton_accion(col_der, "Ver Gráficas", 
                      lambda: importar_y_ejecutar("modulos.graficas", "abrir_ventana_graficas", ventana), "#9b59b6")

    # --- Sección de alertas ---
    alertas_frame = tk.Frame(actions_frame, bg="#ecf0f1", relief="sunken", bd=1)
    alertas_frame.pack(fill="x", padx=20, pady=10)

    tk.Label(alertas_frame, text="Alertas del Sistema", 
             font=("Arial", 12, "bold"), bg="#ecf0f1", fg="#2c3e50").pack(pady=10)

    # Verificar alertas
    def verificar_alertas():
        conn = conectar_bd()
        alertas_container = tk.Frame(alertas_frame, bg="#ecf0f1")
        alertas_container.pack(fill="x", padx=10, pady=5)
        
        if conn:
            try:
                cursor = conn.cursor()
                
                # Alerta de capacidad de huéspedes
                cursor.execute("SELECT COUNT(*) FROM PersonasAlbergadas WHERE fecha_egreso IS NULL")
                total_activos = cursor.fetchone()[0]
                
                if total_activos > 80:
                    alerta_text = f"⚠️ Alerta: {total_activos} huéspedes activos"
                    color_alerta = "#e74c3c"
                elif total_activos > 60:
                    alerta_text = f"⚡ Atención: {total_activos} huéspedes activos"
                    color_alerta = "#f39c12"
                else:
                    alerta_text = f"✅ Capacidad normal: {total_activos} huéspedes"
                    color_alerta = "#27ae60"
                
                tk.Label(alertas_container, text=alerta_text, 
                        font=("Arial", 9), bg="#ecf0f1", fg=color_alerta).pack(anchor="w")
                
                # Alerta de suministros bajos
                cursor.execute("SELECT COUNT(*) FROM Suministros WHERE cantidad < 50")
                suministros_bajos = cursor.fetchone()[0]
                
                if suministros_bajos > 0:
                    alerta_suministros = f"⚠️ {suministros_bajos} suministros con stock bajo"
                    tk.Label(alertas_container, text=alerta_suministros, 
                            font=("Arial", 9), bg="#ecf0f1", fg="#e67e22").pack(anchor="w")
                
                # Alerta de suministros agotados
                cursor.execute("SELECT COUNT(*) FROM Suministros WHERE cantidad = 0")
                suministros_agotados = cursor.fetchone()[0]
                
                if suministros_agotados > 0:
                    alerta_agotados = f"🚨 {suministros_agotados} suministros agotados"
                    tk.Label(alertas_container, text=alerta_agotados, 
                            font=("Arial", 9), bg="#ecf0f1", fg="#e74c3c").pack(anchor="w")
                
            except Exception as e:
                tk.Label(alertas_container, text="Error al verificar alertas", 
                        font=("Arial", 9), bg="#ecf0f1", fg="#e74c3c").pack(anchor="w")
            finally:
                conn.close()

    verificar_alertas()

    # --- Información del sistema ---
    info_frame = tk.Frame(actions_frame, bg="white")
    info_frame.pack(fill="x", padx=20, pady=10)

    tk.Label(info_frame, text="Sistema Albergue v1.0", 
             font=("Arial", 10), bg="white", fg="#7f8c8d").pack()

    # Botón de actualizar
    def actualizar_dashboard():
        # Limpiar y recargar datos
        for item in tabla_recientes.get_children():
            tabla_recientes.delete(item)
        cargar_recientes()
        cargar_suministros()
        
        # Limpiar alertas y regenerar
        for widget in alertas_frame.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.destroy()
        verificar_alertas()
        
        messagebox.showinfo("Actualizado", "Dashboard actualizado correctamente")

    crear_boton_accion(info_frame, "🔄 Actualizar Dashboard", actualizar_dashboard, "#95a5a6")

# Función auxiliar para importar módulos dinámicamente
def importar_y_ejecutar(modulo, funcion, ventana):
    try:
        import importlib
        mod = importlib.import_module(modulo)
        func = getattr(mod, funcion)
        func(ventana)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir la ventana: {e}")
