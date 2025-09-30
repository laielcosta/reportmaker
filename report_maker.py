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
    PRIMARY = '#1976D2'
    SUCCESS = '#4CAF50'
    ERROR = '#F44336'
    BG_LIGHT = '#E8E8E8'
    BG_CARD = '#FFFFFF'
    TEXT_PRIMARY = '#212121'
    TEXT_SECONDARY = '#757575'

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
        self.root.title("ReportMaker")
        self.root.geometry("1400x800")
        self.root.configure(bg=MaterialColors.BG_LIGHT)
        self.root.minsize(1200, 700)
        
        # Guardar referencias a widgets que se ocultan/muestran
        self.summary_widgets = []
        self.procedure_widgets = []
        self.expected_widgets = []
        
        self.create_widgets()
    
    def create_widgets(self):
        # Header
        header = tk.Frame(self.root, bg=MaterialColors.PRIMARY, height=80)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)
        tk.Label(header, text="ReportMaker", font=('Segoe UI', 22, 'bold'),
                bg=MaterialColors.PRIMARY, fg='white').pack(pady=20)
        
        # Contenedor principal
        main = tk.Frame(self.root, bg=MaterialColors.BG_LIGHT)
        main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # COLUMNA IZQUIERDA
        left = tk.Frame(main, bg=MaterialColors.BG_LIGHT)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        canvas = tk.Canvas(left, bg=MaterialColors.BG_LIGHT, highlightthickness=0)
        scrollbar = ttk.Scrollbar(left, orient="vertical", command=canvas.yview)
        self.form_frame = tk.Frame(canvas, bg=MaterialColors.BG_LIGHT)
        
        self.form_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.form_frame, anchor="nw", width=650)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        row_counter = 0
        
        # Tipo de Reparo
        self.add_section("Tipo de Reparo", row_counter)
        row_counter += 1
        self.report_type = ttk.Combobox(self.form_frame, values=["OPENED", "REOPENED", "VERIFIED"],
                                       state='readonly', font=('Segoe UI', 11), width=30)
        self.report_type.grid(row=row_counter, column=0, sticky='w', padx=30, pady=(0, 20))
        self.report_type.current(0)
        self.report_type.bind('<<ComboboxSelected>>', self.on_type_change)
        row_counter += 1
        
        # Summary (solo OPENED) - GUARDAR WIDGETS
        summary_card = self.add_section("Summary", row_counter)
        self.summary_widgets.append(summary_card)
        row_counter += 1
        self.summary = tk.Entry(self.form_frame, font=('Segoe UI', 11), bg='white', relief=tk.FLAT, borderwidth=2)
        self.summary.grid(row=row_counter, column=0, sticky='ew', padx=30, pady=(0, 20))
        self.summary_widgets.append(self.summary)
        row_counter += 1
        
        # Equipment
        self.add_section("Equipment Information", row_counter)
        row_counter += 1
        self.equipment = scrolledtext.ScrolledText(self.form_frame, font=('Consolas', 10),
            bg='white', height=8, relief=tk.FLAT, borderwidth=2, wrap=tk.WORD)
        self.equipment.grid(row=row_counter, column=0, sticky='ew', padx=30, pady=(0, 20))
        row_counter += 1
        
        # Descripción
        self.add_section("Descripción", row_counter)
        row_counter += 1
        self.description = scrolledtext.ScrolledText(self.form_frame, font=('Segoe UI', 10),
            bg='white', height=8, relief=tk.FLAT, borderwidth=2, wrap=tk.WORD)
        self.description.grid(row=row_counter, column=0, sticky='ew', padx=30, pady=(0, 20))
        row_counter += 1
        
        # Procedimiento (OPENED y REOPENED) - GUARDAR WIDGETS
        proc_card = self.add_section("Procedimiento", row_counter)
        self.procedure_widgets.append(proc_card)
        row_counter += 1
        self.procedure = AutoNumberedText(self.form_frame, font=('Segoe UI', 10),
            bg='white', height=6, relief=tk.FLAT, borderwidth=2, wrap=tk.WORD)
        self.procedure.grid(row=row_counter, column=0, sticky='ew', padx=30, pady=(0, 10))
        self.procedure.insert('1.0', '1. ')
        self.procedure_widgets.append(self.procedure)
        row_counter += 1
        
        proc_btn = tk.Button(self.form_frame, text="Reiniciar", command=self.reset_proc,
                 bg=MaterialColors.TEXT_SECONDARY, fg='white', font=('Segoe UI', 9),
                 relief=tk.FLAT, cursor='hand2', padx=15, pady=5)
        proc_btn.grid(row=row_counter, column=0, sticky='w', padx=30, pady=(0, 20))
        self.procedure_widgets.append(proc_btn)
        row_counter += 1
        
        # Resultado Esperado (solo OPENED) - GUARDAR WIDGETS
        exp_card = self.add_section("Resultado Esperado", row_counter)
        self.expected_widgets.append(exp_card)
        row_counter += 1
        self.expected = scrolledtext.ScrolledText(self.form_frame, font=('Segoe UI', 10),
            bg='white', height=4, relief=tk.FLAT, borderwidth=2, wrap=tk.WORD)
        self.expected.grid(row=row_counter, column=0, sticky='ew', padx=30, pady=(0, 20))
        self.expected_widgets.append(self.expected)
        row_counter += 1
        
        # Adjuntos
        self.add_section("Attachments", row_counter)
        row_counter += 1
        self.attachments = tk.Entry(self.form_frame, font=('Segoe UI', 11), bg='white', relief=tk.FLAT, borderwidth=2)
        self.attachments.grid(row=row_counter, column=0, sticky='ew', padx=30, pady=(0, 20))
        row_counter += 1
        
        # Botones
        btn_frame = tk.Frame(self.form_frame, bg=MaterialColors.BG_LIGHT)
        btn_frame.grid(row=row_counter, column=0, pady=30)
        
        tk.Button(btn_frame, text="Limpiar", command=self.clear_form,
                 bg=MaterialColors.TEXT_SECONDARY, fg='white', font=('Segoe UI', 11, 'bold'),
                 relief=tk.FLAT, cursor='hand2', padx=20, pady=12).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Generar Informe", command=self.generate,
                 bg=MaterialColors.SUCCESS, fg='white', font=('Segoe UI', 12, 'bold'),
                 relief=tk.FLAT, cursor='hand2', padx=30, pady=15).pack(side=tk.LEFT, padx=5)
        
        self.form_frame.columnconfigure(0, weight=1)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Scroll con mouse
        def on_mouse(e):
            canvas.yview_scroll(int(-1*(e.delta/120)), "units")
        canvas.bind('<Enter>', lambda e: canvas.bind_all("<MouseWheel>", on_mouse))
        canvas.bind('<Leave>', lambda e: canvas.unbind_all("<MouseWheel>"))
        
        # COLUMNA DERECHA
        right = tk.Frame(main, bg=MaterialColors.BG_LIGHT)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        preview_header = tk.Frame(right, bg=MaterialColors.SUCCESS, height=60)
        preview_header.pack(fill=tk.X)
        preview_header.pack_propagate(False)
        tk.Label(preview_header, text="Vista Previa", font=('Segoe UI', 16, 'bold'),
                bg=MaterialColors.SUCCESS, fg='white').pack(pady=15)
        
        preview_container = tk.Frame(right, bg='white', relief=tk.SOLID, borderwidth=2)
        preview_container.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        self.preview = scrolledtext.ScrolledText(preview_container, font=('Consolas', 10),
            bg='white', fg=MaterialColors.TEXT_PRIMARY, wrap=tk.WORD, padx=15, pady=15)
        self.preview.pack(fill=tk.BOTH, expand=True)
        self.preview.insert('1.0', "\n\n    Vista Previa del Informe\n\n    Completa el formulario y genera\n\n    Se corregirán errores y traducirá al inglés automaticamente\n\n ")
        
        # Botones vista previa
        btn_preview = tk.Frame(right, bg=MaterialColors.BG_LIGHT)
        btn_preview.pack(fill=tk.X, pady=(10, 0))
        
        tk.Button(btn_preview, text="Copiar", command=self.copy_preview,
                 bg=MaterialColors.PRIMARY, fg='white', font=('Segoe UI', 10, 'bold'),
                 relief=tk.FLAT, cursor='hand2', padx=20, pady=10).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_preview, text="Exportar Word", command=self.export_word,
                 bg=MaterialColors.SUCCESS, fg='white', font=('Segoe UI', 10, 'bold'),
                 relief=tk.FLAT, cursor='hand2', padx=20, pady=10).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_preview, text="Limpiar Vista", command=self.clear_preview,
                 bg=MaterialColors.TEXT_SECONDARY, fg='white', font=('Segoe UI', 10, 'bold'),
                 relief=tk.FLAT, cursor='hand2', padx=20, pady=10).pack(side=tk.RIGHT)
        
        # Inicializar visibilidad
        self.on_type_change()
    
    def add_section(self, title, row):
        card = tk.Frame(self.form_frame, bg=MaterialColors.BG_CARD, relief=tk.FLAT)
        card.grid(row=row, column=0, sticky='ew', padx=20, pady=(10, 5))
        card.configure(highlightbackground='#BDBDBD', highlightthickness=1)
        tk.Label(card, text=title, font=('Segoe UI', 12, 'bold'),
                bg=MaterialColors.BG_CARD, fg=MaterialColors.PRIMARY,
                anchor='w', padx=10, pady=8).pack(fill=tk.X)
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
            # OPENED: mostrar TODO
            for widget in self.summary_widgets:
                widget.grid()
            for widget in self.procedure_widgets:
                widget.grid()
            for widget in self.expected_widgets:
                widget.grid()
        
        elif report_type == "REOPENED":
            # REOPENED: mostrar solo Procedure (ocultar Summary y Expected)
            for widget in self.procedure_widgets:
                widget.grid()
        
        elif report_type == "VERIFIED":
            # VERIFIED: ocultar todo (Summary, Procedure y Expected)
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
            messagebox.showwarning("Advertencia", "Genera primero un informe")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        messagebox.showinfo("Copiado", "Informe copiado")
    
    def clear_preview(self):
        self.preview.delete('1.0', tk.END)
        self.preview.insert('1.0', "\n\n    Vista Previa del Informe\n\n    Completa el formulario y genera\n\n")
    
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
                messagebox.showinfo("Exportado", f"Guardado en:\n{path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def generate(self):
        rt = self.report_type.get()
        
        # Validaciones
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
            messagebox.showerror("Error", "Descripción requerida")
            return
        
        try:
            self.preview.delete('1.0', tk.END)
            
            # VERIFIED tiene formato especial
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
                
                self.preview.insert(tk.END, "Traduciendo...\n")
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
                
                messagebox.showinfo("Listo", "Informe generado")
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
                self.preview.insert(tk.END, "Traduciendo...\n")
                self.preview.see(tk.END)
                self.root.update()
                
                summ = translate_and_correct(self.summary.get())
                self.preview.delete("end-2l", "end-1l")
                self.preview.insert(tk.END, f"Summary: {summ}\n\n")
                self.root.update()
            
            # Equipment
            self.preview.insert(tk.END, "Traduciendo...\n")
            self.preview.see(tk.END)
            self.root.update()
            
            eq = translate_equipment_info(self.equipment.get('1.0', tk.END).strip())
            self.preview.delete("end-2l", "end-1l")
            self.preview.insert(tk.END, "[Equipment information]:\n\n")
            self.preview.insert(tk.END, f"{eq}\n\n")
            self.root.update()
            
            # Fault
            self.preview.insert(tk.END, "Traduciendo...\n")
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
                self.preview.insert(tk.END, "Traduciendo...\n")
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
                    self.preview.insert(tk.END, "Traduciendo...\n")
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
            
            messagebox.showinfo("Listo", "Informe generado")
        
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = RepairReportGenerator(root)
    root.mainloop()