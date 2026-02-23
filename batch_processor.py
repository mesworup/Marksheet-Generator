# batch_processor.py
import pandas as pd
import os
from pdf_generator import generate_marksheet_pdf

def batch_generate_marksheets(file_path, output_folder):
    df = pd.read_excel(file_path) if file_path.endswith(".xlsx") else pd.read_csv(file_path)
    subjects = [col for col in df.columns if col not in ["Name","Roll","Grade","Section"]]

    for idx, row in df.iterrows():
        student = row[["Name","Roll","Grade","Section"]].to_dict()
        marks = [int(row[s]) for s in subjects]
        output_file = os.path.join(output_folder, f"{student['Name']}_{student['Roll']}.pdf")
        generate_marksheet_pdf(student, subjects, marks, output_file)