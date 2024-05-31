from flask import Flask, request, jsonify
from flask_cors import CORS
import fitz  # PyMuPDF
import docx
from extract_questions import extract_questions_from_text
from models import Question

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file.filename.endswith('.pdf'):
        text = extract_text_from_pdf(file)
    elif file.filename.endswith('.docx'):
        text = extract_text_from_docx(file)
    else:
        return jsonify({'error': 'Unsupported file type'}), 400

    questions = extract_questions_from_text(text)
    for question in questions:
        Question.insert_question(question)
    
    return jsonify({'message': 'File processed successfully', 'questions': questions})

def extract_text_from_pdf(file):
    pdf_document = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    return text

@app.route('/questions', methods=['GET'])
def get_questions():
    questions = Question.get_all_questions()
    for question in questions:
        question['_id'] = str(question['_id'])
    return jsonify(questions)

@app.route('/modify_question', methods=['POST'])
def modify_question():
    question_id = request.json['_id']
    updated_data = request.json
    Question.update_question(question_id, updated_data)
    return jsonify({'message': 'Question updated successfully'})

@app.route('/delete_question', methods=['POST'])
def delete_question():
    question_id = request.json['id']
    Question.delete_question(question_id)
    return jsonify({'message': 'Question deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
