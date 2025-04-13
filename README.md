# AI-Recruitment-and-Screening

## Project Overview
The **AI-Recruitment-and-Screening** project implements a multi-agent AI system designed to automate and streamline the job candidate screening process, leveraging Generative AI (GenAI) and agent-based principles. It aims to address the inefficiencies and potential errors associated with manual review of job descriptions (JDs) and CVs.

### Problem Statement
Manual job screening is slow, inefficient, and prone to human error. High application volumes overwhelm HR teams, creating a critical bottleneck that delays hiring and risks losing top talent. Automation is essential for speed and accuracy in today's fast-paced recruitment landscape.

### Proposed Solution
This project automates the candidate screening process by performing the following tasks:
- **User Input (UI):** HR users select a Job Description (JD) CSV file and a folder of CVs, set a shortlisting threshold, and choose which job titles to process via a Tkinter-based graphical user interface (GUI).
- **CV Pre-processing:** The system reads PDF CVs and extracts structured data (name, skills, experience, education, contact info) using Ollama LLM.
- **JD Processing & Matching:** For each selected Job Title:
  - JD Summarizer Agent summarizes the JD using Ollama LLM and extracts key requirements.
  - The Shortlisting Agent compares the summarized JD with pre-processed CV data and calculates a match score.
- **Shortlisting:** Candidates exceeding the user-defined threshold are shortlisted.
- **Scheduling (Simulated):** The Scheduler Agent generates personalized interview request messages for shortlisted candidates.
- **Reporting:** A final CSV report is generated with candidate details and match scores for all processed candidates.

## Features
- **User-Friendly Interface:** Built with Tkinter for selecting files, setting parameters, and viewing results.
- **JD Summarization:** Automatically extracts key requirements from job descriptions using Ollama LLM.
- **CV Data Extraction:** Parses PDF CVs and extracts structured data (including contact info).
- **Skill-Based Matching:** Calculates a relevance score between candidate skills and job requirements.
- **Automated Shortlisting:** Filters candidates based on a configurable match score threshold.
- **Interview Request Generation:** Creates template-based interview invitations for shortlisted candidates.
- **CSV Report Generation:** Exports a comprehensive report with candidate details and match scores.
- **Efficient Processing:** Pre-processes CVs once, improving processing speed when screening multiple job titles.
- **Local LLM Execution:** Uses Ollama to run LLMs locally, ensuring enhanced data privacy.

## Technology Stack
- **Python**: Main programming language.
- **Ollama**: Framework for running LLMs locally.
- **Mistral (or similar)**: LLM used for summarization and extraction.
- **PyMuPDF (fitz)**: For reading text from PDF files.
- **Pandas**: For loading and handling CSV data (Job Descriptions).
- **Tkinter**: For building the graphical user interface.
- **CSV Module**: Python's built-in module for CSV export.
- **Multi-Agent Design**: Implemented using Python classes.

## Setup and Installation
### 1. Clone the repository
```bash
git clone https://github.com/yourusername/AI-Recruitment-and-Screening.git
cd AI-Recruitment-and-Screening
