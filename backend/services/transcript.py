from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound


def extract_video_id(url: str) -> str:
    """
    Extracts the video ID from a YouTube URL.
    Supports formats:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    """
    if "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    elif "watch?v=" in url:
        return url.split("watch?v=")[1].split("&")[0]
    else:
        raise ValueError(f"Could not extract video ID from URL: {url}")


def get_transcript(url: str, language: str = "en") -> dict:
    """
    Fetches the transcript of a YouTube video.
    Returns a dict with full text and timestamped segments.
    """
    video_id = extract_video_id(url)

    try:
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)
        transcript = transcript_list.find_transcript([language, "en"])
        transcript_segments = transcript.fetch()

        # Convert FetchedTranscript object to list of dicts
        segments_data = [
            {"text": s.text, "start": s.start, "duration": s.duration}
            for s in transcript_segments
        ]

    except TranscriptsDisabled:
        raise ValueError("This video has transcripts disabled by the creator.")
    except NoTranscriptFound:
        raise ValueError(f"No transcript found for language: {language}")

    # Full transcript as one string
    full_text = " ".join(
        segment["text"] for segment in segments_data
    )

    # Keep timestamps for chapters feature later
    timestamped = [
        {
            "start": round(segment["start"]),
            "text": segment["text"]
        }
        for segment in segments_data
    ]

    return {
        "video_id": video_id,
        "full_text": full_text,
        "timestamped_segments": timestamped,
        "language": language
    }

if __name__ == "__main__":
    result = get_transcript("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    print(result["video_id"])
    print(result["full_text"][:200])  # first 200 characters
    print(f"Total segments: {len(result['timestamped_segments'])}")