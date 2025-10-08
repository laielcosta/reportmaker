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
        text = text.strip()
        
        # Límite seguro para GoogleTranslator (caracteres por chunk)
        MAX_CHUNK_SIZE = 400
        
        # Si el texto es corto, traducir directamente
        if len(text) <= MAX_CHUNK_SIZE:
            return translator.translate(text)
        
        # Para textos largos, dividir inteligentemente
        translated_parts = []
        
        # Primero intentar dividir por párrafos (saltos de línea)
        paragraphs = text.split('\n')
        
        for paragraph in paragraphs:
            if not paragraph.strip():
                translated_parts.append('')
                continue
            
            # Si el párrafo es pequeño, traducir directamente
            if len(paragraph) <= MAX_CHUNK_SIZE:
                try:
                    translated = translator.translate(paragraph.strip())
                    translated_parts.append(translated)
                except Exception as e:
                    print(f"Error traduciendo párrafo: {e}")
                    # Si falla, dividir por oraciones
                    sentences = paragraph.replace('. ', '.|').replace('? ', '?|').replace('! ', '!|').split('|')
                    translated_sentences = []
                    for sentence in sentences:
                        if sentence.strip():
                            try:
                                translated_sentences.append(translator.translate(sentence.strip()))
                            except:
                                translated_sentences.append(sentence.strip())
                    translated_parts.append(' '.join(translated_sentences))
            else:
                # Párrafo muy largo: dividir en chunks por oraciones
                sentences = paragraph.replace('. ', '.|').replace('? ', '?|').replace('! ', '!|').split('|')
                current_chunk = ""
                translated_chunks = []
                
                for sentence in sentences:
                    sentence = sentence.strip()
                    if not sentence:
                        continue
                    
                    # Si agregar esta oración excede el límite, traducir el chunk actual
                    if len(current_chunk) + len(sentence) + 1 > MAX_CHUNK_SIZE:
                        if current_chunk:
                            try:
                                translated_chunks.append(translator.translate(current_chunk))
                            except Exception as e:
                                print(f"Error traduciendo chunk: {e}")
                                translated_chunks.append(current_chunk)
                            current_chunk = sentence
                        else:
                            # Oración individual muy larga, forzar traducción
                            try:
                                translated_chunks.append(translator.translate(sentence))
                            except:
                                translated_chunks.append(sentence)
                    else:
                        current_chunk += (" " if current_chunk else "") + sentence
                
                # Traducir el último chunk
                if current_chunk:
                    try:
                        translated_chunks.append(translator.translate(current_chunk))
                    except Exception as e:
                        print(f"Error traduciendo último chunk: {e}")
                        translated_chunks.append(current_chunk)
                
                translated_parts.append(' '.join(translated_chunks))
        
        return '\n'.join(translated_parts)
    except Exception as e:
        print(f"Error general en traducción: {e}")
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
        'nombre del equipo': 'Equipment', 'nombre': 'Equipment',
        'modelo': 'Model', 'número de serie': 'Serial Number', 'serial': 'Serial Number',
        'versión hardware': 'Hardware Version', 'versión software': 'Software Version',
        'versión firmware': 'Firmware Version', 'código de país': 'Country Code',
        'product id': 'Product ID', 'estado': 'State', 'versión': 'Version',
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
                    field_translated = translations[field]
                else:
                    try:
                        field_translated = GoogleTranslator(source='auto', target='en').translate(parts[0].strip())
                    except:
                        field_translated = parts[0].strip()
                
                result.append(f"{field_translated}: {value}")
            else:
                result.append(line)
        else:
            try:
                line_translated = GoogleTranslator(source='auto', target='en').translate(line)
                result.append(line_translated)
            except:
                result.append(line)
    
    return '\n'.join(result)

