import tkinter as tk
from tkinter import messagebox

def generar_informe():
    ocupacion = int(huespedes_actuales.get()) / int(capacidades.get()) * 100
    resumen = (
        f"Resumen del Albergue:\n"
        f"Capacidad: {capacidades.get()}\n"
        f"Huéspedes actuales: {huespedes_actuales.get()}\n"
        f"Ocupación: {ocupacion:.2f}%\n\n"
        f"Camas disponibles: {camas_disponibles.get()}\n"
        f"Camas ocupadas: {camas_ocupadas.get()}\n"
        f"En mantenimiento: {camas_mantenimiento.get()}\n\n"
        f"Inventario:\n"
        f"Agua: {agua_actual.get()} (Mín: {agua_minima.get()})\n"
        f"Pan: {pan_actual.get()} (Mín: {pan_minima.get()})\n"
        f"Mantas: {mantas_actual.get()} (Mín: {mantas_minima.get()})"
    )
    messagebox.showinfo("Informe generado", resumen)


ventana = tk.Tk()
ventana.title("Administración del Albergue")
ventana.geometry("500x500")
ventana.config(bg="#468fa6") 


tk.Label(ventana, text="Administración del Albergue", font=("Arial", 16, "bold"), fg="gold", bg="#468fa6").pack(pady=10)


frame_resumen = tk.Frame(ventana, bg="#cccccc", bd=2, relief="ridge", padx=10, pady=10)
frame_resumen.place(x=30, y=60)

tk.Label(frame_resumen, text="Resumen General del Albergue", bg="#cccccc", font=("Arial", 10, "bold"), fg="darkblue").grid(row=0, column=0, columnspan=2)

tk.Label(frame_resumen, text="Capacidades:", bg="#cccccc").grid(row=1, column=0, sticky="w")
capacidades = tk.StringVar(value="50")
tk.Entry(frame_resumen, textvariable=capacidades, width=5).grid(row=1, column=1)

tk.Label(frame_resumen, text="Huéspedes actuales:", bg="#cccccc").grid(row=2, column=0, sticky="w")
huespedes_actuales = tk.StringVar(value="38")
tk.Entry(frame_resumen, textvariable=huespedes_actuales, width=5).grid(row=2, column=1)

tk.Label(frame_resumen, text="Ocupado: 76%", bg="#cccccc").grid(row=3, column=0, columnspan=2)

frame_camas = tk.Frame(ventana, bg="#356b81", bd=2, relief="ridge", padx=10, pady=10)
frame_camas.place(x=250, y=60)

tk.Label(frame_camas, text="Camas y Habitaciones", bg="#356b81", fg="white", font=("Arial", 10, "bold")).pack()

camas_disponibles = tk.StringVar(value="12")
tk.Label(frame_camas, text="Camas disponibles", bg="yellow").pack(fill="x")
tk.Entry(frame_camas, textvariable=camas_disponibles, justify="center").pack()

camas_ocupadas = tk.StringVar(value="38")
tk.Label(frame_camas, text="Camas ocupadas", bg="orange").pack(fill="x")
tk.Entry(frame_camas, textvariable=camas_ocupadas, justify="center").pack()

camas_mantenimiento = tk.StringVar(value="2")
tk.Label(frame_camas, text="En mantenimiento", bg="red", fg="white").pack(fill="x")
tk.Entry(frame_camas, textvariable=camas_mantenimiento, justify="center").pack()


frame_inv = tk.Frame(ventana, bg="#555555", bd=2, relief="ridge", padx=10, pady=10)
frame_inv.place(x=30, y=200)

tk.Label(frame_inv, text="Inventario y suministros", fg="white", bg="#555555", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=3)

tk.Label(frame_inv, text="Suministro", bg="#555555", fg="white").grid(row=1, column=0)
tk.Label(frame_inv, text="Cantidad Actual", bg="#555555", fg="white").grid(row=1, column=1)
tk.Label(frame_inv, text="Cantidad Mínima", bg="#555555", fg="white").grid(row=1, column=2)

tk.Label(frame_inv, text="AGUA", bg="#add8e6").grid(row=2, column=0)
agua_actual = tk.StringVar(value="25")
agua_minima = tk.StringVar(value="20")
tk.Entry(frame_inv, textvariable=agua_actual, width=5).grid(row=2, column=1)
tk.Entry(frame_inv, textvariable=agua_minima, width=5).grid(row=2, column=2)

tk.Label(frame_inv, text="Pan", bg="#f4e1a1").grid(row=3, column=0)
pan_actual = tk.StringVar(value="8")
pan_minima = tk.StringVar(value="15")
tk.Entry(frame_inv, textvariable=pan_actual, width=5).grid(row=3, column=1)
tk.Entry(frame_inv, textvariable=pan_minima, width=5).grid(row=3, column=2)

tk.Label(frame_inv, text="Mantas", bg="#d0d0ff").grid(row=4, column=0)
mantas_actual = tk.StringVar(value="20")
mantas_minima = tk.StringVar(value="25")
tk.Entry(frame_inv, textvariable=mantas_actual, width=5).grid(row=4, column=1)
tk.Entry(frame_inv, textvariable=mantas_minima, width=5).grid(row=4, column=2)


tk.Button(ventana, text="Generar Informe", bg="yellow", command=generar_informe).place(x=350, y=400)

ventana.mainloop()
