# Video Q&A Assistant (Streamlit)

This project is a web-based video analysis assistant that enables natural-language questioning over uploaded video files using Google Gemini’s native multimodal capabilities (**Gemini 2.5 Flash**).

The system allows users to upload a video and ask arbitrary questions about its content, with responses generated directly from visual and audio understanding of the video.

---

## What it does

- Accepts video uploads (MP4, MOV, AVI) up to 50 MB  
- Uploads and processes videos using the Gemini Files API  
- Uses **Gemini 2.5 Flash** for fast, cost-efficient multimodal inference  
- Supports free-form natural-language questions about video content  
- Generates answers, explanations, and summaries grounded in the video  
- Provides a simple, interactive web UI using Streamlit  

---

## High-level architecture

### 1. Upload & Validation
- User uploads a video via the Streamlit interface  
- File size and format are validated before processing  

### 2. Video Processing
- Video is uploaded to the Gemini Files API  
- Processing state is monitored until the video is ready for inference  

### 3. Query & Analysis
- User questions are combined with the uploaded video reference  
- **Gemini 2.5 Flash** analyzes both visual and audio content to answer the query  

### 4. Response
- The model generates a grounded response based on video content  
- Results are displayed directly in the UI  

---

## Notes

- Designed as a learning and experimentation project for multimodal AI workflows  
- Focuses on native video understanding rather than transcript-only approaches  
- Includes safeguards such as file size limits to control usage and cost  
- Built for easy cloud deployment using Streamlit Community Cloud  

---

## Setup

Detailed setup instructions, environment configuration, and deployment details are available on request.
