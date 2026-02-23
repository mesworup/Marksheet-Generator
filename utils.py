# utils.py
import matplotlib.pyplot as plt
import os

def generate_marks_chart(subjects, marks, output_file="marks_chart.png"):
    plt.figure(figsize=(4,2))
    plt.bar(subjects, marks, color="#2e7d32")
    plt.ylabel("Marks")
    plt.title("Marks Distribution")
    plt.savefig(output_file, bbox_inches='tight')
    plt.close()
    return output_file