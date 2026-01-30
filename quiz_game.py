import time
import threading
import random

# --- Configuration ---
# Expanded Question Bank with Difficulty Levels
QUESTIONS = [
    # --- EASY ---
    {
        "question": "What is the correct file extension for Python files?",
        "options": ["A. .pt", "B. .pyt", "C. .py", "D. .python"],
        "answer": "C",
        "difficulty": "Easy"
    },
    {
        "question": "Which keyword is used to start a loop?",
        "options": ["A. hoop", "B. loop", "C. for", "D. next"],
        "answer": "C",
        "difficulty": "Easy"
    },
    {
        "question": "Which of these is NOT a core data type in Python?",
        "options": ["A. List", "B. Dictionary", "C. Tuple", "D. Class"],
        "answer": "D",
        "difficulty": "Easy"
    },
    # --- MEDIUM ---
    {
        "question": "Which operator is used for exponentiation (power) in Python?",
        "options": ["A. ^", "B. **", "C. //", "D. exp()"],
        "answer": "B",
        "difficulty": "Medium"
    },
    {
        "question": "What is the output of: print(10 // 3)?",
        "options": ["A. 3.33", "B. 3", "C. 3.0", "D. 30"],
        "answer": "B",
        "difficulty": "Medium"
    },
    {
        "question": "How do you start a comment in Python?",
        "options": ["A. //", "B. <!--", "C. #", "D. %"],
        "answer": "C",
        "difficulty": "Medium"
    },
    # --- HARD ---
    {
        "question": "What comes after 'if' statement if all checks fail?",
        "options": ["A. then", "B. else", "C. stop", "D. elif"],
        "answer": "B",
        "difficulty": "Hard"
    },
    {
        "question": "What data type is the result of: 3 < 10?",
        "options": ["A. int", "B. bool", "C. str", "D. float"],
        "answer": "B",
        "difficulty": "Hard"
    }
]

TIME_LIMIT = 15  # Seconds per question
LIFELINES = {"50-50": True}  # True means available

def get_input_with_timeout(prompt, timeout):
    """
    Helper function to get user input with a time limit using threading.
    """
    print(prompt, end="", flush=True)
    result = [None]
    
    def get_user_input():
        try:
            result[0] = input()
        except:
            return

    input_thread = threading.Thread(target=get_user_input)
    input_thread.daemon = True
    input_thread.start()
    input_thread.join(timeout)
    
    if input_thread.is_alive():
        print("\n⏳ Time's up!", flush=True)
        return None
    else:
        return result[0]

def apply_lifeline_5050(q_data):
    """
    Returns a list of options with 2 wrong answers removed.
    """
    correct_option = next(opt for opt in q_data['options'] if opt.startswith(q_data['answer']))
    wrong_options = [opt for opt in q_data['options'] if not opt.startswith(q_data['answer'])]
    
    # Randomly keep one wrong option
    kept_wrong = random.choice(wrong_options)
    
    # enhance display
    reduced_options = [correct_option, kept_wrong]
    # Sort to keep original order A, B, C, D roughly (optional, but looks better)
    reduced_options.sort() 
    return reduced_options

def run_quiz():
    print("\n" + "="*50)
    print("   PYTHON QUIZ GAME: EXPANDED EDITION   ")
    print("="*50)
    
    # --- Difficulty Selection ---
    print("\nChoose your Difficulty Level:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")
    print("4. Mixed (All Questions)")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    level_map = {'1': 'Easy', '2': 'Medium', '3': 'Hard'}
    selected_difficulty = level_map.get(choice, 'Mixed')
    
    if selected_difficulty == 'Mixed':
        quiz_questions = QUESTIONS
    else:
        quiz_questions = [q for q in QUESTIONS if q['difficulty'] == selected_difficulty]
    
    if not quiz_questions:
        print("No questions found for this difficulty!")
        return

    random.shuffle(quiz_questions) # Shuffle questions for variety
    
    print(f"\nStarting {selected_difficulty} Level Quiz with {len(quiz_questions)} questions.")
    print(f"You have {TIME_LIMIT} seconds per question.")
    print("Lifeline Available: Type 'L' to use 50-50 (Removes 2 wrong options).")
    input("Press Enter to Start...")
    print("\n" + "-"*50 + "\n")

    score = 0
    
    for i, q_data in enumerate(quiz_questions):
        print(f"Question {i+1} [{q_data['difficulty']}]: {q_data['question']}")
        
        # Display Options
        for option in q_data['options']:
            print(option)
            
        # Get Answer Loop (to handle Lifeline usage)
        timer_active = True
        options_displayed = q_data['options'] # Current visible options
        
        while True:
             # If using lifeline, we might restart timer or just continue. 
             # For simplicity, we restart timer on lifeline usage step to be fair.
            user_answer = get_input_with_timeout("\nYour Answer (or 'L' for 50-50): ", TIME_LIMIT)
            
            if user_answer is None: # Timeout
                print(f"❌ Time's up! The correct answer was {q_data['answer']}")
                break
            
            user_answer = user_answer.strip().upper()
            
            # Lifeline Logic
            if user_answer == 'L':
                if LIFELINES["50-50"]:
                    print("\n🔵 USING 50-50 LIFELINE...")
                    options_displayed = apply_lifeline_5050(q_data)
                    print("Remaining Options:")
                    for option in options_displayed:
                        print(option)
                    LIFELINES["50-50"] = False # Mark as used
                    # Continue loop to ask for answer again
                    continue 
                else:
                    print("\n⚠️ You have already used your 50-50 Lifeline!")
                    continue

            # Answer Validation
            valid_choices = ['A', 'B', 'C', 'D']
            if user_answer not in valid_choices:
                print("⚠️ Invalid input. Please type A, B, C, or D.")
                continue
                
            # Check Answer
            if user_answer == q_data['answer']:
                print("✅ Correct!")
                score += 1
            else:
                print(f"❌ Wrong! The correct answer was {q_data['answer']}")
            break # Exit retry loop and go to next question
            
        print("-" * 30 + "\n")
        time.sleep(1)

    # --- Final Result ---
    print("="*50)
    print("        QUIZ COMPLETED!        ")
    print("="*50)
    print(f"Final Score: {score} / {len(quiz_questions)}")
    
    percentage = (score / len(quiz_questions)) * 100
    if percentage == 100:
        print("🏆 Perfect! AMAZING!")
    elif percentage >= 70:
        print("👏 Great Job!")
    else:
        print("📚 Keep practicing!")
    print("="*50)

if __name__ == "__main__":
    run_quiz()
