# ElCliboar
# Copyright (C) 2026 César Díaz Menes
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# Autor: César Díaz Menes
# Version: 1.2.0
#
# elCliboar es una aplicacion de escritorio para gestionar avisos de trabajo.
# Permite registrar clientes, equipos, averias, notas y asistencias, guardar la
# informacion en una base de datos SQLite, consultar los registros y copiar los
# datos seleccionados al portapapeles o guardarlos en un archivo de texto.
# Tambien incluye interfaz bilingue en espanol e ingles.
#
# elCliboar is a desktop application for managing work notices.
# It allows you to register clients, equipment, faults, notes, and attendance,
# store the information in an SQLite database, query records, and copy selected
# data to the clipboard or save it to a text file.
# It also includes a bilingual interface in Spanish and English.
#
# Dependencias en Linux:
# - Sistema: sudo apt install python3-tk
# - Python: python3 -m pip install Pillow
# - sqlite3 forma parte de la libreria estandar de Python.

import os
import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from PIL import Image, ImageDraw

DB_NAME = os.path.expanduser("./elcliboar.db")
APP_VERSION = "1.2.0"

TRANSLATIONS = {
    "es": {
        "app_title": "(c) elCliboar",
        "tab_form": "Formulario",
        "tab_list": "Listado",
        "label_client": "Cliente",
        "label_address": "Dir.",
        "label_ticket": "Nº Aviso",
        "label_contact": "Per/Cto",
        "label_phone": "Mail/Tel.",
        "label_serial": "SN",
        "label_asset": "Bien",
        "label_problem": "Avería",
        "label_note": "Nota",
        "label_assistance": "Asistencia",
        "label_solved": "Sol.",
        "label_no_invoice": "Facturable",
        "label_language": "Idioma",
        "label_help": "Ayuda",
        "label_save": "Guardar",
        "label_clear": "Limpiar",
        "label_search": "Buscar",
        "label_next": "-->",
        "label_txt": "TXT",
        "label_copy": "Copiar",
        "label_refresh": "Refrescar",
        "label_client_col": "Cliente",
        "label_ticket_col": "Nº Aviso",
        "label_asset_col": "Bien",
        "label_problem_col": "Avería",
        "label_save_txt": "Guardar TXT",
        "label_delete": "Borrar",
        "radio_lab": "Lab",
        "radio_remote": "Remoto",
        "radio_client": "Cliente",
        "msg_saved": "Registro guardado correctamente.",
        "msg_updated": "Registro actualizado correctamente.",
        "msg_no_client": "Introduce un cliente para buscar.",
        "msg_not_found": "No se encontraron registros para este cliente.",
        "msg_no_more": "No hay más registros.",
        "msg_first_search": "Primero realiza una búsqueda.",
        "msg_txt_saved": "Texto pegado en el archivo TXT.",
        "msg_copy_ok": "Texto copiado al portapapeles.",
        "msg_delete_confirm": "¿Seguro que quieres borrar este registro completo?",
        "msg_delete_ok": "Registro borrado correctamente.",
        "msg_empty_record": "No se puede guardar un registro vacío.",
        "msg_select_record": "Selecciona un registro en la lista para borrar.",
        "msg_search_title": "Buscar",
        "help_title": "Ayuda de elCliboar",
        "help_description": "elCliboar es una aplicacion de escritorio bilingue para gestionar avisos de trabajo. Guarda los datos en SQLite y permite exportarlos o copiarlos.",
        "help_usage": "Uso:\n1. Completa los datos del aviso y pulsa Guardar.\n2. Usa Buscar y Siguiente para consultar avisos por cliente.\n3. Usa TXT o Copiar para exportar la informacion.\n4. En Listado puedes refrescar y borrar registros.\n5. Cambia el idioma con el selector inferior.",
        "msg_no_invoice_yes": "Sí",
        "msg_no_invoice_no": "No",
        "clipboard_prefix_client": "Cliente",
        "clipboard_prefix_address": "Dir.",
        "clipboard_prefix_ticket": "Nº Aviso",
        "clipboard_prefix_contact": "Per/Cto",
        "clipboard_prefix_phone": "Email/Telf.",
        "clipboard_prefix_assistance": "Asistencia",
        "clipboard_prefix_asset": "Bien",
        "clipboard_prefix_problem": "Avería",
        "clipboard_prefix_solution": "Solución",
        "clipboard_prefix_note": "Nota",
        "clipboard_prefix_no_invoice": "Facturable",
    },
    "en": {
        "app_title": "(c) elCliboar",
        "tab_form": "Form",
        "tab_list": "List",
        "label_client": "Client",
        "label_address": "Address",
        "label_ticket": "Ticket #",
        "label_contact": "Contact",
        "label_phone": "Mail/Tel.",
        "label_serial": "SN",
        "label_asset": "Asset",
        "label_problem": "Problem",
        "label_note": "Note",
        "label_assistance": "Assistance",
        "label_solved": "Sol.",
        "label_no_invoice": "Billable",
        "label_language": "Language",
        "label_help": "Help",
        "label_save": "Save",
        "label_clear": "Clear",
        "label_search": "Search",
        "label_next": "Next",
        "label_txt": "TXT",
        "label_copy": "Copy",
        "label_refresh": "Refresh",
        "label_client_col": "Client",
        "label_ticket_col": "Ticket #",
        "label_asset_col": "Asset",
        "label_problem_col": "Problem",
        "label_save_txt": "Save TXT",
        "label_delete": "Delete",
        "radio_lab": "Lab",
        "radio_remote": "Remote",
        "radio_client": "Client",
        "msg_saved": "Record saved successfully.",
        "msg_updated": "Record updated successfully.",
        "msg_no_client": "Enter a client name to search.",
        "msg_not_found": "No records found for that client.",
        "msg_no_more": "No more records.",
        "msg_first_search": "Run a search first.",
        "msg_txt_saved": "Text saved to the TXT file.",
        "msg_copy_ok": "Text copied to the clipboard.",
        "msg_delete_confirm": "Are you sure you want to delete this full record?",
        "msg_delete_ok": "Record deleted successfully.",
        "msg_empty_record": "An empty record cannot be saved.",
        "msg_select_record": "Select a record in the list to delete.",
        "msg_search_title": "Search",
        "help_title": "elCliboar Help",
        "help_description": "elCliboar is a bilingual desktop application for managing work tickets. It stores data in SQLite and lets you export or copy it.",
        "help_usage": "Usage:\n1. Fill in the ticket details and click Save.\n2. Use Search and Next to find tickets by client.\n3. Use TXT or Copy to export the information.\n4. In List, you can refresh and delete records.\n5. Change the language with the selector at the bottom.",
        "msg_no_invoice_yes": "Yes",
        "msg_no_invoice_no": "No",
        "clipboard_prefix_client": "Client",
        "clipboard_prefix_address": "Address",
        "clipboard_prefix_ticket": "Ticket #",
        "clipboard_prefix_contact": "Contact",
        "clipboard_prefix_phone": "Email/Phone",
        "clipboard_prefix_assistance": "Assistance",
        "clipboard_prefix_asset": "Asset",
        "clipboard_prefix_problem": "Problem",
        "clipboard_prefix_solution": "Solution",
        "clipboard_prefix_note": "Note",
        "clipboard_prefix_no_invoice": "Billable",
    },
}


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS avisos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT,
            direccion TEXT,
            n_aviso TEXT,
            per_cto TEXT,
            telefono TEXT,
            sn TEXT,
            bien TEXT,
            averia TEXT,
            solucion TEXT,
            asistencia TEXT,
            nota TEXT,
            no_fact INTEGER
        )
        """
    )
    conn.commit()
    conn.close()


def create_icon():
    image = Image.new("RGB", (64, 64), color="white")
    draw = ImageDraw.Draw(image)
    draw.rectangle([16, 16, 48, 48], fill="gray")
    return image


class EllinboardT(tk.Tk):
    def __init__(self):
        super().__init__()
        self.current_lang = "es"
        self.search_results = []
        self.current_result_index = 0

        self.title(f"{TRANSLATIONS[self.current_lang]['app_title']} - v{APP_VERSION}")
        self.geometry("420x560")
        self.resizable(False, False)

        self.notebook = ttk.Notebook(self)
        self.form_frame = tk.Frame(self)
        self.list_frame = tk.Frame(self)
        self.notebook.add(self.form_frame, text=TRANSLATIONS[self.current_lang]["tab_form"])
        self.notebook.add(self.list_frame, text=TRANSLATIONS[self.current_lang]["tab_list"])
        self.notebook.pack(fill="both", expand=True)

        self.signature_label = tk.Label(
            self,
            text="César Díaz Menes",
            fg="#7b7b7b",
            font=("TkDefaultFont", 7),
            anchor="sw",
        )
        self.signature_label.place(x=8, y=526)

        self.license_label = tk.Label(
            self,
            text="GPLv3",
            fg="#8a8a8a",
            font=("TkDefaultFont", 6),
            anchor="sw",
        )
        self.license_label.place(x=8, y=540)

        self.language_frame = tk.Frame(self)
        self.language_frame.pack(anchor="ne", padx=12, pady=(8, 0))
        self.language_var = tk.StringVar(value="Español")
        self.lang_labels = {"es": "Español", "en": "English"}
        self.lang_combo = ttk.Combobox(
            self.language_frame,
            textvariable=self.language_var,
            values=["Español", "English"],
            state="readonly",
            width=10,
        )
        self.lang_combo.pack(side="left")
        self.lang_combo.bind("<<ComboboxSelected>>", self.change_language)
        self.help_button = tk.Button(
            self.language_frame,
            text=TRANSLATIONS[self.current_lang]["label_help"],
            command=self.show_help,
        )
        self.help_button.pack(side="left", padx=(6, 0))

        self.labels = {}
        self.create_form_widgets()
        self.create_list_widgets()
        self.apply_language(self.current_lang)

    def change_language(self, event=None):
        selected = self.language_var.get()
        language = "es" if selected == "Español" else "en" if selected == "English" else self.current_lang
        self.apply_language(language)

    def show_help(self):
        texts = TRANSLATIONS[self.current_lang]
        help_window = tk.Toplevel(self)
        help_window.title(texts["help_title"])
        help_window.geometry("390x250")
        help_window.resizable(False, False)
        help_window.transient(self)

        tk.Label(
            help_window,
            text=texts["help_description"],
            justify="left",
            wraplength=360,
            anchor="w",
            font=("TkDefaultFont", 9),
        ).pack(fill="x", padx=12, pady=(12, 8))
        tk.Label(
            help_window,
            text=texts["help_usage"],
            justify="left",
            wraplength=360,
            anchor="w",
            font=("TkDefaultFont", 9),
        ).pack(fill="both", expand=True, padx=12, pady=(0, 12))

    def create_form_widgets(self):
        self.labels["client"] = tk.Label(self.form_frame, text=TRANSLATIONS[self.current_lang]["label_client"])
        self.labels["client"].place(x=10, y=10)
        self.labels["address"] = tk.Label(self.form_frame, text=TRANSLATIONS[self.current_lang]["label_address"])
        self.labels["address"].place(x=10, y=40)
        self.labels["ticket"] = tk.Label(self.form_frame, text=TRANSLATIONS[self.current_lang]["label_ticket"])
        self.labels["ticket"].place(x=10, y=70)
        self.labels["contact"] = tk.Label(self.form_frame, text=TRANSLATIONS[self.current_lang]["label_contact"])
        self.labels["contact"].place(x=10, y=100)
        self.labels["phone"] = tk.Label(self.form_frame, text=TRANSLATIONS[self.current_lang]["label_phone"])
        self.labels["phone"].place(x=10, y=130)
        self.labels["asset"] = tk.Label(self.form_frame, text=TRANSLATIONS[self.current_lang]["label_asset"])
        self.labels["asset"].place(x=10, y=190)
        self.labels["problem"] = tk.Label(self.form_frame, text=TRANSLATIONS[self.current_lang]["label_problem"])
        self.labels["problem"].place(x=10, y=220)
        self.labels["note"] = tk.Label(self.form_frame, text=TRANSLATIONS[self.current_lang]["label_note"])
        self.labels["note"].place(x=10, y=380)

        self.textBox1 = tk.Entry(self.form_frame)
        self.textBox1.place(x=88, y=10, width=220)
        self.textBox2 = tk.Entry(self.form_frame)
        self.textBox2.place(x=88, y=40, width=220)
        self.textBox3 = tk.Entry(self.form_frame)
        self.textBox3.place(x=90, y=70, width=165)
        self.textBox4 = tk.Entry(self.form_frame)
        self.textBox4.place(x=90, y=100, width=165)
        self.textBox5 = tk.Entry(self.form_frame)
        self.textBox5.place(x=90, y=130, width=165)
        self.textBox6 = tk.Entry(self.form_frame)
        self.textBox6.place(x=90, y=160, width=280)
        self.textBox7 = tk.Entry(self.form_frame)
        self.textBox7.place(x=90, y=190, width=280)
        self.textBox8 = tk.Entry(self.form_frame)
        self.textBox8.place(x=90, y=380, width=180)

        self.richTextBox1 = tk.Text(self.form_frame, height=2, width=35)
        self.richTextBox1.place(x=90, y=220, width=280, height=50)
        self.richTextBox2 = tk.Text(self.form_frame, height=5, width=35)
        self.richTextBox2.place(x=90, y=290, width=280, height=70)

        self.checkBox1_var = tk.BooleanVar()
        self.checkBox1 = tk.Checkbutton(self.form_frame, text=TRANSLATIONS[self.current_lang]["label_solved"], variable=self.checkBox1_var)
        self.checkBox1.place(x=10, y=290)

        self.checkBox2_var = tk.BooleanVar()
        self.checkBox2 = tk.Checkbutton(self.form_frame, text=TRANSLATIONS[self.current_lang]["label_serial"], variable=self.checkBox2_var)
        self.checkBox2.place(x=10, y=160)

        self.bottom_frame = tk.Frame(self.form_frame, height=56)
        self.bottom_frame.pack(side="bottom", fill="x", padx=(0, 46), pady=(4, 0))
        self.bottom_frame.pack_propagate(False)

        self.checkBox3_var = tk.BooleanVar()
        self.checkBox3 = tk.Checkbutton(self.bottom_frame, text=TRANSLATIONS[self.current_lang]["label_no_invoice"], variable=self.checkBox3_var)
        self.checkBox3.pack(side="left", padx=6, pady=8)

        self.groupBox1 = tk.LabelFrame(self.form_frame, text=TRANSLATIONS[self.current_lang]["label_assistance"])
        self.groupBox1.place(x=262, y=70, width=110, height=82)
        self.radio_var = tk.StringVar(value="Lab")
        self.radioButton3 = tk.Radiobutton(self.groupBox1, text=TRANSLATIONS[self.current_lang]["radio_lab"], variable=self.radio_var, value="Lab")
        self.radioButton3.place(x=6, y=2)
        self.radioButton1 = tk.Radiobutton(self.groupBox1, text=TRANSLATIONS[self.current_lang]["radio_remote"], variable=self.radio_var, value="Remoto")
        self.radioButton1.place(x=6, y=20)
        self.radioButton2 = tk.Radiobutton(self.groupBox1, text=TRANSLATIONS[self.current_lang]["radio_client"], variable=self.radio_var, value="Cliente")
        self.radioButton2.place(x=6, y=38)

        self.button1 = tk.Button(self.bottom_frame, text=TRANSLATIONS[self.current_lang]["label_save"], command=self.button1_click)
        self.button2 = tk.Button(self.bottom_frame, text=TRANSLATIONS[self.current_lang]["label_clear"], command=self.button2_click)
        self.button1.pack(side="right", padx=4, pady=4)
        self.button2.pack(side="right", padx=4, pady=4)
        self.button3 = tk.Button(self.form_frame, text=TRANSLATIONS[self.current_lang]["label_search"], command=self.button3_click)
        self.button3.place(x=310, y=10, width=60)
        self.button4 = tk.Button(self.form_frame, text=TRANSLATIONS[self.current_lang]["label_next"], command=self.button4_click)
        self.button4.place(x=310, y=42, width=60)
        self.button5 = tk.Button(self.form_frame, text=TRANSLATIONS[self.current_lang]["label_txt"], command=self.paste_to_txt)
        self.button5.place(x=320, y=380, width=50)

        self.button_copy = tk.Button(self.form_frame, text=TRANSLATIONS[self.current_lang]["label_copy"], command=self.copy_to_clipboard)
        self.button_copy.place(x=300, y=412, width=70)

    def create_list_widgets(self):
        cols = ("cliente", "n_aviso", "bien", "averia")
        self.tree = ttk.Treeview(self.list_frame, columns=cols, show="headings")
        headings = [
            ("cliente", TRANSLATIONS[self.current_lang]["label_client_col"]),
            ("n_aviso", TRANSLATIONS[self.current_lang]["label_ticket_col"]),
            ("bien", TRANSLATIONS[self.current_lang]["label_asset_col"]),
            ("averia", TRANSLATIONS[self.current_lang]["label_problem_col"]),
        ]
        for col, text in headings:
            self.tree.heading(col, text=text, anchor="w")
            if col == "cliente":
                self.tree.column(col, width=100, minwidth=80, stretch=True, anchor="w")
            elif col == "averia":
                self.tree.column(col, width=250, minwidth=200, stretch=True, anchor="w")
            elif col == "n_aviso":
                self.tree.column(col, width=90, minwidth=80, stretch=True, anchor="w")
            else:
                self.tree.column(col, width=110, minwidth=90, stretch=True, anchor="w")
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        self.tree.bind("<Double-1>", self.on_tree_double_click)

        self.load_button = tk.Button(self.list_frame, text=TRANSLATIONS[self.current_lang]["label_refresh"], command=self.load_list)
        self.load_button.pack(side="bottom", pady=(6, 2))

        self.delete_button = tk.Button(self.list_frame, text=TRANSLATIONS[self.current_lang]["label_delete"], command=self.delete_selected_record)
        self.delete_button.pack(side="bottom", pady=(0, 6))

    def apply_language(self, language):
        self.current_lang = language
        texts = TRANSLATIONS[language]
        self.title(f"{texts['app_title']} - v{APP_VERSION}")
        self.notebook.tab(self.form_frame, text=texts["tab_form"])
        self.notebook.tab(self.list_frame, text=texts["tab_list"])

        for key, text_key in [
            ("client", "label_client"),
            ("address", "label_address"),
            ("ticket", "label_ticket"),
            ("contact", "label_contact"),
            ("phone", "label_phone"),
            ("asset", "label_asset"),
            ("problem", "label_problem"),
            ("note", "label_note"),
        ]:
            if key in self.labels:
                self.labels[key]["text"] = texts[text_key]

        self.checkBox1["text"] = texts["label_solved"]
        self.checkBox2["text"] = texts["label_serial"]
        self.checkBox3["text"] = texts["label_no_invoice"]
        self.groupBox1["text"] = texts["label_assistance"]
        self.radioButton3["text"] = texts["radio_lab"]
        self.radioButton1["text"] = texts["radio_remote"]
        self.radioButton2["text"] = texts["radio_client"]

        self.button1["text"] = texts["label_save"]
        self.button2["text"] = texts["label_clear"]
        self.button3["text"] = texts["label_search"]
        self.button4["text"] = texts["label_next"]
        self.button5["text"] = texts["label_txt"]
        self.button_copy["text"] = texts["label_copy"]
        self.load_button["text"] = texts["label_refresh"]
        self.delete_button["text"] = texts["label_delete"]
        self.help_button["text"] = texts["label_help"]

        for col, text in [
            ("cliente", texts["label_client_col"]),
            ("n_aviso", texts["label_ticket_col"]),
            ("bien", texts["label_asset_col"]),
            ("averia", texts["label_problem_col"]),
        ]:
            self.tree.heading(col, text=text, anchor="w")
            self.tree.column(col, anchor="w")

        self.language_var.set(self.lang_labels.get(language, "Español"))

    def get_form_data(self):
        texts = TRANSLATIONS[self.current_lang]
        sep = "-----"
        header = [
            f"{texts['clipboard_prefix_client']}: {self.textBox1.get()}",
            f"{texts['clipboard_prefix_address']}: {self.textBox2.get()}",
            f"{texts['clipboard_prefix_ticket']}: {self.textBox3.get()}",
            f"{texts['clipboard_prefix_contact']}: {self.textBox4.get()}",
            f"{texts['clipboard_prefix_phone']}: {self.textBox5.get()}",
            f"{texts['clipboard_prefix_assistance']}: {self.radio_var.get()}",
        ]
        if self.checkBox2_var.get():
            header.append(f"SN: {self.textBox6.get()}")
        header.append(f"{texts['clipboard_prefix_asset']}: {self.textBox7.get()}")

        averia_section = [f"{texts['clipboard_prefix_problem']}: {self.richTextBox1.get('1.0', tk.END).strip()}"]
        if self.checkBox1_var.get():
            averia_section.append(f"{texts['clipboard_prefix_solution']}: {self.richTextBox2.get('1.0', tk.END).strip()}")

        footer = [
            f"{texts['clipboard_prefix_note']}: {self.textBox8.get()}",
            f"{texts['clipboard_prefix_no_invoice']}: {texts['msg_no_invoice_yes'] if self.checkBox3_var.get() else texts['msg_no_invoice_no']}",
        ]
        parts = [sep, "\n".join(header), sep, "\n".join(averia_section), sep, "\n".join(footer)]
        return "\n".join(parts)

    def load_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT id, cliente, n_aviso, telefono, bien, averia, nota FROM avisos ORDER BY id DESC")
        rows = c.fetchall()
        conn.close()
        for row in rows:
            rid = row[0]
            values = (row[1], row[2], row[4], row[5])
            self.tree.insert("", "end", iid=str(rid), values=values)

    def on_tree_double_click(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        try:
            record_id = int(selected[0])
        except ValueError:
            return
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT * FROM avisos WHERE id = ?", (record_id,))
        record = c.fetchone()
        conn.close()
        if record:
            self.notebook.select(self.form_frame)
            self.display_record(record)

    def button1_click(self):
        if not any(
            [
                self.textBox1.get().strip(),
                self.textBox2.get().strip(),
                self.textBox3.get().strip(),
                self.textBox4.get().strip(),
                self.textBox5.get().strip(),
                self.textBox6.get().strip(),
                self.textBox7.get().strip(),
                self.richTextBox1.get("1.0", tk.END).strip(),
                self.richTextBox2.get("1.0", tk.END).strip(),
                self.textBox8.get().strip(),
            ]
        ):
            messagebox.showinfo(TRANSLATIONS[self.current_lang]["msg_search_title"], TRANSLATIONS[self.current_lang]["msg_empty_record"])
            return

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT id FROM avisos WHERE cliente = ? AND n_aviso = ?", (self.textBox1.get(), self.textBox3.get()))
        existing_record = c.fetchone()

        if existing_record:
            c.execute(
                """
                UPDATE avisos
                SET direccion = ?, per_cto = ?, telefono = ?, sn = ?, bien = ?, averia = ?, solucion = ?, asistencia = ?, nota = ?, no_fact = ?
                WHERE id = ?
                """,
                (
                    self.textBox2.get(),
                    self.textBox4.get(),
                    self.textBox5.get(),
                    self.textBox6.get() if self.checkBox2_var.get() else "",
                    self.textBox7.get(),
                    self.richTextBox1.get("1.0", tk.END).strip(),
                    self.richTextBox2.get("1.0", tk.END).strip() if self.checkBox1_var.get() else "",
                    self.radio_var.get(),
                    self.textBox8.get(),
                    1 if self.checkBox3_var.get() else 0,
                    existing_record[0],
                ),
            )
            messagebox.showinfo(TRANSLATIONS[self.current_lang]["msg_search_title"], TRANSLATIONS[self.current_lang]["msg_updated"])
        else:
            c.execute(
                """
                INSERT INTO avisos (cliente, direccion, n_aviso, per_cto, telefono, sn, bien, averia, solucion, asistencia, nota, no_fact)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    self.textBox1.get(),
                    self.textBox2.get(),
                    self.textBox3.get(),
                    self.textBox4.get(),
                    self.textBox5.get(),
                    self.textBox6.get() if self.checkBox2_var.get() else "",
                    self.textBox7.get(),
                    self.richTextBox1.get("1.0", tk.END).strip(),
                    self.richTextBox2.get("1.0", tk.END).strip() if self.checkBox1_var.get() else "",
                    self.radio_var.get(),
                    self.textBox8.get(),
                    1 if self.checkBox3_var.get() else 0,
                ),
            )
            messagebox.showinfo(TRANSLATIONS[self.current_lang]["msg_search_title"], TRANSLATIONS[self.current_lang]["msg_saved"])

        conn.commit(); conn.close()
        self.clipboard_clear(); self.clipboard_append(self.get_form_data())

    def delete_selected_record(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo(TRANSLATIONS[self.current_lang]["msg_search_title"], TRANSLATIONS[self.current_lang]["msg_select_record"])
            return

        record_id = int(selected[0])
        if messagebox.askyesno(TRANSLATIONS[self.current_lang]["msg_search_title"], TRANSLATIONS[self.current_lang]["msg_delete_confirm"]):
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("DELETE FROM avisos WHERE id = ?", (record_id,))
            conn.commit()
            conn.close()
            self.tree.delete(selected[0])
            self.search_results = []
            self.current_result_index = 0
            messagebox.showinfo(TRANSLATIONS[self.current_lang]["msg_search_title"], TRANSLATIONS[self.current_lang]["msg_delete_ok"])

    def button2_click(self):
        self.textBox1.delete(0, tk.END)
        self.textBox2.delete(0, tk.END)
        self.textBox3.delete(0, tk.END)
        self.textBox4.delete(0, tk.END)
        self.textBox5.delete(0, tk.END)
        self.textBox6.delete(0, tk.END)
        self.textBox7.delete(0, tk.END)
        self.textBox8.delete(0, tk.END)
        self.richTextBox1.delete("1.0", tk.END)
        self.richTextBox2.delete("1.0", tk.END)
        self.checkBox1_var.set(False)
        self.checkBox2_var.set(False)
        self.checkBox3_var.set(False)
        self.radio_var.set("Lab")
        self.search_results = []
        self.current_result_index = 0

    def button3_click(self):
        cliente = self.textBox1.get().strip()
        if not cliente:
            messagebox.showinfo(TRANSLATIONS[self.current_lang]["msg_search_title"], TRANSLATIONS[self.current_lang]["msg_no_client"])
            return

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT * FROM avisos WHERE cliente LIKE ? ORDER BY id ASC", (f"%{cliente}%",))
        self.search_results = c.fetchall()
        conn.close()

        if self.search_results:
            self.current_result_index = 0
            self.display_record(self.search_results[self.current_result_index])
        else:
            messagebox.showinfo(TRANSLATIONS[self.current_lang]["msg_search_title"], TRANSLATIONS[self.current_lang]["msg_not_found"])

    def button4_click(self):
        if not self.search_results:
            messagebox.showinfo(TRANSLATIONS[self.current_lang]["msg_search_title"], TRANSLATIONS[self.current_lang]["msg_first_search"])
            return

        if self.current_result_index < len(self.search_results) - 1:
            self.current_result_index += 1
            self.display_record(self.search_results[self.current_result_index])
        else:
            messagebox.showinfo(TRANSLATIONS[self.current_lang]["msg_search_title"], TRANSLATIONS[self.current_lang]["msg_no_more"])

    def display_record(self, record):
        self.textBox1.delete(0, tk.END)
        self.textBox1.insert(0, record[1])
        self.textBox2.delete(0, tk.END)
        self.textBox2.insert(0, record[2])
        self.textBox3.delete(0, tk.END)
        self.textBox3.insert(0, record[3])
        self.textBox4.delete(0, tk.END)
        self.textBox4.insert(0, record[4])
        self.textBox5.delete(0, tk.END)
        self.textBox5.insert(0, record[5])
        self.textBox6.delete(0, tk.END)
        self.textBox6.insert(0, record[6])
        self.textBox7.delete(0, tk.END)
        self.textBox7.insert(0, record[7])
        self.richTextBox1.delete("1.0", tk.END)
        self.richTextBox1.insert("1.0", record[8])
        self.richTextBox2.delete("1.0", tk.END)
        self.richTextBox2.insert("1.0", record[9])
        self.radio_var.set(record[10])
        self.textBox8.delete(0, tk.END)
        self.textBox8.insert(0, record[11])

        self.checkBox2_var.set(bool((record[6] or "").strip()))
        self.checkBox1_var.set(bool((record[9] or "").strip()))
        self.checkBox3_var.set(bool(record[12]))

        self.clipboard_clear(); self.clipboard_append(self.get_form_data())

    def copy_to_clipboard(self):
        payload = self.get_form_data()
        self.clipboard_clear()
        self.clipboard_append(payload)
        messagebox.showinfo(TRANSLATIONS[self.current_lang]["label_copy"], TRANSLATIONS[self.current_lang]["msg_copy_ok"])

    def paste_to_txt(self):
        texto = self.clipboard_get()
        archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivo de texto", "*.txt"), ("Text file", "*.txt")])
        if archivo:
            with open(archivo, "w", encoding="utf-8") as f:
                f.write(texto)
            messagebox.showinfo(TRANSLATIONS[self.current_lang]["label_txt"], TRANSLATIONS[self.current_lang]["msg_txt_saved"])


if __name__ == "__main__":
    init_db()
    app = EllinboardT()
    app.mainloop()
