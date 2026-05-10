import openai
from dotenv import load_dotenv
import os
from IPython.display import Markdown, display
from generate_transcript import generate_transcript


def summarize_youtube_video(system_prompt, user_prompt_prefix, url):
    try:
        api_key_status = check_api_key()
        if(api_key_status):
            video_summary = summarize(system_prompt, user_prompt_prefix, url)
            return video_summary
        else:
            return "Check the api key in .env file"
    except Exception as e:
        return f"Exception at summarize_youtube_video : {str(e)}"

def messages_for(system_prompt, user_prompt_prefix, transcript):
    try:
        print("Initializing the prompts")
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt_prefix + transcript}
        ]
    except Exception as e:
        return f"Exception at messages : {str(e)}"


def summarize(system_prompt, user_prompt_prefix, url):
    try:
        print('Initiating summarization')
        transcript_details = generate_transcript(url)
        language_detected = transcript_details[0]
        transcript = transcript_details[1]
        messages = messages_for(system_prompt, user_prompt_prefix, transcript)
        print(f"messages : {messages}")
        summary = (openai.chat.completions.create(
                                    model="gpt-4.1-mini",
                                    messages=messages
                                            ))
        video_summary = summary.choices[0].message.content
        return [language_detected, video_summary]
    except Exception as e:
        return f"Exception at summarize : {str(e)}"

def check_api_key():
    try:
        # Load environment variables in a file called .env

        load_dotenv(override=True)
        api_key = os.getenv('OPENAI_API_KEY')

        # Check the key

        if not api_key:
            print(
                "No API key was found - please head over to the troubleshooting notebook in this folder to identify & fix!")
            return False
        elif not api_key.startswith("sk-proj-"):
            print(
                "An API key was found, but it doesn't start sk-proj-; please check you're using the right key - see troubleshooting notebook")
            return False
        elif api_key.strip() != api_key:
            print(
                "An API key was found, but it looks like it might have space or tab characters at the start or end - please remove them - see troubleshooting notebook")
            return False
        else:
            print("API key found and looks good so far!")
            return True
    except Exception as e:
        return f"Exception at check_api_key: {str(e)}"
