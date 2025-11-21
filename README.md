Project Title: Academic Note-Taker Agent: 
Demonstrating Tool Use, Memory, and Evaluation

1.Project Overview
The Academic Note-Taker Agent is an intelligent system designed for students, converting raw lecture transcripts and academic text into highly structured, personalized, and high-quality study notes. Built on the Gemini API, this autonomous agent goes beyond simple summarization by extracting key concepts, identifying core definitions, and generating actionable study tasks, significantly boosting student productivity and learning efficiency.
Problem Solved: This agent automates the time-consuming process of manually summarizing dense academic material, freeing up student time and ensuring study guides are effective and accurate.

2.Agent Architecture & Workflow
The system is organized around the central NoteTakingAgent that orchestrates the flow of data, leveraging a structured set of internal tools and persistence mechanisms.
Workflow Steps:
Input: The agent receives the text transcript (simulating a processed lecture recording).
Orchestration: The NoteTakingAgent loads the user's latest preferences from Memory.
Generation (Tool Use): It calls the NoteGenerator (which uses the Gemini API) to create structured notes based on the current style/format preference.
Quality Check (Evaluation): The NoteEvaluator checks the generated notes against the original transcript, providing a score and feedback.
Persistence: The agent saves the session history and the final quality score back to Memory (agent_memory.json).
Output (Tool Use): The final notes are printed to the console and exported to notes_output.md.
Key Capabilities Demonstrated
This project applies the three core concepts taught in the 5-Day AI Agentic Program:
A. Tool Use (Functionality & External Action) The agent abstracts the use of external capabilities into dedicated tools: LLM Tool: The NoteGenerator class uses the models/gemini-2.5-flash model with a specific, engineered prompt to transform unstructured text into structured notes (e.g., separating concepts, definitions, and tasks). Export Tool: The agent implements the export_notes function (Tool Use #3) to write the final, polished notes to a physical file (notes_output.md), demonstrating an external system action.
B. Memory (Statefulness & Personalization) Preference Management: The NoteMemory class stores user preferences (like style, format_type) in agent_memory.json and recalls them to influence the AI's note generation process in subsequent runs. History Tracking: It tracks session history and quality scores, allowing for future long-term agent refinement.
C. Evaluation (Quality & Feedback Loop) The NoteEvaluator provides quantitative and qualitative assessment, a critical element for agent trustworthiness. Metrics: It scores the output against the original transcript using three objective metrics: Completeness, Conciseness, and Structure. Feedback: Provides textual feedback to help the user fine-tune their next request.

4.Technical Implementation & Code Outline
Language: Python Core Library: google-genai Model: models/gemini-2.5-flash

5.Setup and Execution
Prerequisites
Python 3.8+
A valid Gemini API Key.
Getting Started
Clone the Repository: git clone [https://github.com/gorechashubham2412-a11y/AI-Note-Taking-Agent-Capstone]
cd AI-Note-Taking-Agent-Capstone
Install Dependencies: pip install -r requirements.txt (The primary dependency is google-genai)
Configuration: Before running, ensure you set your Gemini API key as an environment variable or replace the placeholder in final.py.
Run the Agent: python final.py
Expected Output: The script will print the final structured notes, a detailed evaluation report, and save the notes to notes_output.md and the session data to agent_memory.json.
