import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from datetime import datetime
from docx import Document
from docx.shared import Pt, RGBColor
import re
from deep_translator import GoogleTranslator
import language_tool_python

translator = GoogleTranslator(source='auto', target='en')
tool = None

def init_language_tool():
    global tool
    if tool is None:
        try:
            tool = language_tool_python.LanguageTool('en-US')
        except:
            pass
    return tool

def translate_to_english(text):
    if not text or not text.strip():
        return text
    try:
        return translator.translate(text)
    except:
        return text

def correct_grammar(text):
    if not text or not text.strip():
        return text
    try:
        lt = init_language_tool()
        if lt:
            matches = lt.check(text)
            return language_tool_python.utils.correct(text, matches)
        return text
    except:
        return text

def translate_and_correct(text):
    if not text or not text.strip():
        return text
    return correct_grammar(translate_to_english(text))

def translate_equipment_info(text):
    if not text or not text.strip():
        return text
    
    translations = {
        'nombre del equipo': 'Equipment name', 'nombre': 'Equipment name',
        'modelo': 'Model', 'número de serie': 'Serial Number', 'serial': 'Serial Number',
        'versión hardware': 'Hardware Version', 'versión software': 'Software Version',
        'versión firmware': 'Firmware Version', 'código de país': 'Country Code',
        'product id': 'Product ID',
    }
    
    lines = text.split('\n')
    result = []
    
    for line in lines:
        line = line.strip()
        if not line:
            result.append('')
            continue
        
        if ':' in line:
            parts = line.split(':', 1)
            if len(parts) == 2:
                field = parts[0].strip().lower()
                value = parts[1].strip()
                
                if field in translations:
                    result.append(f"{translations[field]}: {value}")
                else:
                    try:
                        field_trans = GoogleTranslator(source='auto', target='en').translate(parts[0].strip())
                        result.append(f"{field_trans}: {value}")
                    except:
                        result.append(line)
            else:
                result.append(line)
        else:
            result.append(line)
    
    return '\n'.join(result)

class MaterialColors:
    # Colores estilo Windows 11
    PRIMARY = '#0078D4'  # Azul Windows 11
    PRIMARY_HOVER = '#106EBE'
    SUCCESS = '#107C10'  # Verde Windows 11
    SUCCESS_HOVER = '#0E6B0E'
    ERROR = '#D13438'
    BG_LIGHT = '#F3F3F3'  # Gris claro Win11
    BG_CARD = '#FFFFFF'
    TEXT_PRIMARY = '#1A1A1A'
    TEXT_SECONDARY = '#616161'
    BORDER_LIGHT = '#E0E0E0'
    SHADOW = '#D0D0D0'  # Sombra sutil (sin alpha channel)

class RoundedButton(tk.Canvas):
    """Botón redondeado estilo Windows 11"""
    def __init__(self, parent, text, command, bg_color, fg_color='white', 
                 hover_color=None, font=('Segoe UI', 11, 'bold'), 
                 width=120, height=40, corner_radius=6):
        super().__init__(parent, width=width, height=height, 
                        bg=parent['bg'], highlightthickness=0)
        
        self.command = command
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.hover_color = hover_color or bg_color
        self.font = font
        self.corner_radius = corner_radius
        self.width = width
        self.height = height
        self.text = text
        
        self.draw_button(self.bg_color)
        
        # Eventos
        self.bind('<Button-1>', self.on_click)
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        
    def draw_button(self, color):
        self.delete('all')
        # Rectángulo redondeado
        self.create_rounded_rect(2, 2, self.width-2, self.height-2, 
                                self.corner_radius, fill=color, outline='')
        # Texto
        self.create_text(self.width/2, self.height/2, text=self.text,
                        fill=self.fg_color, font=self.font)
    
    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1+radius, y1,
            x1+radius, y1,
            x2-radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1+radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def on_click(self, event):
        if self.command:
            self.command()
    
    def on_enter(self, event):
        self.draw_button(self.hover_color)
        self.configure(cursor='hand2')
    
    def on_leave(self, event):
        self.draw_button(self.bg_color)
        self.configure(cursor='')

