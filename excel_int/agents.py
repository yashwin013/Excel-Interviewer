import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the client for Perplexity API
client = OpenAI(
    api_key=os.getenv("PERPLEXITY_API_KEY"),
    base_url="https://api.perplexity.ai"
)

def answer_evaluator_agent(question, rubric, user_answer):
    """
    Evaluates a user's answer based on a question and a rubric.
    Returns a JSON object with 'score' and 'justification'.
    """
    prompt = f"""
    You are an expert Excel technical interviewer. Your task is to evaluate a candidate's answer based on a specific question and an evaluation rubric.

    **Question Asked:**
    {question}

    **Evaluation Rubric:**
    {rubric}

    **Candidate's Answer:**
    {user_answer}

    **Your Task:**
    Analyze the candidate's answer against the rubric. Provide a score from 1 (Poor) to 5 (Excellent) and a brief justification for your score.
    Respond ONLY with a single, valid JSON object in the following format. Do not include any other text, just the JSON.
    {{
      "score": <integer>,
      "justification": "<string>"
    }}
    """
    try:
        response = client.chat.completions.create(
            # --- CORRECTED MODEL NAME ---
            model="sonar-pro",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        evaluation = json.loads(response.choices[0].message.content)
        return evaluation
    except Exception as e:
        print(f"Error calling Perplexity API: {e}")
        return {"score": 0, "justification": "Error during evaluation."}


def report_generator_agent(interview_history):
    """
    Generates a final performance report based on the entire interview history.
    """
    formatted_history = "\n\n".join(
        [f"Role: {msg['role']}\nContent: {msg['content']}" for msg in interview_history]
    )

    prompt = f"""
    You are a senior hiring manager providing feedback on an Excel technical interview.
    Based on the following complete interview transcript, your task is to generate a final performance report for the candidate.

    **Interview Transcript:**
    {formatted_history}

    **Your Task:**
    Write a constructive, professional performance summary. The summary should include:
    1.  An **Overall Performance** paragraph.
    2.  A list of **Key Strengths** demonstrated by the candidate.
    3.  A list of **Areas for Improvement**, with actionable advice.
    4.  A final **Overall Score** on a scale of 1 to 10.

    Structure your response using Markdown for clear formatting.
    """
    try:
        response = client.chat.completions.create(
            # --- CORRECTED MODEL NAME ---
            model="sonar-pro",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling Perplexity API for report generation: {e}")
        return "There was an error generating your final report."
    




# agents.py (add this new function at the end)

def conversational_feedback_agent(question, user_answer, evaluation):
    """
    Takes a structured evaluation and delivers it in a natural, conversational way.
    """
    score = evaluation.get("score")
    justification = evaluation.get("justification")

    prompt = f"""
    You are a friendly and encouraging Excel technical interviewer. Your internal system has just evaluated a candidate's answer.

    **Question Asked:** "{question}"
    **Candidate's Answer:** "{user_answer}"
    
    **Internal Evaluation Results:**
    - Score: {score}/5
    - Justification: {justification}

    **Your Task:**
    Deliver this evaluation to the candidate in a natural, conversational, and encouraging tone. Do NOT sound like a robot just listing the score.

    - If the score is high (4 or 5), start with a positive affirmation like "Excellent, that's exactly right!" or "Great explanation!". Then, briefly mention the key points they hit correctly based on the justification.
    - If the score is average (3), acknowledge their answer positively but gently guide them. For example: "That's a solid approach. A slightly more efficient way might be...".
    - If the score is low (1 or 2), be encouraging, not critical. Start with something like "Okay, thanks for walking me through your thought process." or "That's a good start." Then, clearly and simply explain the correct approach based on the justification.
    
    Keep your response concise and focused on the feedback.
    """
    try:
        response = client.chat.completions.create(
            model="sonar-pro", # Or your preferred model
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6 # Allow for a more natural, conversational tone
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling Perplexity API for conversational feedback: {e}")
        # Fallback to the structured feedback if the conversational agent fails
        return f"**Evaluation:**\n- **Score:** {score}/5\n- **Feedback:** {justification}"