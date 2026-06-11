# ✈️ PaperPilot-AI

PaperPilot-AI is an advanced, multi-agent academic paper analysis platform designed to turn static scientific PDFs into interactive, structured study companions. 

By leveraging retrieval-augmented generation (RAG), local vector search, and LLM orchestration, PaperPilot-AI delivers comprehensive insights, interactive quizzes, flashcards, study guides, and context-aware Q&A directly from the browser.

---

## 🚀 Key Features

* **📑 AI Report Generator**: Automatically produces structured, academic summaries covering **Overview**, **Methodology**, **Results**, **Benchmarks**, **Limitations**, and **Key Takeaways**.
* **💬 Chat with Paper (RAG)**: Ask context-grounded questions about any uploaded paper. Answers are retrieved via a local **FAISS** index built on top of embedding layers.
* **🧠 Interactive Quizzes**: Test your reading comprehension with AI-generated, 5-question multiple-choice quizzes complete with correct answers and logical explanations.
* **🃏 Key Concept Flashcards**: Interactive, flipping 3D digital cards with key terms and definitions extracted from the paper text.
* **📖 Structured Study Guides**: Generates customized reading strategies, prerequisite checkups, discussion topics, and practical exercises.
* **🔄 Refresh & Regenerate**: Easily delete existing quizzes, flashcards, or study guides to regenerate fresh variants using updated LLM outputs.
* **🔍 Dashboard Search & Filter**: Search, track, and filter all analyzed papers dynamically on the home dashboard.
* **📥 PDF Report Downloads**: Download generated reports as clean, offline PDFs.

---

## 🛠️ Technology Stack

### Backend
* **Core Framework**: FastAPI (Python 3.12)
* **Agent Engine**: Groq API (`llama-3.3-70b-versatile`)
* **Vector Database & RAG**: FAISS (IndexFlatIP) + SentenceTransformers (`all-MiniLM-L6-v2`)
* **Database & Auth**: Supabase (PostgreSQL with RLS policy & Supabase Auth)

### Frontend
* **Core UI**: React.js (Vite + modern ES6)
* **Design & Styling**: Vanilla CSS, Glassmorphic layouts, and subtle responsive micro-animations
* **Icons**: Lucide React
* **State Management & Client**: Axios, local state, and context

---

## ⚙️ Project Setup

### Prerequisites
* Python 3.12+
* Node.js (v18+)
* Supabase Account
* Groq API Key

---

### Backend Setup

1. **Navigate to the Backend Directory**:
   ```bash
   cd backend
   ```

2. **Create a Virtual Environment & Activate**:
   ```bash
   # On Windows (CMD/PowerShell)
   python -m venv venv
   ..\venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**:
   Create a `.env` file in the project root:
   ```env
   SUPABASE_URL=your_supabase_project_url
   SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
   GROQ_API_KEY=your_groq_api_key
   GROQ_MODEL=llama-3.3-70b-versatile
   ```

5. **Database Initialization**:
   Execute the queries in `supabase_setup.sql` in your Supabase SQL Editor to initialize the necessary tables (`papers`, `reports`, `quizzes`, `flashcards`, `study_advice`, `chat_history`).

---

### Frontend Setup

1. **Navigate to the Frontend Directory**:
   ```bash
   cd frontend
   ```

2. **Install Dependencies**:
   ```bash
   npm install
   ```

3. **Environment Variables**:
   Create a `.env` file in the `frontend` folder:
   ```env
   VITE_API_URL=http://localhost:8000
   VITE_SUPABASE_URL=your_supabase_project_url
   VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
   ```

---

## 🏃 Running the Application

You can launch both the backend and frontend services using the provided launcher scripts at the root directory:

* **Windows Command Prompt**:
  ```cmd
  run.bat
  ```
* **Windows PowerShell**:
  ```powershell
  ./run.ps1
  ```

Once running, the application will be accessible at:
* **Frontend**: `http://localhost:5173`
* **Backend Docs (FastAPI)**: `http://localhost:8000/docs`
