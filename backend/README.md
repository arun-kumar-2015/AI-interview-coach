# Smart AI Interview & Resume Coach - Backend

A production-ready backend for AI-powered interview preparation and resume improvement using Generative AI and RAG (Retrieval-Augmented Generation).

## 🚀 Features

- **Resume Upload (PDF)**: Extract and process text from PDF resumes
- **Vector Storage**: FAISS-based semantic search for resume content
- **Technical Questions**: Personalized interview questions based on resume
- **Answer Evaluation**: Score answers with detailed feedback
- **HR Questions**: Behavioral and leadership questions
- **Resume Improvement**: ATS optimization and content suggestions

## 🛠️ Tech Stack

- **FastAPI**: Modern Python web framework
- **FAISS**: Vector similarity search
- **Sentence-Transformers**: Text embeddings
- **OpenAI API**: LLM for question generation and evaluation
- **PyPDF**: PDF text extraction

## 📁 Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── routes/                # API route handlers
│   ├── upload.py          # Resume upload endpoints
│   ├── questions.py       # Technical question generation
│   ├── evaluate.py        # Answer evaluation
│   ├── hr_questions.py    # HR/behavioral questions
│   └── improve.py         # Resume improvement
├── services/              # Business logic
│   ├── embedding_service.py
│   ├── vector_store.py
│   ├── llm_service.py
│   └── pdf_service.py
└── prompts/               # Prompt templates
    ├── question_generator.py
    ├── hr_questions.py
    ├── answer_evaluator.py
    └── resume_improver.py
```

## ⚙️ Setup Instructions

### 1. Create Virtual Environment

```
bash
# Navigate to backend directory
cd ai-interview-coach/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```
bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```
bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API key
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-3.5-turbo
```

### 4. Run the Server

```
bash
# Development mode
python main.py

# Or using uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/upload_resume` | POST | Upload and process PDF resume |
| `/api/generate_questions` | POST | Generate technical questions |
| `/api/evaluate_answer` | POST | Evaluate interview answer |
| `/api/generate_hr_questions` | POST | Generate behavioral questions |
| `/api/improve_resume` | POST | Get resume improvement suggestions |
| `/api/check_ats` | POST | Check ATS compatibility |

## 🧠 RAG Concept

This application uses **Retrieval-Augmented Generation (RAG)**:

1. **Resume Processing**: Extract text from PDF and create embeddings
2. **Vector Storage**: Store embeddings in FAISS for semantic search
3. **Retrieval**: When generating questions, retrieve relevant resume sections
4. **Generation**: Use LLM with retrieved context for personalized questions

This ensures generated questions are strictly based on the candidate's actual experience.

## 📝 Prompt Engineering

The application uses sophisticated prompt engineering:

- **System Prompts**: Define AI persona and constraints
- **User Prompts**: Task-specific context and requirements
- **Temperature Control**:
  - Low (0.0-0.2): For consistent evaluation
  - Medium (0.5-0.7): For diverse question generation

## 🐳 Docker Support (Optional)

```
dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📄 License

MIT License

## 👤 Author

AI Interview Coach Team
