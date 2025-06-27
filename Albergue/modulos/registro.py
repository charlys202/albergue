import tkinter as tk
import datetime
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from conexion import conectar_bd

def abrir_ventana_registro(padre):
    ventana = tk.Toplevel(padre)
    ventana.title("Registro de Huésped")
    ventana.geometry("600x500")
    ventana.configure(bg="#f8f9fa")
    ventana.resizable(False, False)

    # --- HEADER VERDE ---
    header_frame = tk.Frame(ventana, bg="#27ae60", height=70)
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)
    
    tk.Label(header_frame, text="📋 REGISTRO DE HUÉSPED", 
             font=("Arial", 16, "bold"), fg="white", bg="#27ae60").pack(side="left", padx=20, pady=20)
    
    fecha_label = tk.Label(header_frame, text=datetime.datetime.now().strftime("%d/%m/%Y"), 
                          font=("Arial", 12), fg="#d5f4e6", bg="#27ae60")
    fecha_label.pack(side="right", padx=20, pady=25)

    # --- CONTENEDOR PRINCIPAL ---
    main_container = tk.Frame(ventana, bg="#f8f9fa")
    main_container.pack(fill="both", expand=True, padx=20, pady=20)

    # --- SECCIÓN: INFORMACIÓN PERSONAL ---
    info_personal_frame = tk.LabelFrame(main_container, text="👤 Información Personal", 
                                       font=("Arial", 12, "bold"), fg="#2c3e50", bg="#ffffff",
                                       relief="raised", bd=2)
    info_personal_frame.pack(fill="x", pady=(0, 15))

    # Fila 1: Nombre y Apellidos
    fila1 = tk.Frame(info_personal_frame, bg="#ffffff")
    fila1.pack(fill="x", padx=15, pady=10)
    
    tk.Label(fila1, text="Nombre completo:", font=("Arial", 10, "bold"), 
             bg="#ffffff", fg="#2c3e50").pack(anchor="w")
    entrada_nombre = tk.Entry(fila1, font=("Arial", 11), relief="solid", bd=1, 
                             bg="#ffffff", fg="#2c3e50", width=25)
    entrada_nombre.pack(side="left", fill="x", expand=True, padx=(0, 10))
    
    tk.Label(fila1, text="Apellidos:", font=("Arial", 10, "bold"), 
             bg="#ffffff", fg="#2c3e50").pack(side="right", anchor="e")
    entrada_apellidos = tk.Entry(fila1, font=("Arial", 11), relief="solid", bd=1, 
                                bg="#ffffff", fg="#2c3e50", width=25)
    entrada_apellidos.pack(side="right")

    # Fila 2: Nacionalidad y Género
    fila2 = tk.Frame(info_personal_frame, bg="#ffffff")
    fila2.pack(fill="x", padx=15, pady=10)
    
    tk.Label(fila2, text="Nacionalidad:", font=("Arial", 10, "bold"), 
             bg="#ffffff", fg="#2c3e50").pack(anchor="w")
    entrada_nacionalidad = tk.Entry(fila2, font=("Arial", 11), relief="solid", bd=1, 
                                   bg="#ffffff", fg="#2c3e50", width=25)
    entrada_nacionalidad.pack(side="left", fill="x", expand=True, padx=(0, 10))
    
    tk.Label(fila2, text="Género:", font=("Arial", 10, "bold"), 
             bg="#ffffff", fg="#2c3e50").pack(side="right", anchor="e")
    combo_genero = ttk.Combobox(fila2, values=["Masculino", "Femenino", "Otro"], 
                               font=("Arial", 11), width=22, state="readonly")
    combo_genero.pack(side="right")

    # --- SECCIÓN: DATOS ADICIONALES ---
    datos_adicionales_frame = tk.LabelFrame(main_container, text="📊 Datos Adicionales", 
                                          font=("Arial", 12, "bold"), fg="#2c3e50", bg="#ffffff",
                                          relief="raised", bd=2)
    datos_adicionales_frame.pack(fill="x", pady=(0, 15))

    # Fila 3: Edad y Fecha
    fila3 = tk.Frame(datos_adicionales_frame, bg="#ffffff")
    fila3.pack(fill="x", padx=15, pady=10)
    
    tk.Label(fila3, text="Edad:", font=("Arial", 10, "bold"), 
             bg="#ffffff", fg="#2c3e50").pack(anchor="w")
    entrada_edad = tk.Entry(fila3, font=("Arial", 11), relief="solid", bd=1, 
                           bg="#ffffff", fg="#2c3e50", width=10)
    entrada_edad.pack(side="left", padx=(0, 10))
    
    tk.Label(fila3, text="Fecha de ingreso:", font=("Arial", 10, "bold"), 
             bg="#ffffff", fg="#2c3e50").pack(side="right", anchor="e", padx=(0, 10))
    entrada_fecha = DateEntry(fila3, font=("Arial", 11), width=20)
    entrada_fecha.pack(side="right")

    # Fila 4: Estado de salud
    fila4 = tk.Frame(datos_adicionales_frame, bg="#ffffff")
    fila4.pack(fill="x", padx=15, pady=10)
    
    tk.Label(fila4, text="Estado de salud:", font=("Arial", 10, "bold"), 
             bg="#ffffff", fg="#2c3e50").pack(anchor="w")
    entrada_salud = tk.Entry(fila4, font=("Arial", 11), relief="solid", bd=1, 
                            bg="#ffffff", fg="#2c3e50")
    entrada_salud.pack(fill="x", pady=(5, 0))

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

    # --- SEPARADOR ---
    separador = tk.Frame(main_container, height=2, bg="#bdc3c7")
    separador.pack(fill="x", pady=15)

    # --- BOTONES ---
    botones_frame = tk.Frame(main_container, bg="#f8f9fa")
    botones_frame.pack(fill="x")

    def crear_boton_registro(texto, comando, color, side="left"):
        btn = tk.Button(botones_frame, text=texto, command=comando,
                       bg=color, fg="white", font=("Arial", 12, "bold"),
                       relief="flat", cursor="hand2", width=15, height=2)
        btn.pack(side=side, padx=20)
        
        # Efectos hover
        def on_enter(e): btn.configure(relief="raised")
        def on_leave(e): btn.configure(relief="flat")
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    crear_boton_registro("✅ Registrar", registrar, "#27ae60", "left")
    crear_boton_registro("❌ Cancelar", ventana.destroy, "#95a5a6", "right")


    


    
