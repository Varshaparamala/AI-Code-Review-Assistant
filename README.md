# AI Code Review Assistant

A full-stack web app that reviews Python code. Paste code into the web page and get instant feedback from rule-based checks and an AI reviewer.

## Features
- Rule-based analysis: syntax errors, missing docstrings, bare `except`, `print()` usage, long lines, TODO comments
- AI-powered review using the Claude API
- React frontend with a simple code editor and results list

## Tech Stack
- Backend: Python, FastAPI, Uvicorn
- Frontend: React (Vite)
- AI: Anthropic Claude API

## How to Run

### Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install fastapi uvicorn anthropic
set ANTHROPIC_API_KEY=your-key-here
uvicorn main:app --reload

### Frontend
cd frontend
npm install
npm run dev

Open http://localhost:5173

## API Endpoints
- POST /review: rule-based checks
- POST /review-ai: rule-based checks plus AI feedback
