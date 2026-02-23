import os
import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Custom Modules
from pdf_generator import generate_marksheet_pdf
from batch_processor import batch_generate_marksheets

class MarksheetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Marksheet Generation System v1.0")
        
        # Increased window height to 850 to ensure visibility on most monitors
        self.root.geometry("1000x850")
        
        self.subject_entries = []
        self.mark_entries = []
        
        self._build_ui()

    def _build_ui(self):
        # Main Container
        self.main_container = ttk.Frame(self.root, padding=20)
        self.main_container.pack(fill=BOTH, expand=YES)

        # --- Header Section ---
        header_frame = ttk.Frame(self.main_container)
        header_frame.pack(fill=X, pady=(0, 10))
        
        ttk.Label(header_frame, text="🎓 ABC School", 
                  font=("Segoe UI", 24, "bold"), bootstyle=PRIMARY).pack()
        
        # Added random address below school name
        ttk.Label(header_frame, text="123 Education Way, Ward No. 4, Kathmandu, Nepal", 
                  font=("Segoe UI", 10), bootstyle=SECONDARY).pack()

        ttk.Label(header_frame, text="Official Academic Reporting Portal", 
                  font=("Segoe UI", 11), bootstyle=SECONDARY).pack()

        ttk.Separator(self.main_container, bootstyle=SECONDARY).pack(fill=X, pady=10)

        # --- Student Information Section ---
        # Reduced ipady from 15 to 10 to save vertical space
        student_container = ttk.Frame(self.main_container, bootstyle=LIGHT)
        student_container.pack(fill=X, pady=5, ipadx=15, ipady=10)
        
        ttk.Label(student_container, text="STUDENT INFORMATION", font=("Segoe UI", 10, "bold"), bootstyle=INFO).grid(row=0, column=0, columnspan=4, sticky=W, padx=10, pady=(0,5))

        ttk.Label(student_container, text="Student Name:").grid(row=1, column=0, sticky=E, padx=5, pady=5)
        self.name_entry = ttk.Entry(student_container)
        self.name_entry.grid(row=1, column=1, columnspan=3, sticky=EW, padx=5, pady=5)

        ttk.Label(student_container, text="Roll No:").grid(row=2, column=0, sticky=E, padx=5, pady=5)
        self.roll_entry = ttk.Entry(student_container)
        self.roll_entry.grid(row=2, column=1, sticky=EW, padx=5, pady=5)

        ttk.Label(student_container, text="Grade/Class:").grid(row=2, column=2, sticky=E, padx=5, pady=5)
        self.grade_entry = ttk.Entry(student_container)
        self.grade_entry.grid(row=2, column=3, sticky=EW, padx=5, pady=5)

        student_container.columnconfigure((1, 3), weight=1)

        # --- Academic Record Section ---
        self.academic_container = ttk.Frame(self.main_container, bootstyle=LIGHT)
        self.academic_container.pack(fill=BOTH, expand=YES, pady=5, ipadx=15, ipady=10)

        ttk.Label(self.academic_container, text="SUBJECT-WISE ASSESSMENT", font=("Segoe UI", 10, "bold"), bootstyle=INFO).grid(row=0, column=0, columnspan=2, sticky=W, padx=10, pady=(0,5))

        ttk.Label(self.academic_container, text="Subject Name", font=("Segoe UI", 9, "bold")).grid(row=1, column=0, padx=5, pady=2, sticky=W)
        ttk.Label(self.academic_container, text="Marks", font=("Segoe UI", 9, "bold")).grid(row=1, column=1, padx=5, pady=2, sticky=W)

        for _ in range(5):
            self.add_subject_row()

        # Dynamic Row Controls
        controls_frame = ttk.Frame(self.academic_container)
        controls_frame.grid(row=999, column=0, columnspan=2, pady=10, sticky=W)
        
        ttk.Button(controls_frame, text="➕ Add Subject", bootstyle=SUCCESS, command=self.add_subject_row).pack(side=LEFT, padx=(5, 10))
        ttk.Button(controls_frame, text="➖ Remove Last", bootstyle=DANGER, command=self.remove_subject_row).pack(side=LEFT)

        # --- Action Buttons ---
        # Positioned at the bottom of the container
        action_frame = ttk.Frame(self.main_container)
        action_frame.pack(fill=X, pady=15)

        ttk.Button(action_frame, text="💾 Generate PDF", bootstyle=PRIMARY, width=20, command=self.generate_single).pack(side=LEFT, padx=(0, 15))
        ttk.Button(action_frame, text="📊 Batch Import", bootstyle=SECONDARY, width=20, command=self.generate_batch).pack(side=LEFT)

    def add_subject_row(self):
        row_index = len(self.subject_entries) + 2  
        s = ttk.Entry(self.academic_container, width=40)
        s.grid(row=row_index, column=0, padx=5, pady=3, sticky=W)
        m = ttk.Entry(self.academic_container, width=15)
        m.grid(row=row_index, column=1, padx=5, pady=3, sticky=W)
        self.subject_entries.append(s)
        self.mark_entries.append(m)

    def remove_subject_row(self):
        if len(self.subject_entries) > 1:
            self.subject_entries[-1].destroy()
            self.mark_entries[-1].destroy()
            self.subject_entries.pop()
            self.mark_entries.pop()

    def generate_single(self):
        try:
            student = {
                "Name": self.name_entry.get().strip(),
                "Roll": self.roll_entry.get().strip(),
                "Grade": self.grade_entry.get().strip()
            }
            subjects = [s.get().strip() for s, m in zip(self.subject_entries, self.mark_entries) if s.get().strip()]
            marks = [m.get().strip() for s, m in zip(self.subject_entries, self.mark_entries) if s.get().strip()]

            if not student["Name"] or not subjects:
                messagebox.showerror("Error", "Please fill Student Name and at least one Subject.")
                return

            output_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files","*.pdf")])
            if not output_file: return

            generate_marksheet_pdf(student, subjects, [int(m) for m in marks], output_file)
            messagebox.showinfo("Success", "PDF Generated!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {str(e)}")

    def generate_batch(self):
        file_path = filedialog.askopenfilename(filetypes=[("Data files", "*.xlsx *.csv")])
        if not file_path: return
        folder = filedialog.askdirectory()
        if not folder: return
        try:
            batch_generate_marksheets(file_path, folder)
            messagebox.showinfo("Success", "Batch Complete!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app_root = ttk.Window(themename="cosmo")
    app = MarksheetApp(app_root)
    app_root.mainloop()