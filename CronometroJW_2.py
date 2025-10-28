import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import messagebox
import re 
import time # <--- IMPORTADO

class CronometroAvanzado:
    def __init__(self, root):
        self.root = root
        self.root.title("Cronómetro para Discursos v2")
        self.root.geometry("700x700") 
        self.root.minsize(400, 500) 

        # --- Estado del cronómetro ---
        self.running = False
        self.elapsed_ms = 0 
        self.target_ms = 0 

        # --- Variables de tiempo preciso ---
        self.anchor_time = 0.0
        self.start_elapsed_ms = 0.0

        # --- Variables de Tkinter ---
        self.time_str = tk.StringVar(value="00:00.0")
        self.color_var = tk.BooleanVar(value=True) 
        self.second_window_var = tk.BooleanVar()
        self.mode_var = tk.StringVar(value="ascendente") 

        # --- Definición de Fuentes (Segoe UI es la de Win 11) ---
        try:
            # Intenta usar fuentes más modernas (estilo Win 11)
            self.default_font = font.Font(family="Segoe UI", size=10)
            timer_font_family = "Consolas"
        except tk.TclError:
            # Fallback para otros sistemas
            self.default_font = font.Font(family="Helvetica", size=10)
            timer_font_family = "Courier New"
            
        self.timer_font = font.Font(family=timer_font_family, size=48, weight="bold")
        self.second_timer_font = font.Font(family=timer_font_family, size=60, weight="bold")

        self.second_window = None
        self.second_label = None

        # --- Creación de Estilos (La clave de la modernización) ---
        self.style = ttk.Style(self.root)
        # 'clam' es un tema limpio y plano, bueno como base
        self.style.theme_use('clam') 

        # Configuración de fuente por defecto para todos los widgets ttk
        self.style.configure('.', font=self.default_font, padding=4)

        # --- Estilos del Timer Principal ---
        self.style.configure(
            'Timer.TLabel', 
            font=self.timer_font, 
            padding=10, 
            anchor=tk.CENTER
        )
        self.style.configure('Black.Timer.TLabel', foreground='black')
        self.style.configure('Green.Timer.TLabel', foreground='#008F00') # Un verde más bonito
        self.style.configure('Orange.Timer.TLabel', foreground='#FF8C00')
        self.style.configure('Red.Timer.TLabel', foreground='#D20000')

        # --- Estilos del Timer Secundario ---
        self.style.configure(
            'Second.TLabel', 
            font=self.second_timer_font, 
            padding=20, 
            anchor=tk.CENTER
        )
        self.style.configure('Black.Second.TLabel', foreground='black')
        self.style.configure('Green.Second.TLabel', foreground='#008F00')
        self.style.configure('Orange.Second.TLabel', foreground='#FF8C00')
        self.style.configure('Red.Second.TLabel', foreground='#D20000')

        # --- Estilos de otros widgets ---
        self.style.configure('TButton', padding=6)
        self.style.configure('Treeview', rowheight=28) # Más espacio en las filas
        self.style.configure('Treeview.Heading', font=(timer_font_family, 10, 'bold'))

        self.create_widgets()
        
        self.timer_label.bind("<Configure>", self.on_main_resize)
        
    def create_widgets(self):
        """Crea y posiciona los widgets usando .grid() para responsividad."""
        
        self.root.rowconfigure(0, weight=3) 
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=5)
        self.root.rowconfigure(3, weight=0) # Fila para añadir/quitar
        self.root.columnconfigure(0, weight=1)

        # --- Timer Label (Ahora ttk) ---
        self.timer_label = ttk.Label(
            self.root, 
            textvariable=self.time_str, 
            style='Black.Timer.TLabel', # Inicia con el estilo base
            anchor=tk.CENTER
        )
        self.timer_label.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # --- Controles (Ahora ttk.Frame) ---
        controls_frame = ttk.Frame(self.root, padding=(10, 0))
        controls_frame.grid(row=1, column=0, sticky="ew", pady=5, padx=10)

        time_mode_frame = ttk.Frame(controls_frame)
        ttk.Label(time_mode_frame, text="Tiempo Asignado:").pack(side=tk.LEFT, padx=(0, 5))
        self.assigned_time_entry = ttk.Entry(time_mode_frame, width=12, state="readonly") 
        self.assigned_time_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(time_mode_frame, text="Modo:").pack(side=tk.LEFT, padx=(15, 5))
        mode_combo = ttk.Combobox(
            time_mode_frame,
            textvariable=self.mode_var,
            values=["ascendente", "descendente"],
            width=12,
            state="readonly"
        )
        mode_combo.pack(side=tk.LEFT)
        time_mode_frame.pack(side=tk.TOP)

        button_frame = ttk.Frame(controls_frame)
        self.start_button = ttk.Button(button_frame, text="Empezar", width=10, command=self.start)
        self.start_button.pack(side=tk.LEFT, padx=10)
        self.stop_button = ttk.Button(button_frame, text="Detener/Resetear", width=15, command=self.stop_reset)
        self.stop_button.pack(side=tk.LEFT, padx=10)
        button_frame.pack(side=tk.TOP, pady=10)

        check_frame = ttk.Frame(controls_frame)
        self.color_check = ttk.Checkbutton(check_frame, text="Activar Colores", variable=self.color_var)
        self.color_check.pack(side=tk.LEFT, padx=10)
        self.window_check = ttk.Checkbutton(check_frame, text="Activar Segunda Ventana", variable=self.second_window_var, command=self.toggle_second_window)
        self.window_check.pack(side=tk.LEFT, padx=10)
        check_frame.pack(side=tk.TOP, pady=5)
        
        # --- Treeview (Ya era ttk, solo ajustamos el frame) ---
        tree_frame = ttk.Frame(self.root)
        tree_frame.grid(row=2, column=0, sticky="nsew", padx=15, pady=(5, 10))
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        columns = ('discurso', 'tiempo')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
        
        self.tree.heading('discurso', text='Discurso')
        self.tree.heading('tiempo', text='Tiempo (hh:mm:ss)') 
        self.tree.column('tiempo', width=120, anchor=tk.CENTER)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # --- Controles de Añadir/Quitar (Ahora ttk) ---
        add_frame = ttk.Frame(self.root, padding=10)
        add_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 10))
        add_frame.columnconfigure(1, weight=1) # Hacemos que la entrada de discurso crezca
        
        ttk.Label(add_frame, text="Discurso:").grid(row=0, column=0, padx=(0, 5))
        self.discurso_entry = ttk.Entry(add_frame)
        self.discurso_entry.grid(row=0, column=1, sticky="ew", padx=5)
        
        ttk.Label(add_frame, text="Tiempo (hh:mm:ss):").grid(row=0, column=2, padx=(10, 5)) 
        self.tiempo_entry = ttk.Entry(add_frame, width=10) 
        self.tiempo_entry.grid(row=0, column=3, padx=5)
        
        self.add_button = ttk.Button(add_frame, text="Añadir", command=self.add_discourse)
        self.add_button.grid(row=0, column=4, padx=5)
        
        self.remove_button = ttk.Button(add_frame, text="Quitar Selec.", command=self.remove_discourse)
        self.remove_button.grid(row=0, column=5, padx=5)
        
        self.tree.bind('<<TreeviewSelect>>', self.on_discourse_select)

        # --- Datos de ejemplo ---
        self.tree.insert('', tk.END, values=("Discurso de Apertura", "05:00"))
        self.tree.insert('', tk.END, values=("Anuncios", "10:00"))
        self.tree.insert('', tk.END, values=("Discurso Principal", "30:00"))
        self.tree.insert('', tk.END, values=("Discurso Largo", "01:15:00")) 
        
        try:
            first_item = self.tree.get_children()[0]
            self.tree.selection_set(first_item)
            self.tree.focus(first_item)
        except IndexError:
            pass # No hay items para seleccionar

    def on_main_resize(self, event):
        """Ajusta el tamaño de la fuente principal re-configurando el estilo."""
        new_size = max(10, event.height // 3)
        self.timer_font.configure(size=new_size)
        # Aplicamos la nueva fuente al estilo base
        self.style.configure('Timer.TLabel', font=self.timer_font)

    def on_second_resize(self, event):
        """Ajusta el tamaño de la fuente secundaria re-configurando el estilo."""
        if self.second_label:
            size_by_width = max(20, event.width // 7) 
            size_by_height = max(20, event.height // 2)
            new_size = min(size_by_width, size_by_height)
            
            self.second_timer_font.configure(size=new_size)
            # Aplicamos la nueva fuente al estilo base
            self.style.configure('Second.TLabel', font=self.second_timer_font)

    def add_discourse(self):
        """Añade un nuevo discurso a la lista."""
        discurso = self.discurso_entry.get()
        tiempo = self.tiempo_entry.get()
        
        # Validar formato mm:ss o hh:mm:ss
        if not re.match(r'^(\d{1,2}:\d{2}(:\d{2})?)$', tiempo):
             # Corregir formatos simples (ej. "5" -> "05:00")
            try:
                minutos = int(tiempo)
                tiempo = f"{minutos:02d}:00"
            except ValueError:
                messagebox.showerror(
                    "Error de Formato", 
                    "Formato de tiempo inválido. Use mm:ss o hh:mm:ss (o solo minutos)."
                )
                return

        if discurso:
            self.tree.insert('', tk.END, values=(discurso, tiempo))
            self.discurso_entry.delete(0, tk.END)
            self.tiempo_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Datos Faltantes", "Por favor, ingrese un nombre para el discurso.")


    def remove_discourse(self):
        """Quita el discurso seleccionado de la lista."""
        try:
            selected_item = self.tree.selection()[0]
            self.tree.delete(selected_item)
        except IndexError:
            messagebox.showinfo("Información", "No hay ningún discurso seleccionado")

    def on_discourse_select(self, event):
        """
        Se llama cuando se selecciona un item de la lista.
        Actualiza el campo 'Tiempo Asignado'.
        """
        try:
            selected_item = self.tree.selection()[0]
            values = self.tree.item(selected_item, 'values')
            time_str = values[1]
            
            # ttk.Entry en 'readonly' SÍ permite esta operación
            self.assigned_time_entry.config(state="normal")
            self.assigned_time_entry.delete(0, tk.END)
            self.assigned_time_entry.insert(0, time_str)
            self.assigned_time_entry.config(state="readonly")
            
            self.target_ms = self.parse_assigned_time() * 1000
            
            if not self.running:
                self.elapsed_ms = 0
                self.update_display()
                
        except IndexError:
            self.assigned_time_entry.config(state="normal")
            self.assigned_time_entry.delete(0, tk.END)
            self.assigned_time_entry.config(state="readonly")
            self.target_ms = 0

    def start(self):
        if not self.running:
            self.target_ms = self.parse_assigned_time() * 1000
            
            if self.mode_var.get() == "descendente" and self.target_ms == 0:
                messagebox.showwarning(
                    "Tiempo Requerido",
                    "No se puede iniciar en modo descendente sin un tiempo asignado."
                )
                return

            # --- CAMBIO DE PRECISIÓN ---
            # Guarda el tiempo actual del sistema como ancla
            self.anchor_time = time.monotonic() 
            # Guarda el tiempo que ya había transcurrido (0 si es nuevo, >0 si es 'Continuar')
            self.start_elapsed_ms = self.elapsed_ms
            # --- FIN DE CAMBIO ---

            self.running = True
            
            self.update_timer()
            
    def stop_reset(self):
        if self.running:
            # Modo Pausa (Detener)
            self.running = False
            # Al pausar, self.elapsed_ms retiene el último valor calculado,
            # lo cual es perfecto para cuando pulsemos 'Continuar'.
            self.start_button.config(text="Continuar") 
        else:
            # Modo Reset
            self.running = False
            self.elapsed_ms = 0
            
            # --- CAMBIO DE PRECISIÓN ---
            # Resetea también las variables de tiempo preciso
            self.start_elapsed_ms = 0
            self.anchor_time = 0.0
            # --- FIN DE CAMBIO ---
            
            self.start_button.config(text="Empezar") # Restaura el botón
            self.update_display()
            
            # Intenta avanzar al siguiente discurso
            try:
                selected_id = self.tree.selection()[0]
                next_id = self.tree.next(selected_id)
                if next_id:
                    self.tree.selection_set(next_id)
                    self.tree.focus(next_id)
                else:
                    # Si no hay siguiente, resetea el tiempo del actual
                    self.on_discourse_select(None)
            except IndexError:
                pass 

    def update_timer(self):
        if self.running:
            # --- CÁLCULO DE TIEMPO PRECISO ---
            # Calcula el tiempo (en ms) que ha pasado desde que se hizo clic en 'start'
            current_run_ms = (time.monotonic() - self.anchor_time) * 1000
            # El tiempo total es el tiempo de sesiones pasadas + el de esta sesión
            self.elapsed_ms = self.start_elapsed_ms + current_run_ms
            
            # --- Lógica de parada (la misma que tenías) ---
            if (self.mode_var.get() == "descendente" and 
                not self.color_var.get() and
                self.elapsed_ms >= self.target_ms):
                
                self.elapsed_ms = self.target_ms 
                self.running = False
                self.start_button.config(text="Empezar") # Restaura el botón

            self.update_display()
            
            if self.running:
                # --- CAMBIO SUTIL ---
                # Pedimos la actualización más rápido (50ms) para que sea más fluida.
                # La PRECISIÓN ya no depende de este número.
                self.root.after(50, self.update_timer)

    def update_display(self):
        """Formatea el tiempo basado en el modo (ascendente/descendente)."""
        
        mode = self.mode_var.get()
        current_ms = self.elapsed_ms
        target_ms = self.target_ms
        
        display_ms = 0
        is_negative = False

        if mode == "ascendente":
            display_ms = current_ms
        
        elif mode == "descendente":
            remaining_ms = target_ms - current_ms
            if remaining_ms < 0:
                display_ms = abs(remaining_ms)
                is_negative = True
            else:
                display_ms = remaining_ms

        display_ms_int = int(display_ms)
        
        total_seconds = display_ms_int // 1000
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        tenths = (display_ms_int % 1000) // 100
        
        prefix = "-" if is_negative else ""
        
        if hours > 0:
            formatted_time = f"{prefix}{hours:02d}:{minutes:02d}:{seconds:02d}.{tenths:d}"
        else:
            formatted_time = f"{prefix}{minutes:02d}:{seconds:02d}.{tenths:d}"
        
        self.time_str.set(formatted_time)
        
        self.update_colors()

    def update_colors(self):
        """Aplica colores basado en el TIEMPO TRANSCURRIDO."""
        
        if not self.color_var.get():
            self.set_timer_color_style("Black") # Estilo base
            return

        target_seconds = self.target_ms / 1000.0
        if target_seconds == 0:
            self.set_timer_color_style("Black")
            return

        # Tiempos de cambio de color
        # Lo he cambiado para que rojo sea al 100% y amarillo al 80%
        yellow_time = target_seconds * 0.80 
        current_seconds = self.elapsed_ms / 1000.0

        if current_seconds >= target_seconds:
            self.set_timer_color_style("Red")
        elif current_seconds >= yellow_time:
            self.set_timer_color_style("Orange") 
        else:
            self.set_timer_color_style("Green")

    def set_timer_color_style(self, color_prefix):
        """
        Cambia el *estilo* del label, no solo el 'fg'.
        color_prefix debe ser 'Black', 'Green', 'Orange', o 'Red'.
        """
        try:
            main_style = f"{color_prefix}.Timer.TLabel"
            self.timer_label.config(style=main_style)
            
            if self.second_label:
                second_style = f"{color_prefix}.Second.TLabel"
                self.second_label.config(style=second_style)
        except tk.TclError as e:
            print(f"Error al aplicar estilo: {e}")

    def parse_assigned_time(self):
        """Lee el campo 'Tiempo Asignado' y lo convierte a segundos."""
        try:
            time_str = self.assigned_time_entry.get()
            parts = time_str.split(":")
            
            if len(parts) == 3: # Formato hh:mm:ss
                hours = int(parts[0])
                minutes = int(parts[1])
                seconds = int(parts[2])
                return (hours * 3600) + (minutes * 60) + seconds
            elif len(parts) == 2: # Formato mm:ss
                minutes = int(parts[0])
                seconds = int(parts[1])
                return (minutes * 60) + seconds
            else:
                return 0
            
        except ValueError:
            return 0 

    def toggle_second_window(self):
        if self.second_window_var.get():
            if not self.second_window:
                self.second_window = tk.Toplevel(self.root)
                self.second_window.title("Timer (Discursante)")
                self.second_window.geometry("550x250")
                
                # --- Label de la segunda ventana (Ahora ttk) ---
                self.second_label = ttk.Label(
                    self.second_window,
                    textvariable=self.time_str,
                    style='Black.Second.TLabel', # Inicia con el estilo base
                    anchor=tk.CENTER
                    
                )
                self.second_label.pack(fill=tk.BOTH, expand=True)
                
                self.second_window.bind("<Configure>", self.on_second_resize)
                self.second_window.protocol("WM_DELETE_WINDOW", self.on_second_window_close)
        else:
            self.on_second_window_close()

    def on_second_window_close(self):
        if self.second_window:
            try:
                self.second_window.unbind("<Configure>")
            except tk.TclError:
                pass 
            self.second_window.destroy()
        self.second_window = None
        self.second_label = None
        self.second_window_var.set(False)

if __name__ == "__main__":
    main_window = tk.Tk()

    import sv_ttk
    sv_ttk.set_theme("light")

    app = CronometroAvanzado(main_window)
    main_window.mainloop()