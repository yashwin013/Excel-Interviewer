# app.py

import streamlit as st
import json
from agents import answer_evaluator_agent, report_generator_agent, conversational_feedback_agent
from utils import text_to_speech

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Excel Interviewer",
    page_icon="📊",
    layout="centered"
)

# Apply the custom CSS from ui_styles.py
from ui_styles import css
st.markdown(css, unsafe_allow_html=True)

# --- HEADER ---
st.title("Excel Interviewer")
st.markdown("Welcome! This AI will assess your Excel skills. Let's get started.")

# --- MAIN APP LOGIC ---

def load_questions(file_path="excel_int/questions.json"):
    with open(file_path, 'r') as f:
        return json.load(f)

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.questions = load_questions()
    st.session_state.question_index = 0
    st.session_state.interview_phase = "introduction" 
    
    welcome_message = "Hello! I'm your AI-powered Excel mock interviewer. To begin, could you please tell me a little bit about yourself?"
    welcome_audio = text_to_speech(welcome_message)
    st.session_state.messages.append({"role": "assistant", "content": welcome_message, "audio": welcome_audio})

# --- DISPLAY CHAT HISTORY (with standard st.audio) ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message['content'])
        # Check if the stored message has audio
        if "audio" in message and message["audio"]:
            # Rewind the audio stream before playing
            message["audio"].seek(0)
            # Use the standard, large st.audio player
            st.audio(message["audio"], format='audio/mp3', autoplay=True)

# Main logic based on interview phase...
if st.session_state.interview_phase == "introduction":
    if prompt := st.chat_input("Please introduce yourself..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        acknowledgment = "Great, thank you. Let's dive into the first technical question."
        ack_audio = text_to_speech(acknowledgment)
        st.session_state.messages.append({"role": "assistant", "content": acknowledgment, "audio": ack_audio})
        
        first_question = st.session_state.questions[0]["question"]
        q_audio = text_to_speech(first_question)
        st.session_state.messages.append({"role": "assistant", "content": first_question, "audio": q_audio})

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
        
        feedback_audio = text_to_speech(conversational_feedback)
        st.session_state.messages.append({"role": "assistant", "content": conversational_feedback, "audio": feedback_audio})
        
        st.session_state.question_index += 1
        if st.session_state.question_index < len(st.session_state.questions):
            next_question = st.session_state.questions[st.session_state.question_index]["question"]
            next_q_audio = text_to_speech(next_question)
            st.session_state.messages.append({"role": "assistant", "content": next_question, "audio": next_q_audio})
        else:
            end_message = "That was the last question. Thank you! I will now generate your final performance report."
            end_audio = text_to_speech(end_message)
            st.session_state.messages.append({"role": "assistant", "content": end_message, "audio": end_audio})
            st.session_state.interview_phase = "report"
        
        st.rerun()

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
