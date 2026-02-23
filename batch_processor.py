import pandas as pd
import os
from pdf_generator import generate_marksheet_pdf

def batch_generate_marksheets(data_file, output_folder):
    # Load data based on file extension
    if data_file.endswith('.csv'):
        df = pd.read_csv(data_file)
    else:
        df = pd.read_excel(data_file)

    # Required columns check
    required = ['Name', 'Roll', 'Grade']
    if not all(col in df.columns for col in required):
        raise ValueError(f"File must contain columns: {', '.join(required)}")

    # Identify subject columns (all columns that aren't Name, Roll, or Grade)
    subject_cols = [col for col in df.columns if col not in required]

    for index, row in df.iterrows():
        student = {
            "Name": str(row['Name']),
            "Roll": str(row['Roll']),
            "Grade": str(row['Grade'])
        }
        
        subjects = []
        marks = []
        
        for col in subject_cols:
            if pd.notna(row[col]): # Only add if there is a mark
                subjects.append(col)
                marks.append(int(row[col]))

        filename = f"{student['Name'].replace(' ', '_')}_Marksheet.pdf"
        output_path = os.path.join(output_folder, filename)
        
        generate_marksheet_pdf(student, subjects, marks, output_path)