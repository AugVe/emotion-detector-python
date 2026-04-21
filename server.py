"""
Main FastAPI server for the Emotion Detector application.
Handles web routing and coordinates between the UI and the IBM Watson logic.
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from EmotionDetection.emotion_detection import emotion_detector

# Initialize the FastAPI application
app = FastAPI()

# Configure static files (JS, CSS) and template directory (HTML)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def render_home_page(request: Request):
    """
    Renders the main interface (index.html) of the application.
    """
    return templates.TemplateResponse(
            request=request, 
            name="index.html"
        )

@app.get("/emotionDetector")
async def analyze_emotion(textToAnalyze: str):
    """
    Endpoint that receives text, triggers the emotion analysis,
    and returns a formatted HTML response for the frontend.
    """
    
    # Validation: Check for empty or whitespace-only strings
    if not textToAnalyze or not textToAnalyze.strip():
        raise HTTPException(
            status_code=400, 
            detail="Invalid text! Please try again!"
        )

    # Invoke the IBM Watson analysis logic
    response = emotion_detector(textToAnalyze)

    # Error Handling: Verify if the external API returned a valid result
    if response is None or response.get('dominant_emotion') is None:
        raise HTTPException(
            status_code=400, 
            detail="Invalid text! Please try again!"
        )

    # Prepare the formatted output string for the UI
    formatted_result = (
        f"For the given sentence, the system response is:<br>"
        f"-  <b>Anger:</b> {response['anger']}<br>"
        f"-  <b>Disgust:</b> {response['disgust']}<br>"
        f"-  <b>Fear:</b> {response['fear']}<br>"
        f"-  <b>Joy:</b> {response['joy']}<br>"
        f"-  <b>Sadness:</b> {response['sadness']}<br><br>"
        f"The dominant emotion is <b>{response['dominant_emotion'].upper()}.</b>"
    )
    
    return {"result": formatted_result}