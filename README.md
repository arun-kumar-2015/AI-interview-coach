# Smart AI Interview & Resume Coach

A production-ready full-stack application using Generative AI to help job seekers prepare for interviews and improve their resumes.

## 🚀 Features

### 1. Resume Upload (PDF)
- User uploads resume in PDF format
- Extract text from PDF using PyPDF
- Clean and preprocess text for analysis

### 2. Resume Embedding + Vector Storage
- Convert resume text into embeddings using sentence-transformers
- Store embeddings in FAISS vector database
- Enable semantic retrieval for personalized questions

### 3. Personalized Interview Question Generator
- Generate technical questions based strictly on resume content
- Uses RAG (Retrieval-Augmented Generation) pattern
- Avoid generic questions - all questions are personalized

### 4. Mock Interview Mode
- Ask one question at a time
- Accept user answers
- Evaluate answers with scoring (0-10)
- Provide strengths and improvement suggestions

### 5. HR + Behavioral Question Generator
- Separate prompt templates for HR questions
- Focus on leadership, teamwork, communication
- STAR method guidance

### 6. Resume Improvement Feature
- Analyze resume for ATS optimization
- Suggest improvements for better parsing
- Quantify bullet points suggestions

## 🛠️ Tech Stack

### Frontend
- **React** (Vite)
- **Tailwind CSS**
- **Axios** for API calls
- **React Router** for navigation

### Backend
- **Python**
- **FastAPI** for REST APIs
- **PyPDF** for PDF parsing
- **FAISS** for vector storage
- **Sentence-transformers** for embeddings
- **OpenAI** API compatible for LLM

## 📁 Project Structure

```
ai-interview-coach/
├── backend/
│   ├── main.py                    # FastAPI application
│   ├── requirements.txt           # Python dependencies
│   ├── .env.example              # Environment variables template
│   ├── README.md                  # Backend README
│   ├── routes/                    # API route handlers
│   │   ├── upload.py             # Resume upload endpoints
│   │   ├── questions.py          # Technical question generation
│   │   ├── evaluate.py           # Answer evaluation
│   │   ├── hr_questions.py      # HR/behavioral questions
│   │   └── improve.py            # Resume improvement
│   ├── services/                  # Business logic
│   │   ├── embedding_service.py  # Text embeddings
│   │   ├── vector_store.py       # FAISS vector storage
│   │   ├── llm_service.py        # LLM API service
│   │   └── pdf_service.py        # PDF text extraction
│   └── prompts/                   # Prompt templates
│       ├── question_generator.py  # Technical questions prompts
│       ├── hr_questions.py        # HR questions prompts
│       ├── answer_evaluator.py    # Answer evaluation prompts
│       └── resume_improver.py     # Resume improvement prompts
│
└── frontend/
    ├── package.json               # Node.js dependencies
    ├── vite.config.js            # Vite configuration
    ├── tailwind.config.js        # Tailwind CSS config
    ├── postcss.config.js         # PostCSS config
    ├── index.html                # HTML entry point
    ├── src/
    │   ├── main.jsx              # React entry point
    │   ├── App.jsx               # Main App component
    │   ├── index.css             # Global styles
    │   ├── services/
    │   │   └── api.js           # API service
    │   ├── components/
    │   │   ├── Navbar.jsx       # Navigation bar
    │   │   ├── Loading.jsx      # Loading component
    │   │   └── Error.jsx        # Error component
    │   └── pages/
    │       ├── Home.jsx          # Home page
    │       ├── UploadResume.jsx  # Resume upload page
    │       ├── Interview.jsx     # Mock interview page
    │       ├── HRQuestions.jsx  # HR questions page
    │       └── ResumeImprovement.jsx  # Resume improvement page
```

## ⚙️ Setup Instructions

### Backend Setup

1. **Navigate to backend directory:**
   
```
bash
   cd ai-interview-coach/backend
   
```

2. **Create virtual environment:**
   
```
bash
   python -m venv venv
   
```

3. **Activate virtual environment:**
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

4. **Install dependencies:**
   
```
bash
   pip install -r requirements.txt
   
```

5. **Configure environment variables:**
   
```
bash
   cp .env.example .env
   # Edit .env and add your API key
   OPENAI_API_KEY=your_api_key_here
   
```

6. **Run the backend server:**
   
```
bash
   python main.py
   # OR
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   
```

### Frontend Setup

1. **Navigate to frontend directory:**
   
```
bash
   cd ai-interview-coach/frontend
   
```

2. **Install dependencies:**
   
```
bash
   npm install
   
```

3. **Run the development server:**
   
```
bash
   npm run dev
   
```

4. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 📡 API Endpoints

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

## 📄 License

MIT License

## 👤 Author

AI Interview Coach Team
