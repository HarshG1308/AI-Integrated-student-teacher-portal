import os
from flask import Flask, redirect, render_template, request, url_for, flash, session
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import google.generativeai as genai
import PIL
import pytesseract

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = "your_secret_key"

# Set up the Gemini API Key
API_KEY = "AIzaSyAZWY1WQLlud8xq0HElWDu04AqW3oUwilc"
genai.configure(api_key=API_KEY)

# Set up the folder for file uploads
upload_folder = 'uploads'
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

app.config['UPLOAD_FOLDER'] = upload_folder
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'pdf', 'txt'}

# Users data (for demonstration purposes)
users = {
    "student": {"username": "student", "password": generate_password_hash("student123"), "role": "student"},
    "teacher": {"username": "teacher", "password": generate_password_hash("teacher123"), "role": "teacher"}
}

# Helper function to check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Home Route
@app.route('/')
def home():
    return render_template('index.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)

        if user and check_password_hash(user['password'], password):
            session['username'] = username
            session['role'] = user['role']
            if user['role'] == 'teacher':
                return redirect(url_for('teacher_dashboard'))
            else:
                return redirect(url_for('student_dashboard'))
        else:
            flash("Invalid credentials, please try again.")

    return render_template('login.html')

# Logout Route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# Dashboard Routes (Role-Based)
@app.route('/student_dashboard')
def student_dashboard():
    if 'role' in session and session['role'] == 'student':
        return render_template('student_dashboard.html')
    return redirect(url_for('login'))

@app.route('/teacher_dashboard')
def teacher_dashboard():
    if 'role' in session and session['role'] == 'teacher':
        return render_template('teacher_dashboard.html')
    return redirect(url_for('login'))

# Assignments and Tests Routes (Teacher Only)
@app.route('/assignments')
def assignments():
    if 'role' in session and session['role'] == 'teacher':
        return render_template('assignments.html')
    return redirect(url_for('login'))

@app.route('/tests')
def tests():
    if 'role' in session and session['role'] == 'teacher':
        return render_template('tests.html')
    return redirect(url_for('login'))

# AI Tools Route (Available to both Student and Teacher)
@app.route('/ai-tools')
def ai_tools():
    return render_template('ai-tools.html')

# Upload Assignment (Teacher Only)
@app.route('/teacher/upload-assignment', methods=['GET', 'POST'])
def upload_assignment():
    if 'role' in session and session['role'] == 'teacher':
        if request.method == 'POST':
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'assignments', filename)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                file.save(file_path)
                flash("Assignment uploaded successfully!")
                return redirect(url_for('teacher_dashboard'))
        return render_template('upload_assignment.html')
    return redirect(url_for('login'))

# Upload Test (Teacher Only)
@app.route('/teacher/upload-test', methods=['GET', 'POST'])
def upload_test():
    if 'role' in session and session['role'] == 'teacher':
        if request.method == 'POST':
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'tests', filename)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                file.save(file_path)
                flash("Test uploaded successfully!")
                return redirect(url_for('teacher_dashboard'))
        return render_template('upload_test.html')
    return redirect(url_for('login'))

# AI Tools: Document Summarizer
@app.route('/ai-tools/document-summarizer', methods=['GET', 'POST'])
def document_summarizer():
    summary = None
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content([f"Summarize the following text: {text}"])
                summary = response.text
            except Exception as e:
                flash(f"Error during summarization: {e}")
    return render_template('document-summarizer.html', summary=summary)

# AI Tools: Image to Text
@app.route('/ai-tools/image-to-text', methods=['GET', 'POST'])
def image_to_text():
    extracted_text = None
    if request.method == 'POST':
        image = request.files['image']
        if image and allowed_file(image.filename):
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image.filename))
            image.save(image_path)
            img = PIL.Image.open(image_path)
            extracted_text = pytesseract.image_to_string(img)
    return render_template('image-to-text.html', extracted_text=extracted_text)

# AI Tools: Query Generator
@app.route('/ai-tools/query-generator', methods=['GET', 'POST'])
def query_generator():
    questions = None
    if request.method == 'POST':
        text = request.form['text']
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content([f"Generate questions: {text}"])
            questions = response.text.split('\n')
        except Exception as e:
            flash(f"Error during query generation: {e}")
    return render_template('query-generator.html', questions=questions)

# AI Tools: Translator
@app.route('/ai-tools/translator', methods=['GET', 'POST'])
def translator():
    translated_text = None
    if request.method == 'POST':
        text = request.form['text']
        target_language = request.form['target_language']
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content([f"Translate to {target_language}: {text}"])
            translated_text = response.text
        except Exception as e:
            flash(f"Error during translation: {e}")
    return render_template('translator.html', translated_text=translated_text)

if __name__ == "__main__":
    app.run(debug=True)
