# Design Document: AI-Powered Excel Mock Interviewer

## 1. Project Mission & Business Context

**Mission:** To design and build an automated system that can conduct a preliminary technical interview to assess a candidate's Microsoft Excel skills.

**Business Problem:** The current manual screening process is a time-consuming bottleneck for senior analysts, leading to inconsistent evaluations and slow hiring pipelines. This AI agent aims to solve this by automating and standardizing the initial screening.

---

## 2. Technology Stack Justification

This section outlines the chosen technologies and the reasons for their selection.

* **Core Language: Python**
    * **Justification:** Python is the industry standard for AI and machine learning due to its simple syntax and the extensive ecosystem of libraries (like Streamlit and OpenAI).

* **AI Model: GPT-4o (via OpenAI API)**
    * **Justification:** I chose GPT-4o for its advanced reasoning capabilities, which are essential for intelligently evaluating nuanced, multi-step answers about Excel. Its ability to follow complex instructions and return structured JSON is critical for the `AnswerEvaluator` agent.

* **Web Framework: Streamlit**
    * **Justification:** Streamlit is a Python-based framework perfect for rapidly building interactive Proof-of-Concept (PoC) applications. It allows me to create a functional chat interface with minimal code, avoiding the complexities of traditional web development.

* **Deployment: Streamlit Community Cloud**
    * **Justification:** This is a free hosting platform that integrates directly with GitHub. It provides the fastest path to getting a shareable, deployed link for the PoC, which is a key project deliverable.

---

## 3. System Architecture

The system will be built using a multi-agent approach to separate concerns and keep the code organized:

1.  **`InterviewConductor`:** The main agent that manages the overall flow of the interview.
2.  **`AnswerEvaluator`:** The core engine that takes a single question/answer pair and evaluates it against a predefined rubric.
3.  **`ReportGenerator`:** The agent that synthesizes the entire interview history into a final performance summary.

---

## 4. Solution to the "Cold Start" Problem

The project starts with no pre-existing dataset of interviews. My strategy to solve this is to **bootstrap the system with a manually created, high-quality question bank.**

This involves creating a `questions.json` file containing a curated set of questions, each with a detailed evaluation rubric. This rubric provides the structured criteria the `AnswerEvaluator` agent will use, ensuring consistent and reliable scoring from day one.