class MaterialColors:
    PRIMARY = '#0078D4'
    PRIMARY_HOVER = '#005A9E'
    PRIMARY_LIGHT = '#4A9EDE'
    PRIMARY_DARK = '#004578'
    
    SUCCESS = '#107C10'
    SUCCESS_HOVER = '#0E6B0E'
    
    BG_LIGHT = '#F5F5F5'
    BG_CARD = '#FFFFFF'
    TEXT_PRIMARY = '#1A1A1A'
    TEXT_SECONDARY = '#707070'
    BORDER_LIGHT = '#E0E0E0'
    SHADOW = '#CCCCCC'
    
    SCROLLBAR_BG = '#F0F0F0'
    SCROLLBAR_ACTIVE = "#868686"

class ModernScrollbar(tk.Canvas):
    def __init__(self, parent, orient='vertical', command=None, **kwargs):
        width = 14 if orient == 'vertical' else 200
        height = 200 if orient == 'vertical' else 14
        
        super().__init__(parent, width=width, height=height,
                        bg=MaterialColors.SCROLLBAR_BG, highlightthickness=0, **kwargs)
        
        self.orient = orient
        self.command = command
        self.pressed = False
        self.thumb_pos = 0
        self.thumb_size = 0.3
        self.hover = False
        
        self.bind('<Button-1>', self.on_press)
        self.bind('<B1-Motion>', self.on_drag)
        self.bind('<ButtonRelease-1>', self.on_release)
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        self.bind('<Configure>', self.on_configure)
        
        self.draw_thumb()
    
    def on_configure(self, event):
        self.draw_thumb()
    
    def draw_thumb(self):
        self.delete('all')
        
        if self.thumb_size <= 0 or self.thumb_size >= 1:
            return
        
        color = MaterialColors.SCROLLBAR_ACTIVE if (self.pressed or self.hover) else MaterialColors.TEXT_SECONDARY
        
        if self.orient == 'vertical':
            w = int(self['width'])
            h = self.winfo_height() if self.winfo_height() > 1 else 200
            
            thumb_height = max(30, int(h * self.thumb_size))
            thumb_y = int((h - thumb_height) * self.thumb_pos / (1 - self.thumb_size)) if self.thumb_size < 1 else 0
            
            x1, y1 = 3, thumb_y
            x2, y2 = w - 3, thumb_y + thumb_height
            
            self.create_rounded_rect(x1, y1, x2, y2, 4, fill=color, outline='')
        else:
            w = self.winfo_width() if self.winfo_width() > 1 else 200
            h = int(self['height'])
            
            thumb_width = max(30, int(w * self.thumb_size))
            thumb_x = int((w - thumb_width) * self.thumb_pos / (1 - self.thumb_size)) if self.thumb_size < 1 else 0
            
            x1, y1 = thumb_x, 3
            x2, y2 = thumb_x + thumb_width, h - 3
            
            self.create_rounded_rect(x1, y1, x2, y2, 4, fill=color, outline='')
    
    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1+radius, y1, x2-radius, y1, x2, y1, x2, y1+radius,
            x2, y2-radius, x2, y2, x2-radius, y2, x1+radius, y2,
            x1, y2, x1, y2-radius, x1, y1+radius, x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def set(self, first, last):
        first = float(first)
        last = float(last)
        
        self.thumb_pos = first
        self.thumb_size = last - first
        
        self.draw_thumb()
    
    def on_press(self, event):
        self.pressed = True
        
        if self.orient == 'vertical':
            h = self.winfo_height()
            thumb_height = max(30, int(h * self.thumb_size))
            thumb_y = int((h - thumb_height) * self.thumb_pos / (1 - self.thumb_size)) if self.thumb_size < 1 else 0
            
            if thumb_y <= event.y <= thumb_y + thumb_height:
                self.drag_start_y = event.y - thumb_y
            else:
                ratio = event.y / h
                if self.command:
                    self.command('moveto', ratio)
                self.drag_start_y = thumb_height / 2
        else:
            w = self.winfo_width()
            thumb_width = max(30, int(w * self.thumb_size))
            thumb_x = int((w - thumb_width) * self.thumb_pos / (1 - self.thumb_size)) if self.thumb_size < 1 else 0
            
            if thumb_x <= event.x <= thumb_x + thumb_width:
                self.drag_start_x = event.x - thumb_x
            else:
                ratio = event.x / w
                if self.command:
                    self.command('moveto', ratio)
                self.drag_start_x = thumb_width / 2
        
        self.draw_thumb()
    
    def on_drag(self, event):
        if not self.command:
            return
        
        if self.orient == 'vertical':
            h = self.winfo_height()
            thumb_height = max(30, int(h * self.thumb_size))
            max_y = h - thumb_height
            
            if max_y > 0:
                new_y = event.y - self.drag_start_y
                ratio = new_y / max_y
                ratio = max(0, min(ratio, 1))
                self.command('moveto', ratio * (1 - self.thumb_size))
        else:
            w = self.winfo_width()
            thumb_width = max(30, int(w * self.thumb_size))
            max_x = w - thumb_width
            
            if max_x > 0:
                new_x = event.x - self.drag_start_x
                ratio = new_x / max_x
                ratio = max(0, min(ratio, 1))
                self.command('moveto', ratio * (1 - self.thumb_size))
    
    def on_release(self, event):
        self.pressed = False
        self.draw_thumb()
    
    def on_enter(self, event):
        self.hover = True
        self.draw_thumb()
    
    def on_leave(self, event):
        self.hover = False
        if not self.pressed:
            self.draw_thumb()

