import tkinter as tk
from tkinter import ttk, messagebox
from conexion import conectar_bd

def abrir_ventana_voluntarios(padre):
    ventana = tk.Toplevel(padre)
    ventana.title("Registro de Voluntarios")
    ventana.geometry("600x550")
    ventana.configure(bg="#f8f9fa")
    ventana.resizable(False, False)

    # --- HEADER MORADO ---
    header_frame = tk.Frame(ventana, bg="#9b59b6", height=70)
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)
    
    tk.Label(header_frame, text="👥 REGISTRO DE VOLUNTARIOS", 
             font=("Arial", 16, "bold"), fg="white", bg="#9b59b6").pack(side="left", padx=20, pady=20)
    
    # Icono de usuario
    tk.Label(header_frame, text="👤", font=("Arial", 20), 
             fg="#e8d5f0", bg="#9b59b6").pack(side="right", padx=20, pady=20)

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
    
    tk.Label(fila1, text="Nombre:", font=("Arial", 10, "bold"), 
             bg="#ffffff", fg="#2c3e50").pack(anchor="w")
    entrada_nombre = tk.Entry(fila1, font=("Arial", 11), relief="solid", bd=1, 
                             bg="#ffffff", fg="#2c3e50", width=25)
    entrada_nombre.pack(side="left", fill="x", expand=True, padx=(0, 10))
    
    tk.Label(fila1, text="Apellidos:", font=("Arial", 10, "bold"), 
             bg="#ffffff", fg="#2c3e50").pack(side="right", anchor="e")
    entrada_apellidos = tk.Entry(fila1, font=("Arial", 11), relief="solid", bd=1, 
                                bg="#ffffff", fg="#2c3e50", width=25)
    entrada_apellidos.pack(side="right")

    # Fila 2: Teléfono y Email
    fila2 = tk.Frame(info_personal_frame, bg="#ffffff")
    fila2.pack(fill="x", padx=15, pady=10)
    
    tk.Label(fila2, text="Teléfono:", font=("Arial", 10, "bold"), 
             bg="#ffffff", fg="#2c3e50").pack(anchor="w")
    entrada_telefono = tk.Entry(fila2, font=("Arial", 11), relief="solid", bd=1, 
                               bg="#ffffff", fg="#2c3e50", width=25)
    entrada_telefono.pack(side="left", fill="x", expand=True, padx=(0, 10))
    
    tk.Label(fila2, text="Email:", font=("Arial", 10, "bold"), 
             bg="#ffffff", fg="#2c3e50").pack(side="right", anchor="e")
    entrada_correo = tk.Entry(fila2, font=("Arial", 11), relief="solid", bd=1, 
                             bg="#ffffff", fg="#2c3e50", width=25)
    entrada_correo.pack(side="right")

    # --- SECCIÓN: INFORMACIÓN LABORAL ---
    info_laboral_frame = tk.LabelFrame(main_container, text="💼 Información Laboral", 
                                      font=("Arial", 12, "bold"), fg="#2c3e50", bg="#ffffff",
                                      relief="raised", bd=2)
    info_laboral_frame.pack(fill="x", pady=(0, 15))

    # Fila 3: Rol y Horario
    fila3 = tk.Frame(info_laboral_frame, bg="#ffffff")
    fila3.pack(fill="x", padx=15, pady=10)
    
    tk.Label(fila3, text="Rol/Función:", font=("Arial", 10, "bold"), 
             bg="#ffffff", fg="#2c3e50").pack(anchor="w")
    combo_rol = ttk.Combobox(fila3, values=["Médico", "Apoyo General", "Asistente Social", 
                                           "Cocinero", "Seguridad", "Intérprete", "Coordinador"], 
                           font=("Arial", 11), width=22, state="readonly")
    combo_rol.pack(side="left", fill="x", expand=True, padx=(0, 10))
    
    tk.Label(fila3, text="Horario:", font=("Arial", 10, "bold"), 
             bg="#ffffff", fg="#2c3e50").pack(side="right", anchor="e")
    entrada_horario = tk.Entry(fila3, font=("Arial", 11), relief="solid", bd=1, 
                              bg="#ffffff", fg="#2c3e50", width=25)
    entrada_horario.pack(side="right")

    # Fila 4: Observaciones
    fila4 = tk.Frame(info_laboral_frame, bg="#ffffff")
    fila4.pack(fill="x", padx=15, pady=10)
    
    tk.Label(fila4, text="Observaciones (opcional):", font=("Arial", 10, "bold"), 
             bg="#ffffff", fg="#2c3e50").pack(anchor="w")
    entrada_observaciones = tk.Text(fila4, font=("Arial", 11), relief="solid", bd=1, 
                                   bg="#ffffff", fg="#2c3e50", height=3, width=50)
    entrada_observaciones.pack(fill="x", pady=(5, 0))

    # --- SEPARADOR ---
    separador = tk.Frame(main_container, height=2, bg="#bdc3c7")
    separador.pack(fill="x", pady=15)


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

    # --- BOTONES ---
    botones_frame = tk.Frame(main_container, bg="#f8f9fa")
    botones_frame.pack(fill="x")

    def crear_boton_voluntario(texto, comando, color, side="left"):
        btn = tk.Button(botones_frame, text=texto, command=comando,
                       bg=color, fg="white", font=("Arial", 12, "bold"),
                       relief="flat", cursor="hand2", width=18, height=2)
        btn.pack(side=side, padx=20)
        
        def on_enter(e): btn.configure(relief="raised")
        def on_leave(e): btn.configure(relief="flat")
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    crear_boton_voluntario("✅ Registrar Voluntario", registrar_voluntario, "#9b59b6", "left")
    crear_boton_voluntario("❌ Cancelar", ventana.destroy, "#95a5a6", "right")
