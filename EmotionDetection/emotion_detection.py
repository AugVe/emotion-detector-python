import os
import requests
from typing import Dict, Any, Optional


# --- CONSTANTS ---
WATSON_VERSION = "2022-04-07"


def emotion_detector(text_to_analyze: str) -> Optional[Dict[str, Any]]:
    """
    Analyzes the emotional content of text using IBM Watson NLP API.

    Args:
        text_to_analyze (str): The input text to be processed.

    Returns:
        Optional[Dict[str, Any]]: A dictionary with the following structure:
            {
                'anger': float, 'disgust': float, 'fear': float,
                'joy': float, 'sadness': float, 'dominant_emotion': str
            }
            Returns None if the request fails or URL/API Key are missing.
    """

    # Retrieve environment variables
    url = os.getenv("WATSON_URL")
    api_key = os.getenv("WATSON_API_KEY")

    # Ensure both URL and API key are available before proceeding
    if not url or not api_key:
        return None

    # Format the URL and ensure the required version parameter is included
    base_url = url.rstrip('/')
    if "/v1/analyze" not in base_url:
        full_url = f"{base_url}/v1/analyze?version={WATSON_VERSION}"
    else:
        full_url = base_url

    # Define request headers and payload structure for IBM Watson
    headers = {"Content-Type": "application/json"}
    payload = {
        "text": text_to_analyze,
        "features": {
            "emotion": {}
        }
    }

    try:
        # Execute the POST request using Basic Authentication
        response = requests.post(
            full_url,
            json=payload,
            headers=headers,
            auth=('apikey', api_key),
            timeout=10
        )

        # Process successful response
        if response.status_code == 200:
            full_response = response.json()
            emotions = full_response['emotion']['document']['emotion']

            # Identify the emotion with the highest score
            dominant_emotion = max(emotions, key=emotions.get)

            return {
                'anger': emotions['anger'],
                'disgust': emotions['disgust'],
                'fear': emotions['fear'],
                'joy': emotions['joy'],
                'sadness': emotions['sadness'],
                'dominant_emotion': dominant_emotion
            }

        # Handle API-specific errors (e.g., 401, 404, 400)
        return None

    except requests.exceptions.RequestException:
        # Silently handle connection errors to maintain service stability
        return None
