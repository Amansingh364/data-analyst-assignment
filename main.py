from flask import Flask, request, send_file, render_template
import os
import subprocess

app = Flask(__name__)

# Configuration for upload and report folders
UPLOAD_FOLDER = 'data'
REPORT_FOLDER = 'reports'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def save_uploaded_file(file):
    """Save uploaded CSV to data folder."""
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'data_dump.csv')
    file.save(filepath)
    return filepath


def run_report_generator():
    """Run the script that generates the Excel report."""
    subprocess.run(['python', 'generate_report.py'])


def get_latest_report_path():
    """Find the most recently created Excel report."""
    report_files = sorted(os.listdir(REPORT_FOLDER))
    latest_file = report_files[-1] if report_files else None
    if not latest_file:
        raise FileNotFoundError("No report file found.")
    return os.path.abspath(os.path.join(REPORT_FOLDER, latest_file))


@app.route('/')
def index():
    """Render the upload page."""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload, generate report, and return download."""
    file = request.files.get('file')
    if not file:
        return "No file uploaded!", 400

    save_uploaded_file(file)
    run_report_generator()
    report_path = get_latest_report_path()
    return send_file(report_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
