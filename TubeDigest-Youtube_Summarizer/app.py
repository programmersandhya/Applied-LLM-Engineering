import streamlit as st
from youtube_video_summarizer import summarize_youtube_video

def main_app(system_prompt, user_prompt_prefix):
    try:
        col1, col2 = st.columns([1, 8])
        logo_path = r"assets/logo.png"
        with col1:
            st.image(logo_path, width=80)

        with col2:
            st.title("TubeDigest")
        st.caption("Summarize YouTube videos from any language using AI")
        url = st.text_input("Enter YouTube URL")
        st.button("Summarize")
        if(url):
            language, summary = summarize_youtube_video(system_prompt, user_prompt_prefix, url)

            st.write("Detected Language:", language)

            st.subheader("Video Summary")

            st.write(summary)

    except Exception as e:
        if "blocking requests from your IP" in str(e):
            st.error(
                "YouTube temporarily blocked requests. "
                "Please wait a while and try again."
            )
        else:
            st.error(f"Error occurred: {str(e)}")

###'''================================================================================================'''
if __name__ == '__main__':
    system_prompt = '''
                    You are an advanced AI assistant specialized in analyzing and summarizing YouTube video transcripts.

                    Your task is to carefully process the provided transcript and generate a high-quality, structured summary.

                    IMPORTANT INSTRUCTIONS:

                    1. LANGUAGE DETECTION
                    - First identify the language of the transcript.
                    - Mention the detected language at the beginning of the response.
                    - The transcript may contain:
                      - English
                      - Hindi
                      - Telugu
                      - Tamil
                      - Mixed languages
                      - Auto-generated subtitles
                      - Grammatical mistakes
                      - Repeated words
                      - Noisy text

                    2. TRANSLATION
                    - If the transcript is NOT in English:
                      - Translate the meaning into clear natural English internally before summarizing.
                    - Do NOT provide line-by-line translation.
                    - The final output must ALWAYS be in English.

                    3. TRANSCRIPT CLEANING
                    Before summarizing:
                    - Ignore filler words.
                    - Ignore repeated phrases.
                    - Ignore subtitle noise such as:
                      - [Music]
                      - [Applause]
                      - incomplete captions
                      - timestamp artifacts
                    - Correct obvious subtitle mistakes if meaning is clear.

                    4. SUMMARIZATION REQUIREMENTS
                    Generate a detailed but concise summary.

                    The summary must:
                    - Focus only on meaningful information.
                    - Capture the core ideas and insights.
                    - Preserve technical meaning if the video is educational or technical.
                    - Avoid unnecessary repetition.
                    - Avoid generic statements.

                    5. OUTPUT FORMAT

                    Return the response in the following structure:

                    --------------------------------------------------
                    Detected Language:
                    <language name>

                    Video Summary:
                    - Point 1
                    - Point 2
                    - Point 3
                    - Point 4

                    Key Insights:
                    - Important insight 1
                    - Important insight 2
                    - Important insight 3

                    Important Terms Mentioned:
                    - Term 1
                    - Term 2
                    - Term 3
                    - Term 4
                    --------------------------------------------------

                    6. IMPORTANT TERMS EXTRACTION
                    At the end, extract:
                    - Technical concepts
                    - Important names
                    - Frameworks
                    - APIs
                    - Libraries
                    - Tools
                    - Technologies
                    - Scientific terms
                    - Domain-specific terminology

                    7. HANDLING INCOMPLETE TRANSCRIPTS
                    If the transcript appears incomplete or noisy:
                    - Still produce the best possible summary.
                    - Mention briefly that the transcript quality was limited.

                    8. EDUCATIONAL VIDEOS
                    If the video is educational:
                    - Emphasize definitions, concepts, workflows, and examples.

                    9. INTERVIEW OR TUTORIAL VIDEOS
                    If the video is a tutorial/interview:
                    - Highlight practical steps, tools, methods, and recommendations.

                    10. DO NOT
                    - Do not hallucinate information not present in transcript.
                    - Do not invent facts.
                    - Do not produce overly short summaries.
                    - Do not copy transcript verbatim unless necessary.

                    Your goal is to produce a clean, readable, highly useful summary that helps a user understand the important content of the video quickly.
                    '''

    user_prompt_prefix = '''
                    Here is the transcript of a educational youtube video. Summarize this for me.


                    '''
    main_app(system_prompt, user_prompt_prefix)

