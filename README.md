# Marksheet Generator

[![Python](https://img.shields.io/badge/Python-3.9+-blue)](https://www.python.org/)  
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)  
[![ttkbootstrap](https://img.shields.io/badge/ttkbootstrap-0.7.2-orange)](https://pypi.org/project/ttkbootstrap/)  
[![ReportLab](https://img.shields.io/badge/ReportLab-3.6.12-red)](https://www.reportlab.com/)

A **modern, GUI-based Python application** to generate student marksheets in **PDF format**, complete with **GPA, charts, and batch Excel/CSV import**. Designed for schools and educators, it supports both **single student** and **batch processing**.

---

## Features

- ✅ Modern GUI using **ttkbootstrap**  
- ✅ Dynamic subject entry (add/remove subjects)  
- ✅ PDF marksheets with:
  - School header and logo  
  - Colored table for marks & GPA  
  - GPA reference table  
  - Marks distribution chart  
- ✅ GPA calculation and letter grading  
- ✅ Batch generation via Excel/CSV files  
- ✅ Save PDFs to user-selected folder  
- ✅ Error handling for invalid inputs  

---

## Project Structure


marksheet_app/
├── main.py # GUI entry point
├── pdf_generator.py # PDF generation functions
├── gpa_calculator.py # GPA & grading logic
├── batch_processor.py # Batch Excel/CSV processing
├── utils.py # Helper functions (charts)
├── assets/ # Logos, icons, screenshots
│ └── school_logo.png
├── requirements.txt # Python dependencies
└── README.md


---

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/marksheet_app.git
cd marksheet_app

Create a virtual environment (recommended):

python -m venv venv
# Activate
# Windows
venv\Scripts\activate
# Linux / Mac
source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

requirements.txt includes:

ttkbootstrap
reportlab
matplotlib
pandas
openpyxl
Usage
1️⃣ Single Student Marksheet

Run the GUI:

python main.py

Enter student details: Name, Roll No, Grade, Section.

Enter subjects and marks.

Click "Generate Single Marksheet".

Select output PDF location.

Marksheet is generated with GPA, percentage, and chart.

2️⃣ Batch Generation via Excel/CSV

Prepare an Excel/CSV file with columns:

Name, Roll, Grade, Section, Subject1, Subject2, ...

Run the GUI and click "Batch Generate from Excel/CSV".

Select the Excel/CSV file.

Select a folder to save all PDFs.

All students’ PDFs are generated automatically.

Example CSV:

Name	Roll	Grade	Section	Math	English	Science	Nepali
Roshan Chaudhary	101	10	A	92	88	85	90
Nadish Acharya	102	10	A	85	90	80	88
Screenshots

GUI:

PDF Output:

License

MIT License - see LICENSE

Future Improvements

Add Excel export of results.

Option to email PDF marksheets directly to students.

Add school logo dynamically in PDF.

Add themes for GUI.

Author

Nadish Acharya

Roshan Chaudhary

Sworup Raj Ghatani

Supervisor: Dr. Ashim Khadka

This project is a real-world school project example and is GitHub-ready for portfolios.
