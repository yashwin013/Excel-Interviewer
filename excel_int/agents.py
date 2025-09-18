# agents.py

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
            model="llama-3-sonar-small-32k-online",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        evaluation = json.loads(response.choices[0].message.content)
        return evaluation
    except Exception as e:
        print(f"Error calling Perplexity API: {e}")
        return {"score": 0, "justification": "Error during evaluation."}


# --- THIS AGENT HAS BEEN UPDATED WITH A SMARTER PROMPT ---
def conversational_feedback_agent(question, user_answer, rubric, score):
    """
    Analyzes the user's answer against the rubric and provides a smart,
    context-aware response like a real interviewer.
    """
    prompt = f"""
    You are a highly intelligent and empathetic AI Excel interviewer. Your goal is to provide 'smart replies' that feel like a real, insightful conversation, not a robotic script.

    A candidate has just answered a question. Your internal system has provided you with the scoring rubric and the candidate's score.

    **Question Asked:**
    "{question}"

    **Candidate's Specific Answer:**
    "{user_answer}"

    **Evaluation Rubric (for your reference on what a perfect answer is):**
    "{rubric}"

    **Internal Score:**
    {score}/5

    **Your Task:**
    Do NOT just state the score or the justification from the rubric. Instead, **ANALYZE** the candidate's answer in detail and provide a response that directly engages with what they said.

    1.  **Acknowledge their specific points:** Start by referencing something they actually said. (e.g., "You're right on track with using VLOOKUP for this...")
    2.  **Compare their answer to the rubric:** If they missed a key detail, guide them towards it with a question. (e.g., "...but what about the fourth argument in VLOOKUP? Why is that one important for getting an exact match?")
    3.  **If they are correct (score 5):** Confirm it enthusiastically and add a small, related piece of information. (e.g., "Exactly! Using INDEX/MATCH is a great habit. Many professionals prefer it because it's more robust.")
    4.  **If they are partially correct (score 3-4):** Acknowledge the correct parts and gently correct the incorrect parts or inefficiencies. (e.g., "Using a PivotTable would definitely work here, that's a good solution. For this specific case, a function called SUMIFS would be even more direct. Have you used that one before?")
    5.  **If they are incorrect (score 1-2):** Be encouraging and reframe the problem to guide them without giving the answer away. (e.g., "Okay, I see your thought process. For this task, we need a function that can look up a value. Does a function for that come to mind?")

    **Your tone should be professional, encouraging, and insightful. Your goal is to help the candidate think, not just to grade them.**
    """
    try:
        response = client.chat.completions.create(
            model="sonar-pro",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling Perplexity API for conversational feedback: {e}")
        return "An error occurred while generating feedback."


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
            model="sonar-pro",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling Perplexity API for report generation: {e}")
        return "There was an error generating your final report."