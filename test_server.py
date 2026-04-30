"""
Unit tests for the Emotion Detector FastAPI server.
This suite covers endpoint availability, input validation,
and error handling using a mocked environment for external dependencies.
"""

from fastapi.testclient import TestClient
from unittest.mock import patch
from server import app

# Initialize the TestClient for internal request simulation
client = TestClient(app)


def test_emotion_detector_success():
    """
    Test the successful emotion analysis flow.
    Uses 'unittest.mock.patch' to simulate the IBM Watson API response,
    ensuring the test remains independent of network state and credentials.
    """
    mock_watson_data = {
        'anger': 0.01,
        'disgust': 0.02,
        'fear': 0.03,
        'joy': 0.90,
        'sadness': 0.04,
        'dominant_emotion': 'joy'
    }

    # Patching the emotion_detector function inside the server module
    with patch("server.emotion_detector") as mock_api:
        mock_api.return_value = mock_watson_data

        response = client.get(
            "/emotionDetector?textToAnalyze=I%20love%20coding"
        )

        assert response.status_code == 200
        assert "result" in response.json()
        assert "JOY" in response.json()["result"]


def test_emotion_detector_empty_input():
    """
    Verify that providing an empty string triggers the correct error response.
    Validates that the Global Exception Handler correctly formats
    InvalidInputError.
    """
    response = client.get("/emotionDetector?textToAnalyze=")

    assert response.status_code == 422
    assert "detail" in response.json()


def test_emotion_detector_whitespace_only():
    """
    Ensure that inputs consisting only of whitespace characters are rejected.
    This still hits our manual 400 error because
    strip() happens inside our code.
    """
    response = client.get("/emotionDetector?textToAnalyze=%20%20%20")

    assert response.status_code == 400
    assert response.json()["status"] == "error"


def test_health_check():
    """
    Validate the operational status of the application via the health endpoint.
    Ensures that monitoring tools can verify server availability.
    """
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
