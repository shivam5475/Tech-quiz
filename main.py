import streamlit as st
import random
import time

# Custom CSS for a cool, advanced look
st.markdown("""
    <style>
    .main {
        background-color: #1e1e2f;
        color: #ffffff;
        font-family: 'Arial', sans-serif;
    }
    .stButton>button {
        background-color: #00d4ff;
        color: black;
        border-radius: 10px;
        font-weight: bold;
        padding: 10px 20px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #ff007a;
        color: white;
    }
    .stProgress .st-bo {
        background-color: #00d4ff;
    }
    .title {
        font-size: 40px;
        color: #00d4ff;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .subtitle {
        font-size: 20px;
        color: #ff007a;
        text-align: center;
        margin-bottom: 20px;
    }
    .question-text {
        font-size: 18px;
        margin-bottom: 10px;
    }
    .result-box {
        background-color: #2d2d44;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .stRadio>label {
        color: #ffffff;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

# Sample question bank (expand to 100 questions)
questions = [
    {"question": "What is the time complexity of QuickSort in its average case?", "options": ["O(n)", "O(n log n)", "O(n²)", "O(log n)"], "answer": "O(n log n)"},
    {"question": "Which data structure uses the Last In, First Out (LIFO) principle?", "options": ["Queue", "Stack", "Array", "Tree"], "answer": "Stack"},
    {"question": "What does SQL stand for?", "options": ["Structured Query Language", "Simple Query Logic", "System Query Language", "Structured Quick Language"], "answer": "Structured Query Language"},
    {"question": "Which of these is a type of linked list?", "options": ["Binary Tree", "Doubly Linked List", "Stack", "Queue"], "answer": "Doubly Linked List"},
    {"question": "What protocol is primarily used for sending emails?", "options": ["HTTP", "FTP", "SMTP", "TCP"], "answer": "SMTP"},
    # Add more questions to reach 100, covering topics like Data Structures, Algorithms, Databases, OS, Networks, etc.
    # Example additional question:
    {"question": "Which sorting algorithm is known as Divide and Conquer?", "options": ["Bubble Sort", "Merge Sort", "Selection Sort", "Insertion Sort"], "answer": "Merge Sort"},
]

# Initialize session state variables
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
if 'selected_questions' not in st.session_state:
    st.session_state.selected_questions = []
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'quiz_finished' not in st.session_state:
    st.session_state.quiz_finished = False
if 'end_time' not in st.session_state:
    st.session_state.end_time = None

# Welcome page
if not st.session_state.quiz_started:
    st.markdown("<h1 class='title'>Tech Quiz</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>For 2nd Year CSE B.Tech Students<br>Test your skills with 10 random questions out of 100!<br>You have 10 minutes. Good Luck!</p>", unsafe_allow_html=True)
    if st.button("Start Quiz"):
        # Start the quiz: select 10 random questions and reset state
        st.session_state.selected_questions = random.sample(questions, min(10, len(questions)))  # Ensure we don't exceed available questions
        st.session_state.start_time = time.time()
        st.session_state.quiz_started = True
        st.session_state.current_question = 0
        st.session_state.quiz_finished = False
        st.session_state.end_time = None
        st.experimental_rerun()

# Quiz in progress
elif not st.session_state.quiz_finished:
    # Timer logic
    elapsed_time = time.time() - st.session_state.start_time
    total_time = 600  # 10 minutes in seconds
    remaining_time = max(0, total_time - elapsed_time)
    
    if remaining_time <= 0:
        # Time's up, end the quiz
        st.session_state.end_time = time.time()
        st.session_state.quiz_finished = True
        st.experimental_rerun()
    else:
        # Display timer and progress
        st.markdown(f"<p class='subtitle'>Time Remaining: {int(remaining_time // 60)}:{int(remaining_time % 60):02d}</p>", unsafe_allow_html=True)
        st.progress((st.session_state.current_question + 1) / 10)

        # Current question
        current_q = st.session_state.selected_questions[st.session_state.current_question]
        st.markdown(f"<p class='question-text'><strong>Question {st.session_state.current_question + 1} of 10:</strong> {current_q['question']}</p>", unsafe_allow_html=True)
        selected = st.radio("Select an option:", current_q["options"], key=f"radio_{st.session_state.current_question}")

        # Navigation buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.session_state.current_question > 0:
                if st.button("Previous"):
                    st.session_state.current_question -= 1
                    st.experimental_rerun()
        with col2:
            if st.session_state.current_question < 9:
                if st.button("Next"):
                    st.session_state.current_question += 1
                    st.experimental_rerun()
            else:
                if st.button("Submit"):
                    st.session_state.end_time = time.time()
                    st.session_state.quiz_finished = True
                    st.experimental_rerun()

# Results page
else:
    st.markdown("<h1 class='title'>Quiz Results</h1>", unsafe_allow_html=True)
    
    # Calculate score
    answers = [st.session_state.get(f"radio_{i}", None) for i in range(10)]
    correct_answers = [q["answer"] for q in st.session_state.selected_questions]
    score = sum(a == c for a, c in zip(answers, correct_answers) if a is not None)
    
    # Calculate time taken
    time_taken = st.session_state.end_time - st.session_state.start_time
    minutes, seconds = divmod(int(time_taken), 60)
    result_message = "Time's up! Here are your results:" if time_taken >= total_time else "Quiz completed! Here are your results:"
    st.markdown(f"<p class='subtitle'>{result_message}<br>You scored {score} out of 10 in {minutes} minutes and {seconds} seconds.</p>", unsafe_allow_html=True)
    
    # Detailed feedback
    for i, q in enumerate(st.session_state.selected_questions):
        user_answer = answers[i] if answers[i] is not None else "Not answered"
        correct_answer = q["answer"]
        color = "green" if user_answer == correct_answer else "red" if user_answer != "Not answered" else "gray"
        st.markdown(
            f"<div class='result-box'>"
            f"<strong>Question {i+1}:</strong> {q['question']}<br>"
            f"Your answer: <span style='color:{color}'>{user_answer}</span><br>"
            f"Correct answer: <span style='color:green'>{correct_answer}</span>"
            f"</div>",
            unsafe_allow_html=True
        )
    
    # Retake option
    if st.button("Retake Quiz"):
        st.session_state.quiz_started = False
        st.session_state.selected_questions = []
        st.session_state.current_question = 0
        st.session_state.start_time = None
        st.session_state.end_time = None
        st.session_state.quiz_finished = False
        st.experimental_rerun()
