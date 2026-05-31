from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from services.transcript import get_transcript
from services.ai import summarize, analyze_sentiment, generate_chapters, answer_question

app = FastAPI(
    title="YouTube Summarizer API",
    description="Summarize, analyze and chat with any YouTube video",
    version="1.0.0"
)

# CORS — allows your React frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Request Models ---

class VideoRequest(BaseModel):
    url: str
    language: str = "en"

class QuestionRequest(BaseModel):
    url: str
    question: str
    language: str = "en"


# --- Endpoints ---

@app.get("/")
def root():
    return {"message": "YouTube Summarizer API is running"}


@app.post("/summarize")
def summarize_video(request: VideoRequest):
    try:
        transcript_data = get_transcript(request.url, request.language)
        summary = summarize(transcript_data["full_text"])
        sentiment = analyze_sentiment(transcript_data["full_text"])
        chapters = generate_chapters(transcript_data["timestamped_segments"])

        return {
            "video_id": transcript_data["video_id"],
            "summary": summary,
            "sentiment": sentiment,
            "chapters": chapters,
            "language": transcript_data["language"]
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")


@app.post("/ask")
def ask_question(request: QuestionRequest):
    try:
        transcript_data = get_transcript(request.url, request.language)
        answer = answer_question(transcript_data["full_text"], request.question)

        return {
            "video_id": transcript_data["video_id"],
            "question": request.question,
            "answer": answer
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")