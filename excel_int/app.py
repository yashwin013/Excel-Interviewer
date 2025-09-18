# app.py

import streamlit as st
import json
import os
import random
from agents import answer_evaluator_agent, report_generator_agent, conversational_feedback_agent
from utils import text_to_speech

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Excel Interviewer",
    page_icon="📊",
    layout="centered"
)

# Apply the custom CSS
from ui_styles import css
st.markdown(css, unsafe_allow_html=True)

# --- HEADER ---
st.title("📊 Excel-Interviewer")
st.markdown("Welcome! This AI will assess your Excel skills. Please introduce yourself to begin.")

# --- HELPER FUNCTIONS ---

def load_questions():
    """Loads the entire structured question bank from questions.json."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "questions.json")
    with open(file_path, 'r') as f:
        return json.load(f)

def start_interview(difficulty):
    """Sets up the session state to start the interview for a given difficulty."""
    st.session_state.selected_difficulty = difficulty
    candidate_question_pool = st.session_state.all_questions[difficulty]
    
    num_questions_to_ask = min(6, len(candidate_question_pool))
    st.session_state.questions = random.sample(candidate_question_pool, num_questions_to_ask)
    
    st.session_state.question_index = 0
    st.session_state.interview_phase = "questions"
    
    first_question_text = "Excellent. Based on your selection, let's begin. Here is your first question."
    first_question = st.session_state.questions[0]["question"]
    
    msg1_audio = text_to_speech(first_question_text)
    msg2_audio = text_to_speech(first_question)
    
    st.session_state.messages.append({"role": "assistant", "content": first_question_text, "audio": msg1_audio})
    st.session_state.messages.append({"role": "assistant", "content": first_question, "audio": msg2_audio})
    st.rerun()

# --- INITIALIZATION ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.all_questions = load_questions()
    st.session_state.question_index = 0
    st.session_state.interview_phase = "introduction" 
    
    welcome_message = "Hello! I'm your AI-powered Excel mock interviewer. To begin, could you please tell me a little bit about yourself?"
    welcome_audio = text_to_speech(welcome_message)
    st.session_state.messages.append({"role": "assistant", "content": welcome_message, "audio": welcome_audio})

# --- DISPLAY CHAT HISTORY ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message['content'])
        if "audio" in message and message["audio"]:
            message["audio"].seek(0)
            st.audio(message["audio"], format='audio/mp3')

# --- MAIN LOGIC BASED ON INTERVIEW PHASE ---

# Phase 1: Get user's introduction
if st.session_state.interview_phase == "introduction":
    if prompt := st.chat_input("Please introduce yourself..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        acknowledgment = "Great, thank you for the introduction. Before we dive in, please select your perceived proficiency in Excel."
        ack_audio = text_to_speech(acknowledgment)
        st.session_state.messages.append({"role": "assistant", "content": acknowledgment, "audio": ack_audio})

        st.session_state.interview_phase = "difficulty_selection"
        st.rerun()

# Phase 2: Select Difficulty
elif st.session_state.interview_phase == "difficulty_selection":
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🟩 Beginner"):
            start_interview("easy")
    with col2:
        if st.button("🟦 Intermediate"):
            start_interview("medium")
    with col3:
        if st.button("🟥 Professional"):
            start_interview("hard")

# Phase 3: Ask technical questions
elif st.session_state.interview_phase == "questions":
    if prompt := st.chat_input("Your answer..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        current_q_data = st.session_state.questions[st.session_state.question_index]
        question = current_q_data["question"]
        rubric = current_q_data["rubric"]

        with st.spinner("Thinking..."):
            # --- THIS BLOCK IS UPDATED ---
            # Step 1: Get the silent, structured evaluation
            evaluation = answer_evaluator_agent(question, rubric, prompt)
            score = evaluation.get("score")
            
            # Step 2: Get the new "smart" conversational feedback
            # We now pass the original rubric and score for deeper analysis
            conversational_feedback = conversational_feedback_agent(question, prompt, rubric, score)
        
        feedback_audio = text_to_speech(conversational_feedback)
        st.session_state.messages.append({"role": "assistant", "content": conversational_feedback, "audio": feedback_audio})
        
        st.session_state.question_index += 1
        if st.session_state.question_index < len(st.session_state.questions):
            next_question = st.session_state.questions[st.session_state.question_index]["question"]
            next_q_audio = text_to_speech(next_question)
            st.session_state.messages.append({"role": "assistant", "content": next_question, "audio": next_q_audio})
        else:
            end_message = "That was the last question. Thank you for completing the interview! I will now generate your final performance report."
            end_audio = text_to_speech(end_message)
            st.session_state.messages.append({"role": "assistant", "content": end_message, "audio": end_audio})
            st.session_state.interview_phase = "report"
        
        st.rerun()

# Phase 4: Generate the final report
elif st.session_state.interview_phase == "report":
    if "final_report" not in st.session_state:
        with st.spinner("Compiling your performance summary..."):
            final_report = report_generator_agent(st.session_state.messages)
            st.session_state.final_report = final_report
            report_audio = text_to_speech(final_report)
            st.session_state.messages.append({"role": "assistant", "content": final_report, "audio": report_audio})
            st.rerun()
    else:
        st.success("Report generation complete!")
