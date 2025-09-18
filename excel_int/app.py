# app.py

import streamlit as st
import json
from agents import answer_evaluator_agent, report_generator_agent, conversational_feedback_agent
from utils import text_to_speech
from ui_styles import css

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Excel Interviewer",
    page_icon="📊",
    layout="centered"
)

# Apply the custom CSS
st.markdown(css, unsafe_allow_html=True)

# --- HEADER (Now without the container div) ---
st.title("📊 Excel Interviewer Pro")
st.markdown("Welcome! This AI will assess your Excel skills. Please introduce yourself to begin.")


# --- MAIN APP LOGIC ---

def load_questions(file_path="questions.json"):
    with open(file_path, 'r') as f:
        return json.load(f)

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.questions = load_questions()
    st.session_state.question_index = 0
    st.session_state.interview_phase = "introduction" 
    
    welcome_message = "Hello! I'm your AI-powered Excel mock interviewer. To begin, could you please tell me a little bit about yourself?"
    st.session_state.messages.append({"role": "assistant", "content": welcome_message})
    st.session_state.welcome_audio = text_to_speech(welcome_message)

# Display chat history
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        # REMOVED the <div class='glassmorphism'> wrapper for a cleaner look
        st.markdown(message['content']) 
        if i == 0 and st.session_state.welcome_audio:
            st.audio(st.session_state.welcome_audio, format='audio/mp3', autoplay=True)

# Main logic based on interview phase...
if st.session_state.interview_phase == "introduction":
    if prompt := st.chat_input("Please introduce yourself..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        acknowledgment = "Great, thank you. Let's dive into the first technical question."
        st.session_state.messages.append({"role": "assistant", "content": acknowledgment})
        
        first_question = st.session_state.questions[0]["question"]
        st.session_state.messages.append({"role": "assistant", "content": first_question})

        st.session_state.interview_phase = "questions"
        st.rerun()

elif st.session_state.interview_phase == "questions":
    if prompt := st.chat_input("Your answer..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        current_q_data = st.session_state.questions[st.session_state.question_index]
        question = current_q_data["question"]
        rubric = current_q_data["rubric"]

        with st.spinner("Thinking..."):
            evaluation = answer_evaluator_agent(question, rubric, prompt)
            conversational_feedback = conversational_feedback_agent(question, prompt, evaluation)
        
        st.session_state.messages.append({"role": "assistant", "content": conversational_feedback})
        
        st.session_state.question_index += 1
        if st.session_state.question_index < len(st.session_state.questions):
            next_question = st.session_state.questions[st.session_state.question_index]["question"]
            st.session_state.messages.append({"role": "assistant", "content": next_question})
        else:
            end_message = "That was the last question. Thank you for completing the interview! I will now generate your final performance report."
            st.session_state.messages.append({"role": "assistant", "content": end_message})
            st.session_state.interview_phase = "report"
        
        st.rerun()

elif st.session_state.interview_phase == "report":
    if "final_report" not in st.session_state:
        with st.spinner("Compiling your performance summary..."):
            final_report = report_generator_agent(st.session_state.messages)
            st.session_state.final_report = final_report
            st.session_state.messages.append({"role": "assistant", "content": final_report})
            st.rerun()
    else:
        st.success("Report generation complete!")