class RoundedButton(tk.Canvas):
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
        
        self.bind('<Button-1>', self.on_click)
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        
    def draw_button(self, color):
        self.delete('all')
        self.create_rounded_rect(2, 2, self.width-2, self.height-2, 
                                self.corner_radius, fill=color, outline='')
        self.create_text(self.width/2, self.height/2, text=self.text,
                        fill=self.fg_color, font=self.font)
    
    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1+radius, y1, x2-radius, y1, x2, y1, x2, y1+radius,
            x2, y2-radius, x2, y2, x2-radius, y2, x1+radius, y2,
            x1, y2, x1, y2-radius, x1, y1+radius, x1, y1
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

class AutoNumberedText(tk.Text):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind('<Return>', self.auto_number)
        self.line_count = 0
        self.configure(undo=True, maxundo=-1)
    
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
        self.root.title("ReportMaker v1.2.1")
        self.root.geometry("1450x850")
        self.root.configure(bg=MaterialColors.BG_LIGHT)
        self.root.minsize(1200, 700)
        
        self.setup_modern_style()
        
        self.summary_widgets = []
        self.procedure_widgets = []
        self.expected_widgets = []
        
        self.create_widgets()
        
    def setup_modern_style(self):
        style = ttk.Style()
        style.theme_use('clam')
        
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
    
    def create_rounded_frame(self, parent, **kwargs):
        frame = tk.Frame(parent, **kwargs)
        frame.configure(highlightbackground=MaterialColors.BORDER_LIGHT,
                       highlightthickness=1,
                       relief=tk.FLAT)
        return frame
    
    def create_widgets(self):
        header = tk.Frame(self.root, bg=MaterialColors.PRIMARY, height=70)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)
        
        shadow = tk.Frame(self.root, bg=MaterialColors.SHADOW, height=2)
        shadow.pack(fill=tk.X, side=tk.TOP)
        
        title_frame = tk.Frame(header, bg=MaterialColors.PRIMARY)
        title_frame.pack(pady=18)
        
        tk.Label(title_frame, text="ReportMaker", font=('Segoe UI', 20, 'bold'),
                bg=MaterialColors.PRIMARY, fg='white').pack(side=tk.LEFT)
        tk.Label(title_frame, text=" v1.2.1", font=('Segoe UI', 11),
                bg=MaterialColors.PRIMARY, fg='#CCCCCC').pack(side=tk.LEFT, padx=(5, 0))
        
        main_paned = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, 
                                     bg=MaterialColors.BG_LIGHT, 
                                     sashwidth=8, sashrelief=tk.FLAT,
                                     bd=0)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        left_container = tk.Frame(main_paned, bg=MaterialColors.BG_LIGHT)
        
        canvas = tk.Canvas(left_container, bg=MaterialColors.BG_LIGHT, highlightthickness=0)
        scrollbar = ModernScrollbar(left_container, orient="vertical", command=canvas.yview)
        self.form_frame = tk.Frame(canvas, bg=MaterialColors.BG_LIGHT)
        
        self.form_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        canvas.bind('<Configure>', on_canvas_configure)
        canvas_window = canvas.create_window((0, 0), window=self.form_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        row_counter = 0
        
        self.add_section("Tipo de Reparo", row_counter, icon="")
        row_counter += 1
        
        combo_frame = tk.Frame(self.form_frame, bg=MaterialColors.BG_LIGHT)
        combo_frame.grid(row=row_counter, column=0, sticky='ew', padx=30, pady=(0, 25))
        
        self.report_type = ttk.Combobox(combo_frame, 
                                       values=["OPENED", "REOPENED", "VERIFIED"],
                                       state='readonly', 
                                       font=('Segoe UI', 11), 
                                       width=28,
                                       style='Modern.TCombobox')
        self.report_type.pack(fill=tk.X)
        self.report_type.current(0)
        self.report_type.bind('<<ComboboxSelected>>', self.on_type_change)
        row_counter += 1
        
        summary_card = self.add_section("Summary", row_counter, icon="")
        self.summary_widgets.append(summary_card)
        row_counter += 1
        
        summary_container = self.create_rounded_frame(self.form_frame, bg='white')
        summary_container.grid(row=row_counter, column=0, sticky='ew', padx=30, pady=(0, 25))
        self.summary = tk.Entry(summary_container, font=('Segoe UI', 11), bg='white', 
                               relief=tk.FLAT, borderwidth=0)
        self.summary.pack(fill=tk.X, padx=12, pady=10)
        self.summary_widgets.append(summary_container)
        row_counter += 1
        
        self.add_section("Equipment Information", row_counter, icon="")
        row_counter += 1
        
        eq_frame = self.create_rounded_frame(self.form_frame, bg='white')
        eq_frame.grid(row=row_counter, column=0, sticky='ew', padx=30, pady=(0, 25))
        
        eq_text_frame = tk.Frame(eq_frame, bg='white')
        eq_text_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        self.equipment = tk.Text(eq_text_frame, font=('Segoe UI', 10), bg='white', height=8,
                                relief=tk.FLAT, borderwidth=0, wrap=tk.WORD, undo=True, maxundo=-1)
        eq_scroll = ModernScrollbar(eq_text_frame, orient="vertical", command=self.equipment.yview)
        self.equipment.configure(yscrollcommand=eq_scroll.set)
        
        self.equipment.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        eq_scroll.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 5), pady=10)
        row_counter += 1
        
        self.add_section("Descripcion", row_counter, icon="")
        row_counter += 1
        
        desc_frame = self.create_rounded_frame(self.form_frame, bg='white')
        desc_frame.grid(row=row_counter, column=0, sticky='ew', padx=30, pady=(0, 25))
        
        desc_text_frame = tk.Frame(desc_frame, bg='white')
        desc_text_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        self.description = tk.Text(desc_text_frame, font=('Segoe UI', 10), bg='white', height=8,
                                  relief=tk.FLAT, borderwidth=0, wrap=tk.WORD, undo=True, maxundo=-1)
        desc_scroll = ModernScrollbar(desc_text_frame, orient="vertical", command=self.description.yview)
        self.description.configure(yscrollcommand=desc_scroll.set)
        
        self.description.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        desc_scroll.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 5), pady=10)
        row_counter += 1
        
        proc_card = self.add_section("Procedimiento", row_counter, icon="")
        self.procedure_widgets.append(proc_card)
        row_counter += 1
        
        proc_frame = self.create_rounded_frame(self.form_frame, bg='white')
        proc_frame.grid(row=row_counter, column=0, sticky='ew', padx=30, pady=(0, 15))
        
        proc_text_frame = tk.Frame(proc_frame, bg='white')
        proc_text_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        self.procedure = AutoNumberedText(proc_text_frame, font=('Segoe UI', 10), bg='white', height=6,
                                         relief=tk.FLAT, borderwidth=0, wrap=tk.WORD)
        proc_scroll = ModernScrollbar(proc_text_frame, orient="vertical", command=self.procedure.yview)
        self.procedure.configure(yscrollcommand=proc_scroll.set)
        
        self.procedure.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        proc_scroll.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 5), pady=10)
        
        self.procedure.insert('1.0', '1. ')
        self.procedure_widgets.append(proc_frame)
        row_counter += 1
        
        btn_reset_container = tk.Frame(self.form_frame, bg=MaterialColors.BG_LIGHT)
        btn_reset_container.grid(row=row_counter, column=0, sticky='w', padx=30, pady=(0, 25))
        
        proc_btn = RoundedButton(btn_reset_container, text="Reiniciar", 
                                command=self.reset_proc,
                                bg_color=MaterialColors.TEXT_SECONDARY,
                                hover_color='#525252',
                                width=120, height=36, corner_radius=6)
        proc_btn.pack()
        self.procedure_widgets.append(btn_reset_container)
        row_counter += 1
        
        exp_card = self.add_section("Resultado Esperado", row_counter, icon="")
        self.expected_widgets.append(exp_card)
        row_counter += 1
        
        exp_frame = self.create_rounded_frame(self.form_frame, bg='white')
        exp_frame.grid(row=row_counter, column=0, sticky='ew', padx=30, pady=(0, 25))
        
        exp_text_frame = tk.Frame(exp_frame, bg='white')
        exp_text_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        self.expected = tk.Text(exp_text_frame, font=('Segoe UI', 10), bg='white', height=4,
                               relief=tk.FLAT, borderwidth=0, wrap=tk.WORD, undo=True, maxundo=-1)
        exp_scroll = ModernScrollbar(exp_text_frame, orient="vertical", command=self.expected.yview)
        self.expected.configure(yscrollcommand=exp_scroll.set)
        
        self.expected.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        exp_scroll.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 5), pady=10)
        self.expected_widgets.append(exp_frame)
        row_counter += 1
        
        self.add_section("Attachments", row_counter, icon="")
        row_counter += 1
        
        att_container = self.create_rounded_frame(self.form_frame, bg='white')
        att_container.grid(row=row_counter, column=0, sticky='ew', padx=30, pady=(0, 25))
        self.attachments = tk.Entry(att_container, font=('Segoe UI', 11), bg='white', 
                                    relief=tk.FLAT, borderwidth=0)
        self.attachments.pack(fill=tk.X, padx=12, pady=10)
        row_counter += 1
        
        btn_frame = tk.Frame(self.form_frame, bg=MaterialColors.BG_LIGHT)
        btn_frame.grid(row=row_counter, column=0, pady=35)
        
        btn_clear = RoundedButton(btn_frame, text="Limpiar", 
                                 command=self.clear_form,
                                 bg_color=MaterialColors.TEXT_SECONDARY,
                                 hover_color='#525252',
                                 width=140, height=45)
        btn_clear.pack(side=tk.LEFT, padx=8)
        
        btn_generate = RoundedButton(btn_frame, text="Generar", 
                                    command=self.generate,
                                    bg_color=MaterialColors.SUCCESS,
                                    hover_color=MaterialColors.SUCCESS_HOVER,
                                    font=('Segoe UI', 12, 'bold'),
                                    width=180, height=48)
        btn_generate.pack(side=tk.LEFT, padx=8)
        
        self.form_frame.columnconfigure(0, weight=1)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        def smart_scroll(event):
            widget = event.widget
            
            if isinstance(widget, tk.Text):
                scroll_position = widget.yview()
                delta = int(-1 * (event.delta / 120))
                
                if delta < 0:
                    if scroll_position[0] <= 0.0:
                        canvas.yview_scroll(delta, "units")
                        return "break"
                    else:
                        widget.yview_scroll(delta, "units")
                        return "break"
                else:
                    if scroll_position[1] >= 1.0:
                        canvas.yview_scroll(delta, "units")
                        return "break"
                    else:
                        widget.yview_scroll(delta, "units")
                        return "break"
            else:
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
                return "break"
        
        def bind_smart_scroll_recursive(widget):
            widget.bind("<MouseWheel>", smart_scroll, add="+")
            for child in widget.winfo_children():
                bind_smart_scroll_recursive(child)
        
        bind_smart_scroll_recursive(self.form_frame)
        canvas.bind("<MouseWheel>", smart_scroll, add="+")
        
        right_container = tk.Frame(main_paned, bg=MaterialColors.BG_LIGHT)
        
        preview_card = self.create_rounded_frame(right_container, bg='white')
        preview_card.pack(fill=tk.BOTH, expand=True)
        
        preview_header = tk.Frame(preview_card, bg=MaterialColors.SUCCESS, height=55)
        preview_header.pack(fill=tk.X)
        preview_header.pack_propagate(False)
        
        tk.Label(preview_header, text="Vista Previa", font=('Segoe UI', 15, 'bold'),
                bg=MaterialColors.SUCCESS, fg='white').pack(pady=12)
        
        preview_container = tk.Frame(preview_card, bg='white')
        preview_container.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        preview_text_frame = tk.Frame(preview_container, bg='white')
        preview_text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.preview = tk.Text(preview_text_frame, font=('Consolas', 10),
            bg='white', fg=MaterialColors.TEXT_PRIMARY, wrap=tk.WORD, 
            padx=18, pady=18, relief=tk.FLAT)
        preview_scroll = ModernScrollbar(preview_text_frame, orient="vertical", command=self.preview.yview)
        self.preview.configure(yscrollcommand=preview_scroll.set)
        
        self.preview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        preview_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.preview.insert('1.0', "\n\n    Vista Previa del Informe\n\n    "
                           "Completa el formulario y genera\n\n    "
                           "Se traducirá automáticamente al inglés\n    "
                           "Se corregirán errores gramaticales\n\n ")
        
        btn_preview = tk.Frame(preview_card, bg='white')
        btn_preview.pack(fill=tk.X, padx=15, pady=15)
        
        left_btns = tk.Frame(btn_preview, bg='white')
        left_btns.pack(side=tk.LEFT)
        
        btn_copy = RoundedButton(left_btns, text="Copiar", 
                                command=self.copy_preview,
                                bg_color=MaterialColors.PRIMARY,
                                hover_color=MaterialColors.PRIMARY_HOVER,
                                width=110, height=38)
        btn_copy.pack(side=tk.LEFT, padx=(0, 5))
        
        btn_export = RoundedButton(left_btns, text="Exportar", 
                                  command=self.export_word,
                                  bg_color=MaterialColors.SUCCESS,
                                  hover_color=MaterialColors.SUCCESS_HOVER,
                                  width=120, height=38)
        btn_export.pack(side=tk.LEFT, padx=(5, 0))
        
        right_btns = tk.Frame(btn_preview, bg='white')
        right_btns.pack(side=tk.RIGHT)
        
        btn_clear_prev = RoundedButton(right_btns, text="Limpiar", 
                                      command=self.clear_preview,
                                      bg_color=MaterialColors.TEXT_SECONDARY,
                                      hover_color='#525252',
                                      width=110, height=38)
        btn_clear_prev.pack()
        
        main_paned.add(left_container, minsize=600)
        main_paned.add(right_container, minsize=400)
        
        self.setup_keyboard_shortcuts()
        self.setup_tab_order()
        self.on_type_change()
    
    def setup_tab_order(self):
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
                next_widget = widgets_order[i+1]
                
                if isinstance(widget, (ttk.Combobox, tk.Entry)):
                    widget.bind('<Tab>', lambda e, nw=next_widget: self.focus_next(nw, e))
                    widget.bind('<Shift-Tab>', lambda e, pw=widgets_order[i-1] if i > 0 else None: 
                               self.focus_previous(pw, e))
                elif isinstance(widget, tk.Text):
                    widget.bind('<Tab>', lambda e, nw=next_widget: self.focus_next(nw, e))
                    widget.bind('<Shift-Tab>', lambda e, pw=widgets_order[i-1] if i > 0 else None: 
                               self.focus_previous(pw, e))
        
        last_widget = widgets_order[-1]
        first_widget = widgets_order[0]
        if isinstance(last_widget, (ttk.Combobox, tk.Entry)):
            last_widget.bind('<Tab>', lambda e, fw=first_widget: self.focus_next(fw, e))
        elif isinstance(last_widget, tk.Text):
            last_widget.bind('<Tab>', lambda e, fw=first_widget: self.focus_next(fw, e))
    
    def focus_next(self, widget, event):
        widget.focus_set()
        return 'break'
    
    def focus_previous(self, widget, event):
        if widget:
            widget.focus_set()
        return 'break'
    
    def setup_keyboard_shortcuts(self):
        self.root.bind('<Control-s>', lambda e: (self.generate(), 'break'))
        self.root.bind('<Control-n>', lambda e: (self.clear_form(), 'break'))
        self.root.bind('<Control-e>', lambda e: (self.export_word(), 'break'))
        self.root.bind('<Control-q>', lambda e: self.root.quit())
        
        def clear_current_field(event):
            widget = self.root.focus_get()
            if isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)
            elif isinstance(widget, tk.Text):
                widget.delete('1.0', tk.END)
                if widget == self.procedure:
                    self.procedure.reset_numbering()
                    self.procedure.insert('1.0', '1. ')
            return 'break'
        
        self.root.bind('<Escape>', clear_current_field)
    
    def add_section(self, title, row, icon=""):
        card = tk.Frame(self.form_frame, bg=MaterialColors.BG_LIGHT, relief=tk.FLAT)
        card.grid(row=row, column=0, sticky='ew', padx=20, pady=(15, 8))
        
        label_text = f"{icon} {title}" if icon else title
        tk.Label(card, text=label_text, font=('Segoe UI', 11, 'bold'),
                bg=MaterialColors.BG_LIGHT, fg=MaterialColors.PRIMARY,
                anchor='w').pack(fill=tk.X, pady=(0, 0))
        
        return card
    
    def on_type_change(self, event=None):
        report_type = self.report_type.get()
        
        for widget in self.summary_widgets:
            widget.grid_remove()
        for widget in self.procedure_widgets:
            widget.grid_remove()
        for widget in self.expected_widgets:
            widget.grid_remove()
        
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
            messagebox.showwarning("Advertencia", "Genera primero un informe")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        messagebox.showinfo("Copiado", "Informe copiado al portapapeles")
    
    def clear_preview(self):
        self.preview.delete('1.0', tk.END)
        self.preview.insert('1.0', "\n\n    Vista Previa del Informe\n\n    "
                           "Completa el formulario y genera\n\n    "
                           "Se traducira automaticamente al ingles\n    "
                           "Se corregiran errores gramaticales\n\n ")
    
    def export_word(self):
        content = self.preview.get('1.0', 'end-1c').strip()
        if not content or "Vista Previa" in content:
            messagebox.showwarning("Advertencia", "Genera primero un informe")
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
                messagebox.showinfo("Exportado", f"Documento guardado en:\n{path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def generate(self):
        rt = self.report_type.get()
        
        if rt == "OPENED":
            if not self.summary.get().strip():
                messagebox.showerror("Error", "Summary obligatorio para OPENED")
                return
            proc = self.procedure.get_numbered_text()
            if not proc.strip() or proc.strip() == "1.":
                messagebox.showerror("Error", "Procedimiento obligatorio para OPENED")
                return
            if not self.expected.get('1.0', tk.END).strip():
                messagebox.showerror("Error", "Resultado Esperado obligatorio para OPENED")
                return
        
        if not self.equipment.get('1.0', tk.END).strip():
            messagebox.showerror("Error", "Equipment Information requerido")
            return
        if not self.description.get('1.0', tk.END).strip():
            messagebox.showerror("Error", "Descripcion requerida")
            return
        
        try:
            self.preview.delete('1.0', tk.END)
            
            if rt == "VERIFIED":
                self.preview.insert(tk.END, "Traduciendo...\n")
                self.preview.see(tk.END)
                self.root.update()
                
                eq = translate_equipment_info(self.equipment.get('1.0', tk.END).strip())
                self.preview.delete("end-2l", "end-1l")
                self.preview.insert(tk.END, "[Equipment information]:\n")
                self.preview.insert(tk.END, f"{eq}\n\n")
                self.root.update()
                
                self.preview.insert(tk.END, "The problem is VERIFIED in this version\n\n")
                self.root.update()
                
                self.preview.insert(tk.END, "Traduciendo descripcion...\n")
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
                
                messagebox.showinfo("Listo", "Informe generado correctamente")
                return
            
            self.preview.insert(tk.END, f"{rt}\n")
            if rt == "REOPENED":
                self.preview.insert(tk.END, "The problem continues, REOPENED in this version.\n\n")
            else:
                self.preview.insert(tk.END, "\n")
            self.root.update()
            
            if rt == "OPENED":
                self.preview.insert(tk.END, "Traduciendo...\n")
                self.preview.see(tk.END)
                self.root.update()
                
                summ = translate_and_correct(self.summary.get())
                self.preview.delete("end-2l", "end-1l")
                self.preview.insert(tk.END, f"Summary: {summ}\n\n")
                self.root.update()
            
            self.preview.insert(tk.END, "Traduciendo...\n")
            self.preview.see(tk.END)
            self.root.update()
            
            eq = translate_equipment_info(self.equipment.get('1.0', tk.END).strip())
            self.preview.delete("end-2l", "end-1l")
            self.preview.insert(tk.END, "[Equipment information]:\n\n")
            self.preview.insert(tk.END, f"{eq}\n\n")
            self.root.update()
            
            self.preview.insert(tk.END, "Traduciendo...\n")
            self.preview.see(tk.END)
            self.root.update()
            
            fault = translate_and_correct(self.description.get('1.0', tk.END).strip())
            self.preview.delete("end-2l", "end-1l")
            self.preview.insert(tk.END, "[Fault]:\n")
            self.preview.insert(tk.END, f"{fault}\n\n")
            self.root.update()
            
            proc = self.procedure.get_numbered_text()
            if proc.strip() and proc.strip() != "1.":
                self.preview.insert(tk.END, "Traduciendo...\n")
                self.preview.see(tk.END)
                self.root.update()
                
                proc_t = translate_and_correct(proc)
                self.preview.delete("end-2l", "end-1l")
                self.preview.insert(tk.END, "[Procedure]:\n")
                self.preview.insert(tk.END, f"{proc_t}\n\n")
                self.root.update()
            
            if rt == "OPENED":
                exp = self.expected.get('1.0', tk.END).strip()
                if exp:
                    self.preview.insert(tk.END, "Traduciendo...\n")
                    self.preview.see(tk.END)
                    self.root.update()
                    
                    exp_t = translate_and_correct(exp)
                    self.preview.delete("end-2l", "end-1l")
                    self.preview.insert(tk.END, "[Expected]:\n")
                    self.preview.insert(tk.END, f"{exp_t}\n\n")
                    self.root.update()
            
            att = self.attachments.get().strip()
            if att:
                self.preview.insert(tk.END, "[Attachments]:\n")
                self.preview.insert(tk.END, f"{att}\n")
            
            messagebox.showinfo("Listo", "Informe generado correctamente")
        
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = RepairReportGenerator(root)
    root.mainloop()