const startScreen = document.getElementById('start-screen');
const quizScreen = document.getElementById('quiz-screen');
const resultScreen = document.getElementById('result-screen');
const startBtn = document.getElementById('start-btn');
const restartBtn = document.getElementById('restart-btn');
const questionText = document.getElementById('question-text');
const optionsContainer = document.getElementById('options-container');
const currentScoreSpan = document.getElementById('current-score');
const progressBar = document.getElementById('progress-bar');
const finalScoreSpan = document.getElementById('final-score');
const loadingSpinner = document.getElementById('loading-spinner');

let questions = [];
let currentQuestionIndex = 0;
let score = 0;
let isAnswerLocked = false;

// --- Event Listeners ---
startBtn.addEventListener('click', initGame);
restartBtn.addEventListener('click', initGame);

async function initGame() {
    // UI Reset
    score = 0;
    currentQuestionIndex = 0;
    isAnswerLocked = false;
    currentScoreSpan.innerText = '0';
    progressBar.style.width = '0%';

    // Transitions
    resultScreen.classList.remove('active');
    resultScreen.classList.add('hidden');
    startScreen.classList.remove('hidden');
    startScreen.classList.add('active');

    // Show loading
    startBtn.classList.add('hidden');
    loadingSpinner.classList.remove('hidden');

    try {
        // Fetch Questions from Flask Backend
        const response = await fetch('/api/questions');
        questions = await response.json();

        // Start Game
        startScreen.classList.remove('active');
        startScreen.classList.add('hidden');
        quizScreen.classList.remove('hidden');
        setTimeout(() => quizScreen.classList.add('active'), 50);

        loadQuestion();
    } catch (error) {
        console.error("Failed to fetch questions", error);
        alert("Error loading quiz data. Is the server running?");
        startBtn.classList.remove('hidden');
    } finally {
        loadingSpinner.classList.add('hidden');
    }
}

function loadQuestion() {
    const currentQ = questions[currentQuestionIndex];
    questionText.textContent = currentQ.question;
    optionsContainer.innerHTML = '';
    isAnswerLocked = false;

    // Update Progress
    const progress = (currentQuestionIndex / questions.length) * 100;
    progressBar.style.width = `${progress}%`;

    // Render Options
    currentQ.options.forEach((opt, index) => {
        const btn = document.createElement('button');
        btn.classList.add('option-btn');
        btn.textContent = opt;
        btn.addEventListener('click', () => checkAnswer(currentQ.id, index, btn));
        optionsContainer.appendChild(btn);
    });
}

async function checkAnswer(questionId, selectedIndex, selectedBtn) {
    if (isAnswerLocked) return;
    isAnswerLocked = true;

    try {
        // Validate with Backend
        const response = await fetch('/api/check-answer', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question_id: questionId, answer_index: selectedIndex })
        });

        const result = await response.json();
        const options = document.querySelectorAll('.option-btn');

        if (result.correct) {
            selectedBtn.classList.add('correct');
            score++;
            currentScoreSpan.textContent = score;
        } else {
            selectedBtn.classList.add('wrong');
            // Highlight correct one
            if (options[result.correct_answer]) {
                options[result.correct_answer].classList.add('correct');
            }
        }

        // Next Question Delay
        setTimeout(() => {
            currentQuestionIndex++;
            if (currentQuestionIndex < questions.length) {
                loadQuestion();
            } else {
                showResults();
            }
        }, 1500);

    } catch (error) {
        console.error("Error checking answer", error);
        isAnswerLocked = false; // Allow retry if error
    }
}

function showResults() {
    quizScreen.classList.remove('active');
    quizScreen.classList.add('hidden');

    resultScreen.classList.remove('hidden');
    setTimeout(() => resultScreen.classList.add('active'), 50);

    finalScoreSpan.textContent = `${score} / ${questions.length}`;
}
