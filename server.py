"""
Main FastAPI server for the Emotion Detector application.
Handles web routing and coordinates between the UI and the IBM Watson logic.
"""

import uvicorn
import os
import logging
import sys
from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from EmotionDetection.emotion_detection import emotion_detector

# --- LOGGING CONFIGURATION ---
# Configure logging to output to stdout (visible in Docker/Render logs)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("emotion-detector-server")

# --- CUSTOM EXCEPTIONS (The Hierarchy) ---

class EmotionAppError(Exception):
    """Base class for all exceptions in this application."""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class WatsonServiceError(EmotionAppError):
    """Raised when the external IBM Watson API fails."""
    pass

class InvalidInputError(EmotionAppError):
    """Raised when the user provides invalid text."""
    pass

# --- SCHEMAS  ---
class AnalysisResponse(BaseModel):
    """Schema for the successful emotion analysis response."""
    result: str = Field(
        ..., 
        example="For the given sentence, the system response is: Anger: 0.1, ... The dominant emotion is JOY."
    )

class ErrorResponse(BaseModel):
    """Standardized error response format."""
    detail: str
    status: str = "error"

# --- APP INSTANCE ---
app = FastAPI(
    title="Emotion Detector API 🤖",
    description="""
    Professional API for text emotion analysis using IBM Watson.
    
    * **Reliable:** Built-in error handling and logging.
    * **Documented:** Fully compliant with OpenAPI/Swagger standards.
    * **Optimized:** Lightweight container-ready architecture.
    """,
    version="1.1.0",
    contact={
        "name": "Augusto",
        "url": "https://github.com/AugVe",
    }
)

# --- GLOBAL EXCEPTION HANDLER ---

@app.exception_handler(EmotionAppError)
async def emotion_app_exception_handler(request: Request, exc: EmotionAppError):
    """
    Catches any EmotionAppError (or its children) raised anywhere in the app.
    Logs the incident and returns a standardized JSON response.
    """
    logger.error(f"Application Error: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message, "status": "error"}
    )

# Configure static files (JS, CSS) and template directory (HTML)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def render_home_page(request: Request):
    """
    Renders the main interface (index.html) of the application.
    """
    return templates.TemplateResponse(
        request=request, 
        name="index.html"
    )

@app.get(
    "/emotionDetector", 
    response_model=AnalysisResponse, 
    tags=["Analysis"]
)
async def analyze_emotion(
    textToAnalyze: str = Query(..., description="The text string to be analyzed by the AI model")
):
    """
    Endpoint that receives text, triggers the emotion analysis,
    and returns a formatted HTML response for the frontend.
    """
    logger.info(f"Received analysis request for text: '{textToAnalyze[:30]}...'")

    # Validation: Check for empty or whitespace-only strings
    if not textToAnalyze or not textToAnalyze.strip():
        logger.warning("Empty text provided for analysis.")
        raise InvalidInputError("Invalid text! Please try again!")

    # Invoke the IBM Watson analysis logic
    
    response = emotion_detector(textToAnalyze)


    # Error Handling: Verify if the external API returned a valid result
    if response is None or response.get('dominant_emotion') is None:
        logger.error("AI model returned an invalid or null response.")
        raise WatsonServiceError("Invalid text! Please try again!", status_code=400)

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
    
    logger.info(f"Analysis successful. Dominant emotion: {response['dominant_emotion']}")
    return {"result": formatted_result}

@app.get("/health", tags=["Maintenance"])
async def health_check():
    """
    Health check endpoint to verify that the server is running correctly.
    Used by the cloud provider to monitor application stability.
    """
    logger.debug("Health check requested.")
    return {"status": "ok"}

if __name__ == "__main__":
    """
    Main entry point for the application.
    Configures the server to run on a globally accessible host 
    and handles dynamic port assignment for cloud deployment.
    """
    
    # Retrieve the port from the environment variable 'PORT' (provided by Render)
    # Default to 8000 if the variable is not set (e.g., during local development)
    port = int(os.environ.get("PORT", 8000))
    
    # Start the Uvicorn server
    # 'host="0.0.0.0"' ensures the application is reachable from outside the container
    logger.info(f"Starting server on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)