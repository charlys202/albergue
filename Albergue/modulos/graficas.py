import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as patches
from conexion import conectar_bd
import datetime

def abrir_ventana_graficas(padre):
    ventana = tk.Toplevel(padre)
    ventana.title("Gráficas del Albergue")
    ventana.geometry("1200x800")
    ventana.configure(bg="#5f9ea0")  # Color similar al de la imagen
    ventana.resizable(True, True)

    # --- HEADER ---
    header_frame = tk.Frame(ventana, bg="#5f9ea0", height=80)
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)
    
    title_label = tk.Label(header_frame, text="Gráficas del Albergue", 
                          font=("Arial", 24, "bold"), fg="#ffff00", bg="#5f9ea0")  # Texto amarillo
    title_label.pack(expand=True, pady=20)

    # --- CONTENEDOR PRINCIPAL CON FONDO GRIS ---
    main_frame = tk.Frame(ventana, bg="#808080", relief="raised", bd=3)  # Fondo gris como en la imagen
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # --- CONTENEDOR DE GRÁFICAS ---
    graficas_container = tk.Frame(main_frame, bg="#808080")
    graficas_container.pack(fill="both", expand=True, padx=20, pady=20)

    # Configurar matplotlib para fondo oscuro
    plt.style.use('dark_background')

    # --- GRÁFICA DE ENTRADAS Y SALIDAS (IZQUIERDA) ---
    frame_entradas = tk.Frame(graficas_container, bg="#808080")
    frame_entradas.pack(side="left", fill="both", expand=True, padx=(0, 10))

    label_entradas = tk.Label(frame_entradas, text="Entras y salidas", 
                             font=("Arial", 14, "bold"), fg="#ffff00", bg="#808080")
    label_entradas.pack(pady=(0, 10))

    # Crear figura para gráfico de barras
    fig_barras, ax_barras = plt.subplots(figsize=(6, 5), facecolor='#808080')
    ax_barras.set_facecolor('#404040')

    def obtener_datos_entradas_salidas():
        conn = conectar_bd()
        datos = {'dias': [], 'entradas': [], 'salidas': []}
        
        if conn:
            try:
                cursor = conn.cursor()
                
                # Obtener datos de los últimos 7 días
                for i in range(6, -1, -1):
                    fecha = datetime.date.today() - datetime.timedelta(days=i)
                    
                    # Contar entradas del día
                    cursor.execute("SELECT COUNT(*) FROM PersonasAlbergadas WHERE fecha_ingreso = ?", (fecha,))
                    entradas = cursor.fetchone()[0] or 0
                    
                    # Simular salidas (en un sistema real, tendrías una tabla de salidas)
                    # Por ahora usaremos datos simulados basados en las entradas
                    salidas = max(0, entradas - (i % 3))  # Datos simulados
                    
                    datos['dias'].append(fecha.strftime('%d/%m'))
                    datos['entradas'].append(entradas)
                    datos['salidas'].append(salidas)
                    
            except Exception as e:
                print(f"Error al obtener datos: {e}")
                # Datos por defecto si hay error
                datos = {
                    'dias': ['21/06', '22/06', '23/06', '24/06', '25/06', '26/06', '27/06'],
                    'entradas': [5, 8, 6, 10, 7, 9, 12],
                    'salidas': [3, 5, 4, 7, 5, 6, 8]
                }
            finally:
                if conn:
                    conn.close()
        else:
            # Datos por defecto si no hay conexión
            datos = {
                'dias': ['21/06', '22/06', '23/06', '24/06', '25/06', '26/06', '27/06'],
                'entradas': [5, 8, 6, 10, 7, 9, 12],
                'salidas': [3, 5, 4, 7, 5, 6, 8]
            }
        
        return datos

    # Obtener y graficar datos
    datos_entradas = obtener_datos_entradas_salidas()
    
    x_pos = range(len(datos_entradas['dias']))
    width = 0.35

    barras_entradas = ax_barras.bar([x - width/2 for x in x_pos], datos_entradas['entradas'], 
                                   width, label='Entradas', color='#4CAF50', alpha=0.8)
    barras_salidas = ax_barras.bar([x + width/2 for x in x_pos], datos_entradas['salidas'], 
                                  width, label='Salidas', color='#FF5722', alpha=0.8)

    ax_barras.set_xlabel('Días', color='white', fontsize=12)
    ax_barras.set_ylabel('Cantidad', color='white', fontsize=12)
    ax_barras.set_xticks(x_pos)
    ax_barras.set_xticklabels(datos_entradas['dias'], color='white')
    ax_barras.tick_params(colors='white')
    ax_barras.legend()
    ax_barras.grid(True, alpha=0.3)

    # Integrar gráfico en tkinter
    canvas_barras = FigureCanvasTkAgg(fig_barras, frame_entradas)
    canvas_barras.draw()
    canvas_barras.get_tk_widget().pack(fill="both", expand=True)

    # --- GRÁFICA DE SUMINISTROS (DERECHA) ---
    frame_suministros = tk.Frame(graficas_container, bg="#808080")
    frame_suministros.pack(side="right", fill="both", expand=True, padx=(10, 0))

    label_suministros = tk.Label(frame_suministros, text="Suministros", 
                                font=("Arial", 14, "bold"), fg="#ffff00", bg="#808080")
    label_suministros.pack(pady=(0, 10))

    # Crear figura para gráfico circular
    fig_pie, ax_pie = plt.subplots(figsize=(6, 5), facecolor='#808080')
    ax_pie.set_facecolor('#404040')

    def obtener_datos_suministros():
        conn = conectar_bd()
        
        # En un sistema real, tendrías una tabla de suministros
        # Por ahora usaremos datos simulados
        suministros = {
            'Alimentos': 45,
            'Medicinas': 25,
            'Ropa': 20,
            'Otros': 10
        }
        
        # Si tienes una tabla de suministros, descomenta y modifica esto:
        """
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT tipo_suministro, cantidad FROM Suministros")
                resultados = cursor.fetchall()
                suministros = {}
                for tipo, cantidad in resultados:
                    suministros[tipo] = cantidad
            except Exception as e:
                print(f"Error al obtener suministros: {e}")
            finally:
                conn.close()
        """
        
        return suministros

    # Obtener y graficar datos de suministros
    datos_suministros = obtener_datos_suministros()
    
    labels = list(datos_suministros.keys())
    sizes = list(datos_suministros.values())
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']

    wedges, texts, autotexts = ax_pie.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                                         startangle=90, textprops={'color': 'white', 'fontsize': 10})
    
    ax_pie.set_title('Distribución de Suministros', color='white', fontsize=12, pad=20)

    # Integrar gráfico en tkinter
    canvas_pie = FigureCanvasTkAgg(fig_pie, frame_suministros)
    canvas_pie.draw()
    canvas_pie.get_tk_widget().pack(fill="both", expand=True)

    # --- BOTÓN REGRESAR ---
    boton_frame = tk.Frame(ventana, bg="#5f9ea0")
    boton_frame.pack(fill="x", pady=10)

    def crear_boton_regresar():
        btn = tk.Button(boton_frame, text="Regresar", command=ventana.destroy,
                       bg="#ffff00", fg="black", font=("Arial", 12, "bold"),
                       relief="raised", cursor="hand2", width=15, height=2)
        btn.pack(pady=10)
        
        def on_enter(e):
            btn.configure(bg="#ffff99")
        def on_leave(e):
            btn.configure(bg="#ffff00")
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    crear_boton_regresar()

    # Función para actualizar gráficas
    def actualizar_graficas():
        try:
            # Limpiar gráficas existentes
            ax_barras.clear()
            ax_pie.clear()
            
            # Reconfigurar estilo
            ax_barras.set_facecolor('#404040')
            ax_pie.set_facecolor('#404040')
            
            # Actualizar datos y redibujar
            datos_entradas = obtener_datos_entradas_salidas()
            
            x_pos = range(len(datos_entradas['dias']))
            width = 0.35
            
            ax_barras.bar([x - width/2 for x in x_pos], datos_entradas['entradas'], 
                         width, label='Entradas', color='#4CAF50', alpha=0.8)
            ax_barras.bar([x + width/2 for x in x_pos], datos_entradas['salidas'], 
                         width, label='Salidas', color='#FF5722', alpha=0.8)
            
            ax_barras.set_xlabel('Días', color='white', fontsize=12)
            ax_barras.set_ylabel('Cantidad', color='white', fontsize=12)
            ax_barras.set_xticks(x_pos)
            ax_barras.set_xticklabels(datos_entradas['dias'], color='white')
            ax_barras.tick_params(colors='white')
            ax_barras.legend()
            ax_barras.grid(True, alpha=0.3)
            
            # Actualizar gráfico de suministros
            datos_suministros = obtener_datos_suministros()
            labels = list(datos_suministros.keys())
            sizes = list(datos_suministros.values())
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
            
            ax_pie.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                      startangle=90, textprops={'color': 'white', 'fontsize': 10})
            ax_pie.set_title('Distribución de Suministros', color='white', fontsize=12, pad=20)
            
            # Redibujar canvas
            canvas_barras.draw()
            canvas_pie.draw()
            
            messagebox.showinfo("Actualizado", "Gráficas actualizadas correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar gráficas: {e}")

    # Botón para actualizar gráficas
    btn_actualizar = tk.Button(boton_frame, text="Actualizar Gráficas", command=actualizar_graficas,
                              bg="#4CAF50", fg="white", font=("Arial", 11, "bold"),
                              relief="raised", cursor="hand2", width=18, height=1)
    btn_actualizar.pack(side="right", padx=20, pady=5)

    def on_enter_actualizar(e):
        btn_actualizar.configure(bg="#45a049")
    def on_leave_actualizar(e):
        btn_actualizar.configure(bg="#4CAF50")
    
    btn_actualizar.bind("<Enter>", on_enter_actualizar)
    btn_actualizar.bind("<Leave>", on_leave_actualizar)