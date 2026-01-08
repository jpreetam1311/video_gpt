import streamlit as st
from google import genai
from google.genai import types


 
import time
from pathlib import Path

import tempfile

import os
from dotenv import load_dotenv

load_dotenv()  # local development

API_KEY = None

# Try Streamlit Secrets (only works if secrets.toml exists)
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except Exception:
    pass

# Fallback to environment variable (.env)
if not API_KEY:
    API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error(
        "GOOGLE_API_KEY is missing.\n\n"
        "• Locally: add it to a .env file\n"
        "• On Streamlit Cloud: add it in App → Settings → Secrets"
    )
    st.stop()


client = genai.Client(
    api_key=API_KEY
)


def upload_file(file_path: str):
    # NOTE: use file= ... not path=
    return client.files.upload(file=file_path)

def get_file(name: str):
    return client.files.get(name=name)


# Page configuration
st.set_page_config(
    page_title="Mutimodal AI Video Analysis Agent",
    page_icon=" 🤖",
    layout="wide"
)

st.title("AI Video Analysis Agent🤖🎥")
st.header("Upload a video to get inights!")
st.info("⚠️ Note: Videos larger than 50 MB are not supported.")



#File uploader

video_file = st.file_uploader(
    "Upload a video file", type=["mp4", "mov", "avi",], help="Upload a video file in mp4, mov, or avi format."
)

if video_file:
    # Enforce file size limit
    if video_file.size > MAX_FILE_SIZE_BYTES:
        st.error(
            f"❌ File too large ({video_file.size / (1024*1024):.1f} MB). "
            f"Maximum allowed size is {MAX_FILE_SIZE_MB} MB."
        )
        st.stop()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        temp_video.write(video_file.read())
        video_path = temp_video.name


    st.video(video_path, format="video/mp4", start_time=0)

    user_query = st.text_area(
        "Enter your query about the video:", 
        placeholder="Ask anything about the video content...",
        help = "Provide specific questions or insights you want from the video."
    )    

    if st.button("🔍Analyse Video", key="analyze_button"):
        if not user_query:
            st.warning("Please enter a query to analyze the video.")
        else:
            try:
                with st.spinner("Processing the video and gathering insights..."):
                    # Upload and process video file
                    processed_video = upload_file(video_path)

                    while processed_video.state.name == "PROCESSING":
                        time.sleep(1)
                        processed_video = get_file(processed_video.name)

                    analysis_prompt = f"""
                You are a helpful video summarizer.
                Analyze the uploaded video and answer the user's question based on what happens in the video.

                USER QUESTION:
                {user_query}

                Return a clear, detailed answer with key points and a short summary at the end.
                """.strip()

                    # ✅ IMPORTANT: use the EXACT model name from your list
                    response = client.models.generate_content(
                        model="models/gemini-2.5-flash",
                        contents=[
                            types.Content(
                                role="user",
                                parts=[
                                    types.Part(text=analysis_prompt),
                                    # ✅ Attach the uploaded video file to the prompt
                                    types.Part.from_uri(
                                                        file_uri=processed_video.uri,
                                                        mime_type=getattr(processed_video, "mime_type", "video/mp4"),
                                                        ),
                                ],
                            )
                        ],
                    )

                st.subheader("Analysis Result")
                st.markdown(response.text)

            except Exception as error:
                st.error(f"An error occurred during video analysis: {error}")
            finally:
                # Clean up temporary video file
                Path(video_path).unlink(missing_ok=True)
else:
    st.info("Please upload a video file to get started.")

# Customize text area height
st.markdown(
    """
    <style>
    .stTextArea textarea{
        height: 150px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
