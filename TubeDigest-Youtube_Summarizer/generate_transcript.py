import re
from youtube_transcript_api import YouTubeTranscriptApi
import streamlit as st

def generate_transcript(youtube_url):
    try:
        # Validate URL
        if not is_valid_youtube_url(youtube_url):
            print("Invalid YouTube URL")

        else:
            # Extract Video ID
            video_id = extract_video_id(youtube_url)

            if not video_id:
                print("Could not extract video ID")
                return False
            else:
                print(f"Video ID: {video_id}")

                # Fetch Transcript
                transcript_text = get_transcript(video_id)

                print("\nTranscript:\n")
                print(transcript_text[:3000])  # print first 3000 chars
                return transcript_text

    except Exception as e:
        return f"Exception at generate_transcript : {str(e)}"


def is_valid_youtube_url(url):
    pattern = r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/"
    return re.match(pattern, url) is not None


def extract_video_id(url):
    patterns = [
        r"v=([a-zA-Z0-9_-]{11})",          # youtube.com/watch?v=
        r"youtu\.be/([a-zA-Z0-9_-]{11})", # youtu.be/
        r"embed/([a-zA-Z0-9_-]{11})"      # embed/
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None


@st.cache_data
def get_transcript(video_id):
    try:
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)

        transcript_obj = next(iter(transcript_list))
        language = transcript_obj.language
        language_code = transcript_obj.language_code

        transcript = transcript_obj.fetch()
        full_text = " ".join([entry.text for entry in transcript])

        return [language, full_text]

    except Exception as e:
        return f"Error fetching transcript: {e}"


