# pdf_generator.py
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.lib.utils import ImageReader
import matplotlib.pyplot as plt
import io

# ================= GPA Letter Conversion =================
def gpa_to_letter(gpa):
    if gpa >= 4.0:
        return "A+"
    elif gpa >= 3.6:
        return "A"
    elif gpa >= 3.2:
        return "B+"
    elif gpa >= 2.8:
        return "B"
    elif gpa >= 2.4:
        return "C+"
    elif gpa >= 2.0:
        return "C"
    else:
        return "F"

# ================= PDF Generator with Chart =================
def generate_marksheet_pdf(student, subjects, marks, output_file):
    """
    Generates a PDF marksheet for a single student with GPA reference and marks bar chart.
    
    student: dict with keys 'Name', 'Roll', 'Grade', 'Section'
    subjects: list of subject names
    marks: list of corresponding marks
    output_file: PDF output path
    """

    # School info
    school_name = "Kathmandu National School"
    school_address = "Surya Bikram Gyawali Marg, Kathmandu, Nepal"

    total_marks = sum(marks)
    percentage = round((total_marks / (len(subjects)*100))*100, 2)

    # GPA calculation
    if percentage >= 90:
        gpa = 4.0
    elif percentage >= 80:
        gpa = 3.6
    elif percentage >= 70:
        gpa = 3.2
    elif percentage >= 60:
        gpa = 2.8
    elif percentage >= 50:
        gpa = 2.4
    elif percentage >= 40:
        gpa = 2.0
    else:
        gpa = 0.0

    gpa_letter = gpa_to_letter(gpa)

    # ================= PDF =================
    c = canvas.Canvas(output_file, pagesize=letter)
    width, height = letter

    # Background
    c.setFillColor(colors.white)
    c.rect(0, 0, width, height, fill=True, stroke=False)

    # School Header
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, height-50, school_name)
    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, height-70, school_address)

    # Student Details
    c.setFont("Helvetica-Bold", 14)
    y_position = height - 110
    c.drawString(50, y_position, f"Student Name: {student['Name']}")
    c.drawString(350, y_position, f"Roll No: {student['Roll']}")
    y_position -= 20
    c.drawString(50, y_position, f"Grade: {student['Grade']}")
    c.drawString(350, y_position, f"Section: {student['Section']}")

    # ================= Main Marks Table =================
    table_data = [["Subject", "Marks"]]
    for s, m in zip(subjects, marks):
        table_data.append([s, str(m)])
    table_data.append(["Total", f"{total_marks} / {len(subjects)*100}"])
    table_data.append(["Percentage", f"{percentage}%"])
    table_data.append(["GPA", f"{gpa} ({gpa_letter})"])

    table = Table(table_data, colWidths=[250, 120])

    # Colors
    header_bg = colors.HexColor("#FFD966")  # Golden header
    footer_bg = colors.HexColor("#FFF4B2")  # Light yellow footer

    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), header_bg),
        ('BACKGROUND', (0,-3), (-1,-1), footer_bg),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTNAME', (0,-3), (-1,-1), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))

    table_width, table_height = table.wrap(0,0)
    x = (width - table_width)/2
    y = y_position - 40
    table.drawOn(c, x, y - table_height)

    # ================= GPA Reference Table =================
    ref_title_y = y - table_height - 40
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width/2, ref_title_y, "GPA Reference")

    ref_data = [
        ["GPA Range", "Grade"],
        ["4.0", "A+"],
        ["3.6 – 3.9", "A"],
        ["3.2 – 3.5", "B+"],
        ["2.8 – 3.1", "B"],
        ["2.4 – 2.7", "C+"],
        ["2.0 – 2.3", "C"],
        ["Below 2.0", "F"],
    ]

    ref_table = Table(ref_data, colWidths=[150,150])
    ref_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), header_bg),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))

    ref_width, ref_height = ref_table.wrap(0,0)
    ref_x = (width - ref_width)/2
    ref_y = ref_title_y - 20 - ref_height
    ref_table.drawOn(c, ref_x, ref_y)

    # ================= Marks Bar Chart =================
    plt.figure(figsize=(5,2.5))
    bars = plt.bar(subjects, marks, color="#4CAF50")
    plt.ylim(0, 100)
    plt.ylabel("Marks")
    plt.title("Marks Distribution")
    for bar, mark in zip(bars, marks):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, str(mark),
                 ha='center', va='bottom', fontsize=9)
    plt.tight_layout()

    # Save chart to memory
    buf = io.BytesIO()
    plt.savefig(buf, format='PNG', dpi=150)
    plt.close()
    buf.seek(0)

    # Embed chart in PDF
    chart_height = 200
    c.drawImage(ImageReader(buf), x, ref_y - chart_height - 20, width=table_width, height=chart_height)

    # Save PDF
    c.save()