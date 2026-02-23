# 🎓 Marksheet Generation System

A professional Python-based desktop application designed for schools to automate the creation of student progress reports. Generate high-quality PDFs with GPA calculations, grade distributions, and visual charts in seconds.

## ✨ Features
* **Dual Mode Generation:** Create individual marksheets manually or process hundreds at once using Excel/CSV batch imports.
* **Automated GPA Logic:** Built-in calculation engine for GPA and Letter Grades based on custom percentage intervals.
* **Visual Analytics:** Automatically generates a bar chart for subject-wise performance using Matplotlib.
* **Professional PDF Output:** Beautifully formatted reports featuring school branding, grading keys, and signature placeholders via ReportLab.
* **Modern UI:** A clean, user-friendly interface powered by `ttkbootstrap`.

## 📁 Project Structure
* `main.py`: The entry point and GUI logic.
* `pdf_generator.py`: Handles the PDF layout and table construction.
* `batch_processor.py`: Manages data extraction from .csv and .xlsx files.
* `gpa_calculator.py`: Contains the logic for grade-to-point conversion.
* `utils.py`: Generates performance charts.
* `requirements.txt`: List of necessary Python libraries.

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have Python 3.8+ installed on your system.

### 2. Installation
Clone this repository or download the source code, then install the dependencies:
```bash
pip install -r requirements.txt
```

### 3. Usage
Run the application using:

```bash
python main.py
```

### 4. Batch Import Format
For batch processing, your Excel or CSV file must contain the following headers:

<pre>Name, Roll, Grade
</pre>
Any additional columns will be treated as Subject Names with their corresponding marks.

### 🛠️ Built With
* ttkbootstrap - Modern GUI theming.
* ReportLab - PDF generation engine.
* Pandas - Data manipulation.
* Matplotlib - Performance charting.

## 📸 Screenshots
> *Tip: Replace these placeholders with actual screenshots of your app!*
1. **Main Interface:** `C:\Users\razzs\OneDrive\Documents\Project\Marksheet-Generator\image.png`
2. **Generated Marksheet PDF:** `C:\Users\razzs\OneDrive\Documents\Project\Marksheet-Generator\testpdf.png`





