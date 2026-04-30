import unittest
from unittest.mock import patch
from EmotionDetection import emotion_detection


"""
Unit tests for the Emotion Detection logic.
Ensures that the IBM Watson API integration correctly identifies
dominant emotions across different scenarios.
"""

"""
Unit tests for the Emotion Detection logic.
Ensures that the IBM Watson API integration correctly identifies
dominant emotions across different scenarios.
"""


class TestEmotionDetection(unittest.TestCase):
    """
    Unit tests for the underlying emotion detection logic.
    Uses mocking to ensure tests are deterministic and do not require API keys.
    """

    @patch("EmotionDetection.emotion_detection.emotion_detector")
    def test_emotion_detector_accuracy(self, mock_detector):
        """
        Verify that the logic correctly identifies dominant emotions.
        """
        # Case 1: Joy
        mock_detector.return_value = {'dominant_emotion': 'joy'}
        result = emotion_detection.emotion_detector("I am glad this happened")
        self.assertEqual(result['dominant_emotion'], 'joy')

        # Case 2: Anger
        mock_detector.return_value = {'dominant_emotion': 'anger'}
        result = emotion_detection.emotion_detector(
            "I am really mad about this"
        )
        self.assertEqual(result['dominant_emotion'], 'anger')

    @patch("EmotionDetection.emotion_detection.emotion_detector")
    def test_emotion_detector_invalid_input(self, mock_detector):
        """
        Verify the behavior when the API returns None (e.g., empty input).
        """
        mock_detector.return_value = None
        result = emotion_detection.emotion_detector("")
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
