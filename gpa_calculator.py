# Replace your existing functions with this:

def percentage_to_gpa(percentage):
    if percentage >= 90: return 4.0
    elif percentage >= 80: return 3.6
    elif percentage >= 70: return 3.2
    elif percentage >= 60: return 2.8
    elif percentage >= 50: return 2.4
    elif percentage >= 40: return 2.0
    elif percentage >= 35: return 1.6
    else: return 0.0

def gpa_to_letter(gpa):
    if gpa >= 4.0: return "A+"
    elif gpa >= 3.6: return "A"
    elif gpa >= 3.2: return "B+"
    elif gpa >= 2.8: return "B"
    elif gpa >= 2.4: return "C+"
    elif gpa >= 2.0: return "C"
    elif gpa >= 1.6: return "D"
    else: return "NG"