from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch

def get_grade_and_gpa(mark):
    """Reference logic for grades and points"""
    if mark >= 90: return "A+", 4.0
    elif mark >= 80: return "A", 3.6
    elif mark >= 70: return "B+", 3.2
    elif mark >= 60: return "B", 2.8
    elif mark >= 50: return "C+", 2.4
    elif mark >= 40: return "C", 2.0
    else: return "D", 1.0

def generate_marksheet_pdf(student_data, subjects, marks, output_path):
    doc = SimpleDocTemplate(output_path, pagesize=A4, topMargin=0.5*inch)
    elements = []
    styles = getSampleStyleSheet()

    # --- Header ---
    school_style = ParagraphStyle('Sch', alignment=1, fontSize=22, fontName="Helvetica-Bold", textColor=colors.HexColor("#2C3E50"))
    report_style = ParagraphStyle('Rep', alignment=1, fontSize=14, spaceAfter=20, fontName="Helvetica-Bold", textColor=colors.HexColor("#7F8C8D"))
    
    elements.append(Paragraph("KATHMANDU NATIONAL SCHOOL", school_style))
    elements.append(Paragraph("PROGRESS REPORT", report_style))

    # --- Student Info ---
    info_data = [[f"Student Name: {student_data['Name']}", f"Roll No: {student_data['Roll']}"],
                 [f"Grade: {student_data['Grade']}", ""]]
    info_table = Table(info_data, colWidths=[4*inch, 2.5*inch])
    info_table.setStyle(TableStyle([('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'), ('BOTTOMPADDING', (0,0), (-1,-1), 12)]))
    elements.append(info_table)
    elements.append(Spacer(1, 0.2 * inch))

    # --- Main Marks Table ---
    table_data = [["Subject", "Full Marks", "Marks Obtained"]]
    total_marks, total_gp = 0, 0
    
    for sub, mark in zip(subjects, marks):
        table_data.append([sub, "100", str(mark)])
        total_marks += mark
        _, gp = get_grade_and_gpa(mark)
        total_gp += gp

    avg_marks = total_marks / len(marks)
    final_gpa = total_gp / len(marks)
    final_letter, _ = get_grade_and_gpa(avg_marks)

    # Adding Summary Rows with Spanning (Merging Cells)
    # Total Row
    table_data.append(["TOTAL MARKS", "", str(total_marks)])
    # Percentage Row (Center Aligned via Spanning)
    table_data.append(["PERCENTAGE OBTAINED", "", f"{avg_marks:.2f}%"])
    # GPA Row (Center Aligned via Spanning)
    table_data.append(["FINAL GPA (GRADE)", "", f"{final_gpa:.2f} ({final_letter})"])

    main_table = Table(table_data, colWidths=[3.5*inch, 1.5*inch, 1.5*inch])
    
    # Styling with Span: (column_start, row_start), (column_end, row_end)
    summary_idx = len(table_data) - 3
    main_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2C3E50")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, summary_idx), (-1, -1), colors.HexColor("#ECF0F1")),
        ('FONTNAME', (0, summary_idx), (-1, -1), 'Helvetica-Bold'),
        # Merge the "Subject" and "Full Marks" columns for the last three rows
        ('SPAN', (0, summary_idx), (1, summary_idx)),         # Total span
        ('SPAN', (0, summary_idx+1), (1, summary_idx+1)),     # Percentage span
        ('SPAN', (0, summary_idx+2), (1, summary_idx+2)),     # GPA span
    ])
    
    main_table.setStyle(main_style)
    elements.append(main_table)
    elements.append(Spacer(1, 0.4 * inch))

    # --- Reference Grading Table ---
    elements.append(Paragraph("GRADING SYSTEM REFERENCE", ParagraphStyle('RefTitle', fontSize=10, fontName="Helvetica-Bold", spaceAfter=5)))
    
    ref_data = [
        ["Interval", "Grade", "Grade Point", "Description"],
        ["90% - 100%", "A+", "4.0", "Outstanding"],
        ["80% - 89%", "A", "3.6", "Excellent"],
        ["70% - 79%", "B+", "3.2", "Very Good"],
        ["60% - 69%", "B", "2.8", "Good"],
        ["50% - 59%", "C+", "2.4", "Satisfactory"],
        ["40% - 49%", "C", "2.0", "Acceptable"],
        ["Below 40%", "D", "1.0", "Insufficient"]
    ]
    
    ref_table = Table(ref_data, colWidths=[1.5*inch, 1*inch, 1.2*inch, 1.8*inch])
    ref_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#EEEEEE")),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ]))
    elements.append(ref_table)
    elements.append(Spacer(1, 0.6 * inch))

    # --- Signatures ---
    sig_data = [["____________________", "____________________"], ["Class Teacher", "Principal"]]
    sig_table = Table(sig_data, colWidths=[3.25*inch, 3.25*inch])
    sig_table.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'), ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold')]))
    elements.append(sig_table)

    doc.build(elements)