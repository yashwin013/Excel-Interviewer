# app.py

import streamlit as st
import json
# Make sure to import the new agent
from agents import answer_evaluator_agent, report_generator_agent, conversational_feedback_agent

st.title("AI-Powered Excel Mock Interviewer 📝")

def load_questions(file_path="questions.json"):
    """Loads questions from a JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)

# --- INITIALIZATION ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.questions = load_questions()
    st.session_state.question_index = 0
    welcome_message = "Hello! I'm your AI-powered Excel mock interviewer. I'll ask you a series of questions to assess your skills. Please provide your answers in the chat. Let's start with your first question."
    st.session_state.messages.append({"role": "assistant", "content": welcome_message})
    first_question = st.session_state.questions[0]["question"]
    st.session_state.messages.append({"role": "assistant", "content": first_question})

# --- DISPLAY CHAT HISTORY ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- MAIN INTERVIEW LOGIC ---
if st.session_state.question_index < len(st.session_state.questions):
    if prompt := st.chat_input("Your answer"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        current_q_data = st.session_state.questions[st.session_state.question_index]
        question = current_q_data["question"]
        rubric = current_q_data["rubric"]

        # --- UPDATED FEEDBACK LOGIC ---
        with st.spinner("Thinking..."):
            # Step 1: Get the silent, structured evaluation
            evaluation = answer_evaluator_agent(question, rubric, prompt)
            
            # Step 2: Get the friendly, conversational feedback
            conversational_feedback = conversational_feedback_agent(question, prompt, evaluation)

        # Display the conversational feedback
        st.session_state.messages.append({"role": "assistant", "content": conversational_feedback})
        with st.chat_message("assistant"):
            st.markdown(conversational_feedback)
        
        # Move to the next question
        st.session_state.question_index += 1
        if st.session_state.question_index < len(st.session_state.questions):
            next_question = st.session_state.questions[st.session_state.question_index]["question"]
            st.session_state.messages.append({"role": "assistant", "content": next_question})
            with st.chat_message("assistant"):
                st.markdown(next_question)
        else:
            end_message = "That was the last question. Thank you for completing the interview! I will now generate your final performance report."
            st.session_state.messages.append({"role": "assistant", "content": end_message})
            with st.chat_message("assistant"):
                st.markdown(end_message)

else:
    # --- REPORT GENERATION ---
    st.info("Interview finished. Generating your final report...")
    if "final_report" not in st.session_state:
        with st.spinner("Compiling your performance summary... this may take a moment."):
            final_report = report_generator_agent(st.session_state.messages)
            st.session_state.final_report = final_report
            st.session_state.messages.append({"role": "assistant", "content": final_report})
            with st.chat_message("assistant"):
                st.markdown(final_report)
    else:
        st.success("Report generation complete!")