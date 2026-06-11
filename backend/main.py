import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

from api import auth, paper, report, quiz, flashcard, study_advice, chat

app = FastAPI(
    title="PaperPilot-AI API",
    description="Multi-agent academic paper analysis platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        os.getenv("FRONTEND_URL", "http://localhost:5173"),
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(paper.router, prefix="/paper", tags=["Papers"])
app.include_router(report.router, prefix="/report", tags=["Reports"])
app.include_router(quiz.router, prefix="/paper", tags=["Quiz"])
app.include_router(flashcard.router, prefix="/paper", tags=["Flashcards"])
app.include_router(study_advice.router, prefix="/paper", tags=["Study Advice"])
app.include_router(chat.router, prefix="/paper", tags=["Chat"])


@app.get("/", tags=["Health"])
def root():
    return {"message": "PaperPilot-AI API is running", "version": "1.0.0"}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}