class AutoNumberedText(scrolledtext.ScrolledText):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind('<Return>', self.auto_number)
        self.line_count = 0
    
    def auto_number(self, event):
        content = self.get('1.0', 'end-1c')
        lines = [l.strip() for l in content.split('\n') if l.strip()]
        self.line_count = len(lines)
        self.insert('insert', f'\n{self.line_count + 1}. ')
        return 'break'
    
    def reset_numbering(self):
        self.line_count = 0
    
    def get_numbered_text(self):
        content = self.get('1.0', 'end-1c')
        lines = content.split('\n')
        clean = []
        counter = 1
        for line in lines:
            clean_line = re.sub(r'^\d+\.\s*', '', line).strip()
            if clean_line:
                clean.append(f"{counter}. {clean_line}")
                counter += 1
        return '\n'.join(clean)

class RepairReportGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("ReportMaker v1.1")
        self.root.geometry("1450x850")
        self.root.configure(bg=MaterialColors.BG_LIGHT)
        self.root.minsize(1200, 700)
        
        # Configurar estilo Windows 11
        self.setup_modern_style()
        
        # Referencias a widgets
        self.summary_widgets = []
        self.procedure_widgets = []
        self.expected_widgets = []
        
        self.create_widgets()
        
    def setup_modern_style(self):
        """Configura estilos modernos Windows 11"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Estilo para Combobox
        style.configure('Modern.TCombobox',
                       fieldbackground='white',
                       background=MaterialColors.PRIMARY,
                       foreground=MaterialColors.TEXT_PRIMARY,
                       borderwidth=1,
                       relief='flat',
                       arrowsize=15)
        
        style.map('Modern.TCombobox',
                 fieldbackground=[('readonly', 'white')],
                 selectbackground=[('readonly', MaterialColors.PRIMARY)],
                 selectforeground=[('readonly', 'white')])
        
        # Estilo para Scrollbar
        style.configure('Modern.Vertical.TScrollbar',
                       background=MaterialColors.BG_LIGHT,
                       troughcolor='white',
                       borderwidth=0,
                       arrowsize=14)
        
        style.map('Modern.Vertical.TScrollbar',
                 background=[('active', MaterialColors.PRIMARY)])
    
    def create_rounded_frame(self, parent, **kwargs):
        """Crea un frame con bordes redondeados estilo Windows 11"""
        frame = tk.Frame(parent, **kwargs)
        frame.configure(highlightbackground=MaterialColors.BORDER_LIGHT,
                       highlightthickness=1,
                       relief=tk.FLAT)
        return frame
    
    def create_widgets(self):
        # Header moderno con gradiente simulado
        header = tk.Frame(self.root, bg=MaterialColors.PRIMARY, height=70)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)
        
        # Agregar sombra sutil
        shadow = tk.Frame(self.root, bg=MaterialColors.SHADOW, height=3)
        shadow.pack(fill=tk.X, side=tk.TOP)
        
        title_frame = tk.Frame(header, bg=MaterialColors.PRIMARY)
        title_frame.pack(pady=18)
        
        tk.Label(title_frame, text="🔧 ReportMaker", font=('Segoe UI', 20, 'bold'),
                bg=MaterialColors.PRIMARY, fg='white').pack(side=tk.LEFT)
        tk.Label(title_frame, text=" v1.1", font=('Segoe UI', 11),
                bg=MaterialColors.PRIMARY, fg='#CCCCCC').pack(side=tk.LEFT, padx=(5, 0))
        
        # Contenedor principal con padding
        main = tk.Frame(self.root, bg=MaterialColors.BG_LIGHT)
        main.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # COLUMNA IZQUIERDA
        left = tk.Frame(main, bg=MaterialColors.BG_LIGHT)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))
        
        # Canvas con scrollbar moderno
        canvas = tk.Canvas(left, bg=MaterialColors.BG_LIGHT, highlightthickness=0)
        scrollbar = ttk.Scrollbar(left, orient="vertical", command=canvas.yview, 
                                 style='Modern.Vertical.TScrollbar')
        self.form_frame = tk.Frame(canvas, bg=MaterialColors.BG_LIGHT)
        
        self.form_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.form_frame, anchor="nw", width=680)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        row_counter = 0
        
        # Tipo de Reparo con diseño moderno
        self.add_section("Tipo de Reparo", row_counter, icon="📋")
        row_counter += 1
        
        combo_frame = tk.Frame(self.form_frame, bg=MaterialColors.BG_LIGHT)
        combo_frame.grid(row=row_counter, column=0, sticky='w', padx=30, pady=(0, 25))
        
        self.report_type = ttk.Combobox(combo_frame, 
                                       values=["OPENED", "REOPENED", "VERIFIED"],
                                       state='readonly', 
                                       font=('Segoe UI', 11), 
                                       width=28,
                                       style='Modern.TCombobox')
        self.report_type.pack()
        self.report_type.current(0)
        self.report_type.bind('<<ComboboxSelected>>', self.on_type_change)
        row_counter += 1
        
        # Summary (solo OPENED)
        summary_card = self.add_section("Summary", row_counter, icon="📝")
        self.summary_widgets.append(summary_card)
        row_counter += 1
        
        summary_container = self.create_rounded_frame(self.form_frame, bg='white')
        summary_container.grid(row=row_counter, column=0, sticky='ew', padx=30, pady=(0, 25))
        self.summary = tk.Entry(summary_container, font=('Segoe UI', 11), bg='white', 
                               relief=tk.FLAT, borderwidth=0)
        self.summary.pack(fill=tk.X, padx=12, pady=10)
        self.summary_widgets.append(summary_container)
        row_counter += 1
        
        # Equipment Information
        self.add_section("Equipment Information", row_counter, icon="🖥️")
        row_counter += 1
        
        eq_frame = self.create_rounded_frame(self.form_frame, bg='white')
        eq_frame.grid(row=row_counter, column=0, sticky='ew', padx=30, pady=(0, 25))
        
        self.equipment = tk.Text(eq_frame, font=('Consolas', 10), bg='white', height=8,
                                relief=tk.FLAT, borderwidth=0, wrap=tk.WORD)
        eq_scroll = ttk.Scrollbar(eq_frame, orient="vertical", command=self.equipment.yview,
                                 style='Modern.Vertical.TScrollbar')
        self.equipment.configure(yscrollcommand=eq_scroll.set)
        
        self.equipment.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        eq_scroll.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 5), pady=10)
        row_counter += 1
        
        # Descripción
        self.add_section("Descripción", row_counter, icon="📄")
        row_counter += 1
        
        desc_frame = self.create_rounded_frame(self.form_frame, bg='white')
        desc_frame.grid(row=row_counter, column=0, sticky='ew', padx=30, pady=(0, 25))
        
        self.description = tk.Text(desc_frame, font=('Segoe UI', 10), bg='white', height=8,
                                  relief=tk.FLAT, borderwidth=0, wrap=tk.WORD)
        desc_scroll = ttk.Scrollbar(desc_frame, orient="vertical", command=self.description.yview,
                                   style='Modern.Vertical.TScrollbar')
        self.description.configure(yscrollcommand=desc_scroll.set)
        
        self.description.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        desc_scroll.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 5), pady=10)
        row_counter += 1
        
        # Procedimiento (OPENED y REOPENED)
        proc_card = self.add_section("Procedimiento", row_counter, icon="🔧")
        self.procedure_widgets.append(proc_card)
        row_counter += 1
        
        proc_frame = self.create_rounded_frame(self.form_frame, bg='white')
        proc_frame.grid(row=row_counter, column=0, sticky='ew', padx=30, pady=(0, 15))
        
        self.procedure = AutoNumberedText(proc_frame, font=('Segoe UI', 10), bg='white', height=6,
                                         relief=tk.FLAT, borderwidth=0, wrap=tk.WORD)
        self.procedure.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.procedure.insert('1.0', '1. ')
        self.procedure_widgets.append(proc_frame)
        row_counter += 1
        
        # Botón reiniciar con diseño moderno
        btn_reset_container = tk.Frame(self.form_frame, bg=MaterialColors.BG_LIGHT)
        btn_reset_container.grid(row=row_counter, column=0, sticky='w', padx=30, pady=(0, 25))
        
        proc_btn = RoundedButton(btn_reset_container, text="🔄 Reiniciar", 
                                command=self.reset_proc,
                                bg_color=MaterialColors.TEXT_SECONDARY,
                                hover_color='#525252',
                                width=120, height=36, corner_radius=6)
        proc_btn.pack()
        self.procedure_widgets.append(btn_reset_container)
        row_counter += 1
        
        # Resultado Esperado (solo OPENED)
        exp_card = self.add_section("Resultado Esperado", row_counter, icon="✅")
        self.expected_widgets.append(exp_card)
        row_counter += 1
        
        exp_frame = self.create_rounded_frame(self.form_frame, bg='white')
        exp_frame.grid(row=row_counter, column=0, sticky='ew', padx=30, pady=(0, 25))
        
        self.expected = tk.Text(exp_frame, font=('Segoe UI', 10), bg='white', height=4,
                               relief=tk.FLAT, borderwidth=0, wrap=tk.WORD)
        exp_scroll = ttk.Scrollbar(exp_frame, orient="vertical", command=self.expected.yview,
                                  style='Modern.Vertical.TScrollbar')
        self.expected.configure(yscrollcommand=exp_scroll.set)
        
        self.expected.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        exp_scroll.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 5), pady=10)
        self.expected_widgets.append(exp_frame)
        row_counter += 1
        
        # Adjuntos
        self.add_section("Attachments", row_counter, icon="📎")
        row_counter += 1
        
        att_container = self.create_rounded_frame(self.form_frame, bg='white')
        att_container.grid(row=row_counter, column=0, sticky='ew', padx=30, pady=(0, 25))
        self.attachments = tk.Entry(att_container, font=('Segoe UI', 11), bg='white', 
                                    relief=tk.FLAT, borderwidth=0)
        self.attachments.pack(fill=tk.X, padx=12, pady=10)
        row_counter += 1
        
        # Botones principales con diseño moderno
        btn_frame = tk.Frame(self.form_frame, bg=MaterialColors.BG_LIGHT)
        btn_frame.grid(row=row_counter, column=0, pady=35)
        
        btn_clear = RoundedButton(btn_frame, text="🗑️ Limpiar", 
                                 command=self.clear_form,
                                 bg_color=MaterialColors.TEXT_SECONDARY,
                                 hover_color='#525252',
                                 width=140, height=45)
        btn_clear.pack(side=tk.LEFT, padx=8)
        
        btn_generate = RoundedButton(btn_frame, text="✨ Generar", 
                                    command=self.generate,
                                    bg_color=MaterialColors.SUCCESS,
                                    hover_color=MaterialColors.SUCCESS_HOVER,
                                    font=('Segoe UI', 12, 'bold'),
                                    width=180, height=48)
        btn_generate.pack(side=tk.LEFT, padx=8)
        
        self.form_frame.columnconfigure(0, weight=1)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Scroll mejorado con detección de widgets
        def on_mouse_wheel(event):
            # Verificar si el cursor está sobre un widget de texto
            widget = event.widget
            
            # Si es un widget Text o ScrolledText, dejar que maneje su propio scroll
            if isinstance(widget, (tk.Text, scrolledtext.ScrolledText)):
                # Obtener posición actual del scroll
                try:
                    yview = widget.yview()
                    # Si está en el tope y scrollea hacia arriba, permitir scroll del canvas
                    if event.delta > 0 and yview[0] <= 0.0:
                        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
                        return "break"
                    # Si está en el fondo y scrollea hacia abajo, permitir scroll del canvas
                    elif event.delta < 0 and yview[1] >= 1.0:
                        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
                        return "break"
                    # En cualquier otro caso, dejar que el widget maneje el scroll
                    return
                except:
                    pass
            else:
                # Si no es un widget de texto, hacer scroll del canvas
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
                return "break"
        
        # Vincular scroll a todo el formulario
        def bind_mouse_wheel(widget):
            widget.bind("<MouseWheel>", on_mouse_wheel)
            for child in widget.winfo_children():
                bind_mouse_wheel(child)
        
        bind_mouse_wheel(self.form_frame)
        canvas.bind("<MouseWheel>", on_mouse_wheel)
        
        # COLUMNA DERECHA
        right = tk.Frame(main, bg=MaterialColors.BG_LIGHT)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(8, 0))
        
        # Preview con diseño moderno
        preview_card = self.create_rounded_frame(right, bg='white')
        preview_card.pack(fill=tk.BOTH, expand=True)
        
        preview_header = tk.Frame(preview_card, bg=MaterialColors.SUCCESS, height=55)
        preview_header.pack(fill=tk.X)
        preview_header.pack_propagate(False)
        
        tk.Label(preview_header, text="📄 Vista Previa", font=('Segoe UI', 15, 'bold'),
                bg=MaterialColors.SUCCESS, fg='white').pack(pady=12)
        
        preview_container = tk.Frame(preview_card, bg='white')
        preview_container.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        self.preview = scrolledtext.ScrolledText(preview_container, font=('Consolas', 10),
            bg='white', fg=MaterialColors.TEXT_PRIMARY, wrap=tk.WORD, 
            padx=18, pady=18, relief=tk.FLAT)
        self.preview.pack(fill=tk.BOTH, expand=True)
        self.preview.insert('1.0', "\n\n    📋 Vista Previa del Informe\n\n    "
                           "✏️ Completa el formulario y genera\n\n    "
                           "🌐 Se traducirá automáticamente al inglés\n    "
                           "✅ Se corregirán errores gramaticales\n\n ")
        
        # Mejorar scroll del preview
        def on_preview_scroll(event):
            # El ScrolledText maneja su propio scroll naturalmente
            return
        
        self.preview.bind("<MouseWheel>", on_preview_scroll)
        
        # Botones vista previa con diseño moderno
        btn_preview = tk.Frame(preview_card, bg='white')
        btn_preview.pack(fill=tk.X, padx=15, pady=15)
        
        btn_copy = RoundedButton(btn_preview, text="📋 Copiar", 
                                command=self.copy_preview,
                                bg_color=MaterialColors.PRIMARY,
                                hover_color=MaterialColors.PRIMARY_HOVER,
                                width=110, height=38)
        btn_copy.pack(side=tk.LEFT, padx=5)
        
        btn_export = RoundedButton(btn_preview, text="📄 Exportar", 
                                  command=self.export_word,
                                  bg_color=MaterialColors.SUCCESS,
                                  hover_color=MaterialColors.SUCCESS_HOVER,
                                  width=120, height=38)
        btn_export.pack(side=tk.LEFT, padx=5)
        
        btn_clear_prev = RoundedButton(btn_preview, text="🗑️ Limpiar", 
                                      command=self.clear_preview,
                                      bg_color=MaterialColors.TEXT_SECONDARY,
                                      hover_color='#525252',
                                      width=110, height=38)
        btn_clear_prev.pack(side=tk.RIGHT, padx=5)
        
        # Configurar navegación con Tab
        self.setup_tab_order()
        
        # Configurar atajos de teclado
        self.setup_keyboard_shortcuts()
        
        # Inicializar visibilidad
        self.on_type_change()
    
    def setup_tab_order(self):
        """Configura el orden de navegación con Tab"""
        widgets_order = [
            self.report_type,
            self.summary,
            self.equipment,
            self.description,
            self.procedure,
            self.expected,
            self.attachments
        ]
        
        for i, widget in enumerate(widgets_order):
            if i < len(widgets_order) - 1:
                widget.bind('<Tab>', lambda e, next_widget=widgets_order[i+1]: 
                           self.focus_next(next_widget))
    
    def focus_next(self, widget):
        """Mueve el foco al siguiente widget"""
        widget.focus_set()
        return 'break'
    
    def setup_keyboard_shortcuts(self):
        """Configura atajos de teclado modernos"""
        # Ctrl+Z para deshacer en campos de texto
        text_widgets = [self.equipment, self.description, self.procedure, self.expected]
        for widget in text_widgets:
            widget.bind('<Control-z>', lambda e, w=widget: w.edit_undo())
            widget.bind('<Control-y>', lambda e, w=widget: w.edit_redo())
        
        # Ctrl+S para generar (guardar)
        self.root.bind('<Control-s>', lambda e: self.generate())
        
        # Ctrl+N para limpiar (nuevo)
        self.root.bind('<Control-n>', lambda e: self.clear_form())
        
        # Ctrl+E para exportar
        self.root.bind('<Control-e>', lambda e: self.export_word())
        
        # Ctrl+C para copiar preview (solo cuando está enfocado)
        self.preview.bind('<Control-c>', lambda e: self.copy_preview())
    
    def add_section(self, title, row, icon=""):
        """Crea una sección con diseño moderno Windows 11"""
        card = tk.Frame(self.form_frame, bg=MaterialColors.BG_LIGHT, relief=tk.FLAT)
        card.grid(row=row, column=0, sticky='ew', padx=20, pady=(15, 8))
        
        label_text = f"{icon} {title}" if icon else title
        tk.Label(card, text=label_text, font=('Segoe UI', 11, 'bold'),
                bg=MaterialColors.BG_LIGHT, fg=MaterialColors.PRIMARY,
                anchor='w').pack(fill=tk.X, pady=(0, 0))
        
        return card
    
    def on_type_change(self, event=None):
        report_type = self.report_type.get()
        
        # Ocultar todo primero
        for widget in self.summary_widgets:
            widget.grid_remove()
        for widget in self.procedure_widgets:
            widget.grid_remove()
        for widget in self.expected_widgets:
            widget.grid_remove()
        
        # Mostrar según el tipo
        if report_type == "OPENED":
            for widget in self.summary_widgets:
                widget.grid()
            for widget in self.procedure_widgets:
                widget.grid()
            for widget in self.expected_widgets:
                widget.grid()
        
        elif report_type == "REOPENED":
            for widget in self.procedure_widgets:
                widget.grid()
        
        elif report_type == "VERIFIED":
            pass
    
    def reset_proc(self):
        self.procedure.delete('1.0', tk.END)
        self.procedure.reset_numbering()
        self.procedure.insert('1.0', '1. ')
    
    def clear_form(self):
        self.summary.delete(0, tk.END)
        self.equipment.delete('1.0', tk.END)
        self.description.delete('1.0', tk.END)
        self.procedure.delete('1.0', tk.END)
        self.procedure.reset_numbering()
        self.procedure.insert('1.0', '1. ')
        self.expected.delete('1.0', tk.END)
        self.attachments.delete(0, tk.END)
        self.report_type.current(0)
        self.on_type_change()
    
    def copy_preview(self):
        content = self.preview.get('1.0', 'end-1c')
        if not content.strip() or "Vista Previa" in content:
            messagebox.showwarning("⚠️ Advertencia", "Genera primero un informe")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        messagebox.showinfo("✅ Copiado", "Informe copiado al portapapeles")
    
    def clear_preview(self):
        self.preview.delete('1.0', tk.END)
        self.preview.insert('1.0', "\n\n    📋 Vista Previa del Informe\n\n    "
                           "✏️ Completa el formulario y genera\n\n    "
                           "🌐 Se traducirá automáticamente al inglés\n    "
                           "✅ Se corregirán errores gramaticales\n\n ")
    
    def export_word(self):
        content = self.preview.get('1.0', 'end-1c').strip()
        if not content or "Vista Previa" in content:
            messagebox.showwarning("⚠️ Advertencia", "Genera primero un informe")
            return
        
        try:
            doc = Document()
            for line in content.split('\n'):
                if line.strip():
                    if line.strip() in ['OPENED', 'REOPENED', 'VERIFIED']:
                        p = doc.add_paragraph()
                        run = p.add_run(line)
                        run.bold = True
                        run.font.size = Pt(14)
                        if 'REOPENED' in line:
                            run.font.color.rgb = RGBColor(255, 0, 0)
                        elif 'VERIFIED' in line:
                            run.font.color.rgb = RGBColor(0, 128, 0)
                    elif line.strip().startswith('[') and line.strip().endswith(']:'):
                        p = doc.add_paragraph()
                        p.add_run(line).bold = True
                    else:
                        doc.add_paragraph(line)
                else:
                    doc.add_paragraph()
            
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = filedialog.asksaveasfilename(
                defaultextension=".docx",
                filetypes=[("Word", "*.docx")],
                initialfile=f"Repair_{self.report_type.get()}_{ts}.docx"
            )
            if path:
                doc.save(path)
                messagebox.showinfo("✅ Exportado", f"Documento guardado en:\n{path}")
        except Exception as e:
            messagebox.showerror("❌ Error", str(e))
    
    def generate(self):
        rt = self.report_type.get()
        
        # Validaciones
        if rt == "OPENED":
            if not self.summary.get().strip():
                messagebox.showerror("❌ Error", "Summary obligatorio para OPENED")
                return
            proc = self.procedure.get_numbered_text()
            if not proc.strip() or proc.strip() == "1.":
                messagebox.showerror("❌ Error", "Procedimiento obligatorio para OPENED")
                return
            if not self.expected.get('1.0', tk.END).strip():
                messagebox.showerror("❌ Error", "Resultado Esperado obligatorio para OPENED")
                return
        
        if not self.equipment.get('1.0', tk.END).strip():
            messagebox.showerror("❌ Error", "Equipment Information requerido")
            return
        if not self.description.get('1.0', tk.END).strip():
            messagebox.showerror("❌ Error", "Descripción requerida")
            return
        
        try:
            self.preview.delete('1.0', tk.END)
            
            # VERIFIED tiene formato especial
            if rt == "VERIFIED":
                self.preview.insert(tk.END, "🌐 Traduciendo...\n")
                self.preview.see(tk.END)
                self.root.update()
                
                eq = translate_equipment_info(self.equipment.get('1.0', tk.END).strip())
                self.preview.delete("end-2l", "end-1l")
                self.preview.insert(tk.END, "[Equipment information]:\n")
                self.preview.insert(tk.END, f"{eq}\n\n")
                self.root.update()
                
                self.preview.insert(tk.END, "The problem is VERIFIED in this version\n\n")
                self.root.update()
                
                self.preview.insert(tk.END, "🌐 Traduciendo...\n")
                self.preview.see(tk.END)
                self.root.update()
                
                desc = translate_and_correct(self.description.get('1.0', tk.END).strip())
                self.preview.delete("end-2l", "end-1l")
                self.preview.insert(tk.END, f"{desc}\n\n")
                self.root.update()
                
                att = self.attachments.get().strip()
                if att:
                    self.preview.insert(tk.END, "[Attachments]:\n")
                    self.preview.insert(tk.END, f"{att}\n")
                
                messagebox.showinfo("✅ Listo", "Informe generado correctamente")
                return
            
            # OPENED y REOPENED
            self.preview.insert(tk.END, f"{rt}\n")
            if rt == "REOPENED":
                self.preview.insert(tk.END, "The problem continues, REOPENED in this version.\n\n")
            else:
                self.preview.insert(tk.END, "\n")
            self.root.update()
            
            # Summary (solo OPENED)
            if rt == "OPENED":
                self.preview.insert(tk.END, "🌐 Traduciendo...\n")
                self.preview.see(tk.END)
                self.root.update()
                
                summ = translate_and_correct(self.summary.get())
                self.preview.delete("end-2l", "end-1l")
                self.preview.insert(tk.END, f"Summary: {summ}\n\n")
                self.root.update()
            
            # Equipment
            self.preview.insert(tk.END, "🌐 Traduciendo...\n")
            self.preview.see(tk.END)
            self.root.update()
            
            eq = translate_equipment_info(self.equipment.get('1.0', tk.END).strip())
            self.preview.delete("end-2l", "end-1l")
            self.preview.insert(tk.END, "[Equipment information]:\n\n")
            self.preview.insert(tk.END, f"{eq}\n\n")
            self.root.update()
            
            # Fault
            self.preview.insert(tk.END, "🌐 Traduciendo...\n")
            self.preview.see(tk.END)
            self.root.update()
            
            fault = translate_and_correct(self.description.get('1.0', tk.END).strip())
            self.preview.delete("end-2l", "end-1l")
            self.preview.insert(tk.END, "[Fault]:\n")
            self.preview.insert(tk.END, f"{fault}\n\n")
            self.root.update()
            
            # Procedure
            proc = self.procedure.get_numbered_text()
            if proc.strip() and proc.strip() != "1.":
                self.preview.insert(tk.END, "🌐 Traduciendo...\n")
                self.preview.see(tk.END)
                self.root.update()
                
                proc_t = translate_and_correct(proc)
                self.preview.delete("end-2l", "end-1l")
                self.preview.insert(tk.END, "[Procedure]:\n")
                self.preview.insert(tk.END, f"{proc_t}\n\n")
                self.root.update()
            
            # Expected (solo OPENED)
            if rt == "OPENED":
                exp = self.expected.get('1.0', tk.END).strip()
                if exp:
                    self.preview.insert(tk.END, "🌐 Traduciendo...\n")
                    self.preview.see(tk.END)
                    self.root.update()
                    
                    exp_t = translate_and_correct(exp)
                    self.preview.delete("end-2l", "end-1l")
                    self.preview.insert(tk.END, "[Expected]:\n")
                    self.preview.insert(tk.END, f"{exp_t}\n\n")
                    self.root.update()
            
            # Attachments
            att = self.attachments.get().strip()
            if att:
                self.preview.insert(tk.END, "[Attachments]:\n")
                self.preview.insert(tk.END, f"{att}\n")
            
            messagebox.showinfo("✅ Listo", "Informe generado correctamente")
        
        except Exception as e:
            messagebox.showerror("❌ Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = RepairReportGenerator(root)
    root.mainloop()