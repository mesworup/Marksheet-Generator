# main.py
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from pdf_generator import generate_marksheet_pdf
from batch_processor import batch_generate_marksheets

# ================= Subject Row Functions =================
def add_subject_row(frame, s_entries, m_entries):
    row_index = len(s_entries) + 1  # +1 because row 0 is headers
    s = ttk.Entry(frame, width=25)
    s.grid(row=row_index, column=0, padx=5, pady=4, sticky="w")
    m = ttk.Entry(frame, width=10)
    m.grid(row=row_index, column=1, padx=5, pady=4, sticky="w")
    s_entries.append(s)
    m_entries.append(m)

def remove_subject_row(s_entries, m_entries):
    if s_entries:
        s_entries[-1].destroy()
        m_entries[-1].destroy()
        s_entries.pop()
        m_entries.pop()

# ================= GUI =================
root = ttk.Window(themename="flatly")
root.title("Marksheet Generator")
root.geometry("950x750")
root.configure(bg="#EEDC82")  # flaxen background

# Center card frame with white background
card = ttk.Frame(root, padding=25, bootstyle="white")
card.place(relx=0.5, rely=0.5, anchor="center")  # center the card

# Constants
LEFT_MARGIN = 0  # entries inside card centered, so no extra left margin

# School Title
ttk.Label(card, text="Kathmandu National School", font=("Segoe UI", 22, "bold")).grid(
    row=0, column=0, columnspan=4, pady=15
)

# -------- Student Info --------
ttk.Label(card, text="Student Name:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
name_entry = ttk.Entry(card, width=30)
name_entry.grid(row=1, column=1, pady=5, sticky="w")

ttk.Label(card, text="Roll No:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
roll_entry = ttk.Entry(card, width=10)
roll_entry.grid(row=2, column=1, sticky="w")

ttk.Label(card, text="Grade:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
grade_entry = ttk.Entry(card, width=10)
grade_entry.grid(row=3, column=1, sticky="w")

ttk.Label(card, text="Section:").grid(row=3, column=2, sticky="e", padx=5, pady=5)
section_entry = ttk.Entry(card, width=10)
section_entry.grid(row=3, column=3, sticky="w")

# -------- Subjects Table --------
ttk.Label(card, text="Subjects & Marks", font=("Segoe UI", 14, "bold")).grid(
    row=4, column=0, columnspan=4, pady=15
)
subject_frame = ttk.Frame(card, padding=10, bootstyle="light")
subject_frame.grid(row=5, column=0, columnspan=4, pady=5)

# Table headers
ttk.Label(subject_frame, text="Subject", font=("Segoe UI", 12, "bold"), width=25, anchor="center", relief="ridge").grid(
    row=0, column=0, padx=5, pady=1
)
ttk.Label(subject_frame, text="Marks", font=("Segoe UI", 12, "bold"), width=10, anchor="center", relief="ridge").grid(
    row=0, column=1, padx=5, pady=1
)

subject_entries = []
mark_entries = []

# Initial 5 rows
for _ in range(5):
    add_subject_row(subject_frame, subject_entries, mark_entries)

# -------- Add/Remove Buttons --------
button_frame = ttk.Frame(card)
button_frame.grid(row=6, column=0, columnspan=4, pady=10)
ttk.Button(button_frame, text="+ Add Subject", bootstyle=SUCCESS, command=lambda:add_subject_row(subject_frame, subject_entries, mark_entries)).pack(side=LEFT, padx=10)
ttk.Button(button_frame, text="- Remove Subject", bootstyle=DANGER, command=lambda:remove_subject_row(subject_entries, mark_entries)).pack(side=LEFT, padx=10)

# -------- Generate Functions --------
def generate_single_marksheet():
    try:
        student = {
            "Name": name_entry.get().strip(),
            "Roll": roll_entry.get().strip(),
            "Grade": grade_entry.get().strip(),
            "Section": section_entry.get().strip()
        }
        subjects = [s.get().strip() for s in subject_entries]
        marks = [m.get().strip() for m in mark_entries]

        if not all(student.values()):
            messagebox.showerror("Error", "Please fill all student details")
            return
        if any(s == "" for s in subjects):
            messagebox.showerror("Error", "Please fill all subjects")
            return
        if any(not m.isdigit() for m in marks):
            messagebox.showerror("Error", "All marks must be numbers")
            return

        output_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files","*.pdf")])
        if not output_file: return

        marks = [int(m) for m in marks]
        generate_marksheet_pdf(student, subjects, marks, output_file)
        messagebox.showinfo("Success", f"Marksheet generated!\n{output_file}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def generate_batch_marksheets_gui():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files","*.xlsx"), ("CSV files","*.csv")])
    if not file_path: return
    folder = filedialog.askdirectory(title="Select folder to save PDFs")
    if not folder: return
    try:
        batch_generate_marksheets(file_path, folder)
        messagebox.showinfo("Success", f"All marksheets generated in {folder}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# -------- Generate Buttons --------
gen_frame = ttk.Frame(card)
gen_frame.grid(row=7, column=0, columnspan=4, pady=20)
ttk.Button(gen_frame, text="Generate Single Marksheet", bootstyle=PRIMARY, command=generate_single_marksheet).pack(side=LEFT, padx=15)
ttk.Button(gen_frame, text="Batch Generate from Excel/CSV", bootstyle=INFO, command=generate_batch_marksheets_gui).pack(side=LEFT, padx=15)

root.mainloop()