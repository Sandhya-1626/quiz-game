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

let currentQuestionIndex = 0;
let score = 0;

// Sample Questions Data
const questions = [
    {
        question: "What does HTML stand for?",
        options: [
            "Hyper Text Preprocessor",
            "Hyper Text Markup Language",
            "Hyper Text Multiple Language",
            "Hyper Tool Multi Language"
        ],
        answer: 1 // Index of correct answer
    },
    {
        question: "Which language runs in a web browser?",
        options: ["Java", "C", "Python", "JavaScript"],
        answer: 3
    },
    {
        question: "What does CSS stand for?",
        options: [
            "Central Style Sheets",
            "Cascading Style Sheets",
            "Cascading Simple Sheets",
            "Cars SUVs Sailboats"
        ],
        answer: 1
    },
    {
        question: "What year was JavaScript launched?",
        options: ["1996", "1995", "1994", "None of the above"],
        answer: 1
    },
    {
        question: "Which symbol is used for comments in JavaScript?",
        options: ["//", "<!--", "#", "/* */"],
        answer: 0
    }
];

// Event Listeners
startBtn.addEventListener('click', startQuiz);
restartBtn.addEventListener('click', () => {
    resetQuiz();
    startQuiz();
});

function startQuiz() {
    startScreen.classList.remove('active');
    startScreen.classList.add('hidden');
    
    quizScreen.classList.remove('hidden');
    setTimeout(() => {
        quizScreen.classList.add('active');
    }, 10); // Small delay for transition
    
    currentQuestionIndex = 0;
    score = 0;
    updateScore();
    loadQuestion();
}

function loadQuestion() {
    const currentQuestion = questions[currentQuestionIndex];
    questionText.textContent = currentQuestion.question;
    
    optionsContainer.innerHTML = '';
    
    currentQuestion.options.forEach((option, index) => {
        const button = document.createElement('button');
        button.classList.add('option-btn');
        button.textContent = option;
        button.addEventListener('click', () => selectOption(index));
        optionsContainer.appendChild(button);
    });

    // Update Progress Bar
    const progress = ((currentQuestionIndex) / questions.length) * 100;
    progressBar.style.width = `${progress}%`;
}

function selectOption(selectedIndex) {
    const currentQuestion = questions[currentQuestionIndex];
    const options = optionsContainer.children;
    
    // Disable all buttons
    for(let btn of options) {
        btn.disabled = true;
        btn.style.cursor = 'default';
    }

    // Check Answer
    if (selectedIndex === currentQuestion.answer) {
        options[selectedIndex].classList.add('correct');
        score++;
        updateScore();
    } else {
        options[selectedIndex].classList.add('wrong');
        // Show correct answer
        options[currentQuestion.answer].classList.add('correct');
    }

    // Wait and go to next question
    setTimeout(() => {
        currentQuestionIndex++;
        if (currentQuestionIndex < questions.length) {
            loadQuestion();
        } else {
            showResults();
        }
    }, 1500);
}

function updateScore() {
    currentScoreSpan.textContent = score;
}

function showResults() {
    quizScreen.classList.remove('active');
    quizScreen.classList.add('hidden');
    
    resultScreen.classList.remove('hidden');
    setTimeout(() => {
        resultScreen.classList.add('active');
    }, 10);
    
    finalScoreSpan.textContent = `${score} / ${questions.length}`;
}

function resetQuiz() {
    resultScreen.classList.remove('active');
    resultScreen.classList.add('hidden');
    
    startScreen.classList.remove('hidden');
    setTimeout(() => {
        startScreen.classList.add('active');
    }, 10);
}
