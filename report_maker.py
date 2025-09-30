import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from datetime import datetime
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import re
from deep_translator import GoogleTranslator
import language_tool_python

# Variables globales
translator = GoogleTranslator(source='auto', target='en')
tool = None

def init_language_tool():
    global tool
    if tool is None:
        try:
            print("Inicializando corrector gramatical...")
            tool = language_tool_python.LanguageTool('en-US')
            print("Corrector listo")
        except Exception as e:
            print(f"Error: {e}")
    return tool

def translate_to_english(text):
    if not text or not text.strip():
        return text
    try:
        return translator.translate(text)
    except Exception as e:
        print(f"Error traducción: {e}")
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
    except Exception as e:
        print(f"Error gramática: {e}")
        return text

def translate_and_correct(text):
    if not text or not text.strip():
        return text
    translated = translate_to_english(text)
    return correct_grammar(translated)

def translate_equipment_info(text):
    if not text or not text.strip():
        return text
    
    field_translations = {
        'nombre del equipo': 'Equipment name',
        'nombre': 'Equipment name',
        'modelo': 'Model',
        'número de serie': 'Serial Number',
        'numero de serie': 'Serial Number',
        'serial': 'Serial Number',
        'versión hardware': 'Hardware Version',
        'version hardware': 'Hardware Version',
        'versión software': 'Software Version',
        'version software': 'Software Version',
        'versión firmware': 'Firmware Version',
        'version firmware': 'Firmware Version',
        'código de país': 'Country Code',
        'codigo de pais': 'Country Code',
        'product id': 'Product ID',
    }
    
    lines = text.split('\n')
    translated_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            translated_lines.append('')
            continue
        
        if ':' in line:
            parts = line.split(':', 1)
            if len(parts) == 2:
                field = parts[0].strip()
                value = parts[1].strip()
                field_lower = field.lower()
                
                if field_lower in field_translations:
                    translated_lines.append(f"{field_translations[field_lower]}: {value}")
                else:
                    try:
                        field_translated = GoogleTranslator(source='auto', target='en').translate(field)
                        translated_lines.append(f"{field_translated}: {value}")
                    except:
                        translated_lines.append(line)
            else:
                translated_lines.append(line)
        else:
            translated_lines.append(line)
    
    return '\n'.join(translated_lines)

class MaterialColors:
    PRIMARY = '#1976D2'
    SUCCESS = '#4CAF50'
    ERROR = '#F44336'
    BG_LIGHT = '#FAFAFA'
    BG_CARD = '#FFFFFF'
    TEXT_PRIMARY = '#212121'
    TEXT_SECONDARY = '#757575'
    DIVIDER = '#BDBDBD'

class AutoNumberedText(scrolledtext.ScrolledText):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind('<Return>', self.auto_number)
        self.line_count = 0
        
    def auto_number(self, event):
        content = self.get('1.0', 'end-1c')
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        self.line_count = len(lines)
        self.insert('insert', f'\n{self.line_count + 1}. ')
        return 'break'
    
    def reset_numbering(self):
        self.line_count = 0
    
    def get_numbered_text(self):
        content = self.get('1.0', 'end-1c')
        lines = content.split('\n')
        clean_lines = []
        counter = 1
        for line in lines:
            clean_line = re.sub(r'^\d+\.\s*', '', line).strip()
            if clean_line:
                clean_lines.append(f"{counter}. {clean_line}")
                counter += 1
        return '\n'.join(clean_lines)

class RepairReportGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("ReportMaker - Generador de Informes de Reparos")
        self.root.geometry("1400x800")
        self.root.configure(bg=MaterialColors.BG_LIGHT)
        self.root.minsize(1200, 700)
        self.create_widgets()
    
    def create_widgets(self):
        # Header
        header = tk.Frame(self.root, bg=MaterialColors.PRIMARY, height=80)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)
        
        title_label = tk.Label(header, text="ReportMaker", font=('Segoe UI', 22, 'bold'),
                              bg=MaterialColors.PRIMARY, fg='white')
        title_label.pack(pady=20)
        
        # Contenedor principal - DOS COLUMNAS
        main_container = tk.Frame(self.root, bg=MaterialColors.BG_LIGHT)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # COLUMNA IZQUIERDA: Formulario
        left_frame = tk.Frame(main_container, bg=MaterialColors.BG_LIGHT)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        canvas = tk.Canvas(left_frame, bg=MaterialColors.BG_LIGHT, highlightthickness=0)
        scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg=MaterialColors.BG_LIGHT)
        
        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=650)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Tipo de Reparo
        self.create_section("Tipo de Reparo", 0)
        self.report_type = ttk.Combobox(self.scrollable_frame, values=["OPENED", "REOPENED", "VERIFIED"],
                                       state='readonly', font=('Segoe UI', 11), width=30)
        self.report_type.grid(row=1, column=0, sticky='w', padx=30, pady=(0, 20))
        self.report_type.current(0)
        self.report_type.bind('<<ComboboxSelected>>', self.update_form)
        
        # Resumen
        self.create_section("Resumen / Summary", 2)
        self.summary = tk.Entry(self.scrollable_frame, font=('Segoe UI', 11), bg='white', relief=tk.FLAT, borderwidth=2)
        self.summary.grid(row=3, column=0, sticky='ew', padx=30, pady=(0, 20))
        
        # Información del Equipo
        self.create_section("Información del Equipo", 4)
        self.equipment_info = scrolledtext.ScrolledText(self.scrollable_frame, font=('Consolas', 10),
            bg='white', height=8, relief=tk.FLAT, borderwidth=2, wrap=tk.WORD)
        self.equipment_info.grid(row=5, column=0, sticky='ew', padx=30, pady=(0, 20))
        
        # Descripción del Fallo
        self.create_section("Descripción del Fallo", 6)
        self.fault_text = scrolledtext.ScrolledText(self.scrollable_frame, font=('Segoe UI', 10),
            bg='white', height=8, relief=tk.FLAT, borderwidth=2, wrap=tk.WORD)
        self.fault_text.grid(row=7, column=0, sticky='ew', padx=30, pady=(0, 20))
        
        # Procedimiento
        self.procedure_row = 8
        self.create_section("Procedimiento (Enter = numerar)", self.procedure_row)
        self.procedure_text = AutoNumberedText(self.scrollable_frame, font=('Segoe UI', 10),
            bg='white', height=6, relief=tk.FLAT, borderwidth=2, wrap=tk.WORD)
        self.procedure_text.grid(row=self.procedure_row+1, column=0, sticky='ew', padx=30, pady=(0, 10))
        self.procedure_text.insert('1.0', '1. ')
        
        reset_btn = tk.Button(self.scrollable_frame, text="Reiniciar numeración",
                             command=self.reset_procedure, bg=MaterialColors.TEXT_SECONDARY, fg='white',
                             font=('Segoe UI', 9), relief=tk.FLAT, cursor='hand2', padx=15, pady=5)
        reset_btn.grid(row=self.procedure_row+2, column=0, sticky='w', padx=30, pady=(0, 20))
        
        # Resultado Esperado
        self.expected_row = 11
        self.create_section("Resultado Esperado", self.expected_row)
        self.expected_text = scrolledtext.ScrolledText(self.scrollable_frame, font=('Segoe UI', 10),
            bg='white', height=4, relief=tk.FLAT, borderwidth=2, wrap=tk.WORD)
        self.expected_text.grid(row=self.expected_row+1, column=0, sticky='ew', padx=30, pady=(0, 20))
        
        # Adjuntos
        self.create_section("Archivos Adjuntos", 13)
        self.attachments = tk.Entry(self.scrollable_frame, font=('Segoe UI', 11), bg='white', relief=tk.FLAT, borderwidth=2)
        self.attachments.grid(row=14, column=0, sticky='ew', padx=30, pady=(0, 20))
        
        # Botones
        button_frame = tk.Frame(self.scrollable_frame, bg=MaterialColors.BG_LIGHT)
        button_frame.grid(row=15, column=0, pady=30)
        
        tk.Button(button_frame, text="Limpiar Todo", command=self.clear_form,
                 bg=MaterialColors.TEXT_SECONDARY, fg='white', font=('Segoe UI', 11, 'bold'),
                 relief=tk.FLAT, cursor='hand2', padx=20, pady=12).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Generar Informe", command=self.generate_report,
                 bg=MaterialColors.SUCCESS, fg='white', font=('Segoe UI', 12, 'bold'),
                 relief=tk.FLAT, cursor='hand2', padx=30, pady=15).pack(side=tk.LEFT, padx=5)
        
        self.scrollable_frame.columnconfigure(0, weight=1)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # COLUMNA DERECHA: Vista Previa
        right_frame = tk.Frame(main_container, bg=MaterialColors.BG_LIGHT)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        preview_header = tk.Frame(right_frame, bg=MaterialColors.SUCCESS, height=60)
        preview_header.pack(fill=tk.X, side=tk.TOP)
        preview_header.pack_propagate(False)
        
        tk.Label(preview_header, text="Vista Previa del Informe", font=('Segoe UI', 16, 'bold'),
                bg=MaterialColors.SUCCESS, fg='white').pack(pady=15)
        
        preview_container = tk.Frame(right_frame, bg='white', relief=tk.SOLID, borderwidth=2)
        preview_container.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        self.preview_text = scrolledtext.ScrolledText(preview_container, font=('Consolas', 10),
            bg='white', fg=MaterialColors.TEXT_PRIMARY, wrap=tk.WORD, padx=15, pady=15)
        self.preview_text.pack(fill=tk.BOTH, expand=True)
        self.preview_text.insert('1.0', "\n\n    Aquí aparecerá tu informe traducido\n\n    1. Completa los campos\n    2. Genera el informe\n    3. Edítalo si quieres\n    4. Cópialo\n\n")
        
        # Botones de vista previa
        btn_frame = tk.Frame(right_frame, bg=MaterialColors.BG_LIGHT)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Button(btn_frame, text="Copiar Todo", command=self.copy_preview,
                 bg=MaterialColors.PRIMARY, fg='white', font=('Segoe UI', 10, 'bold'),
                 relief=tk.FLAT, cursor='hand2', padx=20, pady=10).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Exportar a Word", command=self.export_word,
                 bg=MaterialColors.SUCCESS, fg='white', font=('Segoe UI', 10, 'bold'),
                 relief=tk.FLAT, cursor='hand2', padx=20, pady=10).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Limpiar Vista", command=self.clear_preview,
                 bg=MaterialColors.TEXT_SECONDARY, fg='white', font=('Segoe UI', 10, 'bold'),
                 relief=tk.FLAT, cursor='hand2', padx=20, pady=10).pack(side=tk.RIGHT)
        
        self.update_form()
    
    def create_section(self, title, row):
        card = tk.Frame(self.scrollable_frame, bg=MaterialColors.BG_CARD, relief=tk.FLAT)
        card.grid(row=row, column=0, sticky='ew', padx=20, pady=(10, 5))
        card.configure(highlightbackground=MaterialColors.DIVIDER, highlightthickness=1)
        tk.Label(card, text=title, font=('Segoe UI', 12, 'bold'),
                bg=MaterialColors.BG_CARD, fg=MaterialColors.PRIMARY, anchor='w',
                padx=10, pady=8).pack(fill=tk.X)
    
    def reset_procedure(self):
        self.procedure_text.delete('1.0', tk.END)
        self.procedure_text.reset_numbering()
        self.procedure_text.insert('1.0', '1. ')
    
    def update_form(self, event=None):
        expected_rows = [self.expected_row, self.expected_row+1]
        if self.report_type.get() == "OPENED":
            for widget in self.scrollable_frame.grid_slaves():
                info = widget.grid_info()
                if info and 'row' in info and info['row'] in expected_rows:
                    widget.grid()
        else:
            for widget in self.scrollable_frame.grid_slaves():
                info = widget.grid_info()
                if info and 'row' in info and info['row'] in expected_rows:
                    widget.grid_remove()
    
    def clear_form(self):
        self.summary.delete(0, tk.END)
        self.equipment_info.delete('1.0', tk.END)
        self.fault_text.delete('1.0', tk.END)
        self.procedure_text.delete('1.0', tk.END)
        self.procedure_text.reset_numbering()
        self.procedure_text.insert('1.0', '1. ')
        self.expected_text.delete('1.0', tk.END)
        self.attachments.delete(0, tk.END)
        self.report_type.current(0)
        self.update_form()
    
    def copy_preview(self):
        content = self.preview_text.get('1.0', 'end-1c')
        if not content.strip() or "Aquí aparecerá" in content:
            messagebox.showwarning("Advertencia", "Genera primero un informe")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        messagebox.showinfo("Copiado", "Informe copiado al portapapeles")
    
    def clear_preview(self):
        self.preview_text.delete('1.0', tk.END)
        self.preview_text.insert('1.0', "\n\n    Aquí aparecerá tu informe traducido\n\n    1. Completa los campos\n    2. Genera el informe\n    3. Edítalo si quieres\n    4. Cópialo\n\n")
    
    def export_word(self):
        content = self.preview_text.get('1.0', 'end-1c').strip()
        if not content or "Aquí aparecerá" in content:
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
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = filedialog.asksaveasfilename(
                defaultextension=".docx",
                filetypes=[("Word Document", "*.docx")],
                initialfile=f"Repair_Report_{self.report_type.get()}_{timestamp}.docx"
            )
            
            if filepath:
                doc.save(filepath)
                messagebox.showinfo("Exportado", f"Guardado en:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar:\n{str(e)}")
    
    def generate_report(self):
        if not self.summary.get().strip():
            messagebox.showerror("Error", "Ingrese un resumen")
            return
        if not self.equipment_info.get('1.0', tk.END).strip():
            messagebox.showerror("Error", "Ingrese información del equipo")
            return
        if not self.fault_text.get('1.0', tk.END).strip():
            messagebox.showerror("Error", "Describa el fallo")
            return
        
        try:
            self.preview_text.delete('1.0', tk.END)
            report_type = self.report_type.get()
            
            # Título
            self.preview_text.insert(tk.END, f"{report_type}\n")
            self.root.update()
            
            if report_type == "REOPENED":
                self.preview_text.insert(tk.END, "The problem continues, REOPENED in this version.\n\n")
            elif report_type == "VERIFIED":
                self.preview_text.insert(tk.END, "The problem is VERIFIED in this version\n\n")
            else:
                self.preview_text.insert(tk.END, "\n")
            self.root.update()
            
            # Resumen
            self.preview_text.insert(tk.END, "Traduciendo resumen...\n")
            self.preview_text.see(tk.END)
            self.root.update()
            
            summary = translate_and_correct(self.summary.get())
            self.preview_text.delete("end-2l", "end-1l")
            self.preview_text.insert(tk.END, f"Summary: {summary}\n\n")
            self.root.update()
            
            # Equipo
            self.preview_text.insert(tk.END, "Traduciendo equipo...\n")
            self.preview_text.see(tk.END)
            self.root.update()
            
            equipment = translate_equipment_info(self.equipment_info.get('1.0', tk.END).strip())
            self.preview_text.delete("end-2l", "end-1l")
            self.preview_text.insert(tk.END, "[Equipment information]:\n\n")
            self.preview_text.insert(tk.END, f"{equipment}\n\n")
            self.root.update()
            
            # Fallo
            self.preview_text.insert(tk.END, "Traduciendo fallo...\n")
            self.preview_text.see(tk.END)
            self.root.update()
            
            fault = translate_and_correct(self.fault_text.get('1.0', tk.END).strip())
            self.preview_text.delete("end-2l", "end-1l")
            self.preview_text.insert(tk.END, "[Fault]:\n")
            self.preview_text.insert(tk.END, f"{fault}\n\n")
            self.root.update()
            
            # Procedimiento
            procedure = self.procedure_text.get_numbered_text()
            if procedure.strip() and procedure.strip() != "1.":
                self.preview_text.insert(tk.END, "Traduciendo procedimiento...\n")
                self.preview_text.see(tk.END)
                self.root.update()
                
                proc_trans = translate_and_correct(procedure)
                self.preview_text.delete("end-2l", "end-1l")
                self.preview_text.insert(tk.END, "[Procedure]:\n")
                self.preview_text.insert(tk.END, f"{proc_trans}\n\n")
                self.root.update()
            
            # Esperado
            if report_type == "OPENED":
                expected = self.expected_text.get('1.0', tk.END).strip()
                if expected:
                    self.preview_text.insert(tk.END, "Traduciendo esperado...\n")
                    self.preview_text.see(tk.END)
                    self.root.update()
                    
                    exp_trans = translate_and_correct(expected)
                    self.preview_text.delete("end-2l", "end-1l")
                    self.preview_text.insert(tk.END, "[Expected]:\n")
                    self.preview_text.insert(tk.END, f"{exp_trans}\n\n")
                    self.root.update()
            
            # Adjuntos
            attachments = self.attachments.get().strip()
            if attachments:
                self.preview_text.insert(tk.END, "[Attachments]:\n")
                self.preview_text.insert(tk.END, f"{attachments}\n")
            
            messagebox.showinfo("Listo", "Informe generado\nPuedes editarlo y copiarlo")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RepairReportGenerator(root)
    root.mainloop()