import tkinter as tk
from tkinter import ttk, messagebox
from modulos.registro import abrir_ventana_registro
from modulos.consultas import abrir_ventana_consulta
from modulos.registro_voluntarios import abrir_ventana_voluntarios
from modulos.dashboard import abrir_ventana_dashboard  # Nueva importación

def main():
    ventana = tk.Tk()
    ventana.title("Sistema Albergue Fronterizo")
    ventana.geometry("500x400")
    ventana.config(bg="#f0f0f0")
    
    # Centrar la ventana
    ventana.eval('tk::PlaceWindow . center')

    # Header principal
    header_frame = tk.Frame(ventana, bg="#2c3e50", height=80)
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)
    
    title_label = tk.Label(header_frame, text="SISTEMA ALBERGUE FRONTERIZO", 
                          font=("Arial", 18, "bold"), fg="white", bg="#2c3e50")
    title_label.pack(expand=True)

    # Contenedor principal
    main_frame = tk.Frame(ventana, bg="#f0f0f0")
    main_frame.pack(fill="both", expand=True, padx=30, pady=30)

    tk.Label(main_frame, text="Seleccione una opción:", 
             font=("Arial", 14), bg="#f0f0f0", fg="#2c3e50").pack(pady=(0, 20))

    # Función para crear botones estilizados
    def crear_boton(texto, comando, color):
        btn = tk.Button(main_frame, text=texto, command=comando, 
                       bg=color, fg="white", font=("Arial", 12, "bold"),
                       relief="flat", cursor="hand2", width=25, height=2)
        btn.pack(pady=8)
        

        def on_enter(e):
            btn.configure(relief="raised", bg=darken_color(color))
        def on_leave(e):
            btn.configure(relief="flat", bg=color)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    def darken_color(color):
        color_map = {
            "#3498db": "#2980b9",
            "#27ae60": "#229954",
            "#e67e22": "#d35400",
            "#9b59b6": "#8e44ad",
            "#e74c3c": "#c0392b"
        }
        return color_map.get(color, color)

    # Botones del menú
    crear_boton("📊 Dashboard Principal", lambda: abrir_ventana_dashboard(ventana), "#3498db")
    crear_boton("👥 Registro de Huéspedes", lambda: abrir_ventana_registro(ventana), "#27ae60")
    crear_boton("🔍 Consultar Huéspedes", lambda: abrir_ventana_consulta(ventana), "#e67e22")
    crear_boton("🤝 Registrar Voluntarios", lambda: abrir_ventana_voluntarios(ventana), "#9b59b6")
    crear_boton("❌ Salir", ventana.quit, "#e74c3c")

    # Footer
    footer_frame = tk.Frame(ventana, bg="#ecf0f1", height=30)
    footer_frame.pack(fill="x", side="bottom")
    footer_frame.pack_propagate(False)
    
    tk.Label(footer_frame, text="Sistema de Gestión Albergue Fronterizo v1.0", 
             font=("Arial", 9), bg="#ecf0f1", fg="#7f8c8d").pack(expand=True)

    ventana.mainloop()

if __name__ == "__main__":
    main()
