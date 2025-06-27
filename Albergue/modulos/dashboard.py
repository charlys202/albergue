import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from conexion import conectar_bd


def abrir_ventana_dashboard(padre):
    ventana = tk.Toplevel(padre)
    ventana.title("Dashboard - Albergue Fronterizo")
    ventana.geometry("1200x700")
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

    # --- Panel de estadísticas (izquierda) ---
    stats_frame = tk.Frame(main_container, bg="#ffffff", relief="raised", bd=1)
    stats_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

    # Título de estadísticas
    tk.Label(stats_frame, text="Estadísticas Generales", 
             font=("Arial", 16, "bold"), bg="white", fg="#2c3e50").pack(pady=15)

    # Container para tarjetas de estadísticas
    cards_container = tk.Frame(stats_frame, bg="white")
    cards_container.pack(fill="x", padx=20)

    # Función para crear tarjetas de estadísticas
    def crear_tarjeta_stat(parent, titulo, valor, color):
        card = tk.Frame(parent, bg=color, relief="raised", bd=2, height=100)
        card.pack(fill="x", pady=10)
        card.pack_propagate(False)
        
        tk.Label(card, text=titulo, font=("Arial", 12, "bold"), 
                bg=color, fg="white").pack(pady=(15, 5))
        tk.Label(card, text=str(valor), font=("Arial", 20, "bold"), 
                bg=color, fg="white").pack()

    # Obtener estadísticas de la base de datos
    def obtener_estadisticas():
        conn = conectar_bd()
        stats = {"total_huespedes": 0, "huespedes_hoy": 0, "voluntarios_activos": 0}
        
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

    # --- Lista de huéspedes recientes ---
    recientes_frame = tk.Frame(stats_frame, bg="white")
    recientes_frame.pack(fill="both", expand=True, padx=20, pady=20)

    tk.Label(recientes_frame, text="Huéspedes Recientes", 
             font=("Arial", 14, "bold"), bg="white", fg="#2c3e50").pack(anchor="w")

    # Tabla de huéspedes recientes
    columnas_recientes = ("Nombre", "Nacionalidad", "Fecha")
    tabla_recientes = ttk.Treeview(recientes_frame, columns=columnas_recientes, show="headings", height=8)
    
    for col in columnas_recientes:
        tabla_recientes.heading(col, text=col)
        tabla_recientes.column(col, width=120)

    tabla_recientes.pack(fill="both", expand=True, pady=10)

    # Cargar huéspedes recientes
    def cargar_recientes():
        conn = conectar_bd()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT TOP 10 nombre + ' ' + apellidos, nacionalidad, fecha_ingreso
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

    # --- Panel de acciones rápidas (derecha) ---
    actions_frame = tk.Frame(main_container, bg="#ffffff", relief="raised", bd=1)
    actions_frame.pack(side="right", fill="y", padx=(10, 0))

    tk.Label(actions_frame, text="Acciones Rápidas", 
             font=("Arial", 16, "bold"), bg="white", fg="#2c3e50").pack(pady=15)

    # Función para crear botones de acción
    def crear_boton_accion(parent, texto, comando, color):
        btn = tk.Button(parent, text=texto, command=comando, 
                       bg=color, fg="white", font=("Arial", 11, "bold"),
                       relief="flat", cursor="hand2", width=20, height=2)
        btn.pack(pady=10, padx=20)
        
        # Efectos hover
        def on_enter(e):
            btn.configure(relief="raised")
        def on_leave(e):
            btn.configure(relief="flat")
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    # Botones de acción
    crear_boton_accion(actions_frame, "Nuevo Huésped", 
                      lambda: importar_y_ejecutar("modulos.registro", "abrir_ventana_registro", ventana), "#3498db")
    
    crear_boton_accion(actions_frame, "Consultar Huéspedes", 
                      lambda: importar_y_ejecutar("modulos.consultas", "abrir_ventana_consulta", ventana), "#27ae60")
    
    crear_boton_accion(actions_frame, "Registrar Voluntario", 
                      lambda: importar_y_ejecutar("modulos.registro_voluntarios", "abrir_ventana_voluntarios", ventana), "#e67e22")

    # --- Sección de alertas ---
    alertas_frame = tk.Frame(actions_frame, bg="#ecf0f1", relief="sunken", bd=1)
    alertas_frame.pack(fill="x", padx=20, pady=20)

    tk.Label(alertas_frame, text="Alertas del Sistema", 
             font=("Arial", 12, "bold"), bg="#ecf0f1", fg="#2c3e50").pack(pady=10)

    # Verificar capacidad del albergue
    def verificar_alertas():
        conn = conectar_bd()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM PersonasAlbergadas")
                total = cursor.fetchone()[0]
                
                # Alerta de capacidad (asumiendo capacidad máxima de 100)
                if total > 80:
                    alerta_text = f"⚠️ Alerta: Capacidad al {total}%"
                    color_alerta = "#e74c3c"
                elif total > 60:
                    alerta_text = f"⚡ Atención: Capacidad al {total}%"
                    color_alerta = "#f39c12"
                else:
                    alerta_text = f"✅ Capacidad normal: {total}%"
                    color_alerta = "#27ae60"
                
                tk.Label(alertas_frame, text=alerta_text, 
                        font=("Arial", 10), bg="#ecf0f1", fg=color_alerta).pack(pady=5)
                
            except Exception as e:
                tk.Label(alertas_frame, text="Error al verificar alertas", 
                        font=("Arial", 10), bg="#ecf0f1", fg="#e74c3c").pack(pady=5)
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
        verificar_alertas()
        messagebox.showinfo("Actualizado", "Dashboard actualizado correctamente")

    crear_boton_accion(actions_frame, "Actualizar Dashboard", actualizar_dashboard, "#95a5a6")

# Función auxiliar para importar módulos dinámicamente
def importar_y_ejecutar(modulo, funcion, ventana):
    try:
        import importlib
        mod = importlib.import_module(modulo)
        func = getattr(mod, funcion)
        func(ventana)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir la ventana: {e}")