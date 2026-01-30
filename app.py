from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# --- Expanded Database ---
QUESTION_POOL = [
    # PY BASICS
    {"id": 1, "question": "What does HTML stand for?", "options": ["Hyper Text Preprocessor", "Hyper Text Markup Language", "Hyper Text Multiple Language", "Hyper Tool Multi Language"], "answer": 1},
    {"id": 2, "question": "Which language runs in a web browser?", "options": ["Java", "C", "Python", "JavaScript"], "answer": 3},
    {"id": 3, "question": "What does CSS stand for?", "options": ["Central Style Sheets", "Cascading Style Sheets", "Cascading Simple Sheets", "Cars SUVs Sailboats"], "answer": 1},
    {"id": 4, "question": "What year was JavaScript launched?", "options": ["1996", "1995", "1994", "None of the above"], "answer": 1},
    {"id": 5, "question": "Which symbol is used for comments in Python?", "options": ["//", "<!--", "#", "/* */"], "answer": 2},
    {"id": 6, "question": "Which framework is used for backend in this project?", "options": ["Django", "Flask", "FastAPI", "Express"], "answer": 1},
    {"id": 7, "question": "What is the output of: 2 ** 3 in Python?", "options": ["6", "8", "9", "5"], "answer": 1},
    {"id": 8, "question": "How do you create a function in Python?", "options": ["function myFunc():", "def myFunc():", "create myFunc():", "func myFunc():"], "answer": 1},
    {"id": 9, "question": "Which data type is immutable in Python?", "options": ["List", "Dictionary", "Set", "Tuple"], "answer": 3},
    {"id": 10, "question": "Which HTML tag is used for the largest heading?", "options": ["<head>", "<h6>", "<h1>", "<header>"], "answer": 2},
    # GEN KNOWLEDGE & CS
    {"id": 11, "question": "What does CPU stand for?", "options": ["Central Process Unit", "Central Processing Unit", "Computer Personal Unit", "Central Processor Unit"], "answer": 1},
    {"id": 12, "question": "Which company owns GitHub?", "options": ["Google", "Facebook", "Microsoft", "Amazon"], "answer": 2},
    {"id": 13, "question": "What port does Flask run on by default?", "options": ["3000", "8000", "8080", "5000"], "answer": 3},
    {"id": 14, "question": "Which is NOT a valid variable name in Python?", "options": ["my_var", "_var", "2var", "var2"], "answer": 2},
    {"id": 15, "question": "What does API stand for?", "options": ["Application Programming Interface", "Apple Pie Ingredients", "Advanced Peripheral Integration", "Application Process Integration"], "answer": 0}
]

QUESTIONS_PER_GAME = 5

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/questions')
def get_questions():
    # Shuffle and pick random questions for a new game
    # We maintain the list of dictionaries
    current_game_questions = random.sample(QUESTION_POOL, min(len(QUESTION_POOL), QUESTIONS_PER_GAME))
    
    # Send questions without the answer key to frontend
    safe_questions = []
    for q in current_game_questions:
        safe_questions.append({
            "id": q["id"],
            "question": q["question"],
            "options": q["options"]
        })
    return jsonify(safe_questions)

@app.route('/api/check-answer', methods=['POST'])
def check_answer():
    data = request.json
    question_id = data.get('question_id')
    user_answer_index = data.get('answer_index')
    
    # Find question in the Full Pool
    question = next((q for q in QUESTION_POOL if q["id"] == question_id), None)
    
    if not question:
        return jsonify({"error": "Question not found"}), 404
        
    is_correct = (question["answer"] == user_answer_index)
    
    return jsonify({
        "correct": is_correct,
        "correct_answer": question["answer"]
    })

if __name__ == '__main__':
    print("Starting Quiz Web App on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
