import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.1-8b-instant"


def _ask(prompt: str) -> str:
    """
    Internal helper — sends a prompt to Groq and returns the text response.
    All other functions use this instead of repeating the same API call.
    """
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return response.choices[0].message.content


def summarize(transcript: str) -> str:
    """
    Sends transcript to Groq and returns a clean summary.
    """
    prompt = f"""
    You are an expert at summarizing YouTube videos.
    
    Given the transcript below, provide:
    1. A concise summary (3-5 sentences)
    2. 5 key takeaways as bullet points
    
    Transcript:
    {transcript}
    
    Respond in this exact format:
    SUMMARY:
    <your summary here>
    
    KEY TAKEAWAYS:
    - <point 1>
    - <point 2>
    - <point 3>
    - <point 4>
    - <point 5>
    """
    return _ask(prompt)


def analyze_sentiment(transcript: str) -> str:
    """
    Analyzes the overall sentiment and tone of the video.
    """
    prompt = f"""
    Analyze the sentiment and tone of this YouTube video transcript.
    
    Provide:
    1. Overall sentiment (Positive / Negative / Neutral / Mixed)
    2. Emotional tone (e.g. educational, motivational, critical, humorous)
    3. One sentence explanation of why
    
    Transcript:
    {transcript}
    
    Respond in this exact format:
    SENTIMENT: <value>
    TONE: <value>
    REASON: <one sentence>
    """
    return _ask(prompt)


def generate_chapters(timestamped_segments: list) -> str:
    """
    Generates chapter markers from timestamped transcript segments.
    """
    formatted = "\n".join(
        f"[{seg['start']}s] {seg['text']}"
        for seg in timestamped_segments[:200]
    )

    prompt = f"""
    You are given timestamped segments of a YouTube video transcript.
    Identify 5-8 natural chapter breaks and give each a short title.
    
    Segments:
    {formatted}
    
    Respond in this exact format:
    CHAPTERS:
    - [Xs] Chapter Title
    - [Xs] Chapter Title
    (where X is the timestamp in seconds)
    """
    return _ask(prompt)


def answer_question(transcript: str, question: str) -> str:
    """
    Answers a user question based ONLY on the video transcript.
    """
    prompt = f"""
    You are a helpful assistant. Answer the user's question 
    based ONLY on the video transcript provided.
    If the answer is not in the transcript, say so clearly.
    
    Transcript:
    {transcript}
    
    User Question:
    {question}
    
    Answer:
    """
    return _ask(prompt)


if __name__ == "__main__":
    from transcript import get_transcript

    result = get_transcript("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    print("=== SUMMARY ===")
    print(summarize(result["full_text"]))

    print("\n=== SENTIMENT ===")
    print(analyze_sentiment(result["full_text"]))

    print("\n=== CHAPTERS ===")
    print(generate_chapters(result["timestamped_segments"]))