"""
Unit tests for the Emotion Detection logic.
Ensures that the IBM Watson API integration correctly identifies 
dominant emotions across different scenarios.
"""

import unittest
from EmotionDetection.emotion_detection import emotion_detector

class TestEmotionDetection(unittest.TestCase):
    """
    Test suite for verifying the accuracy of the emotion_detector function.
    """

    def test_emotion_detector_accuracy(self):
        """
        Tests various input sentences to verify that the correct 
        dominant emotion is identified for each case.
        """
        
        # Test Case 1: Joy
        result_1 = emotion_detector("I am glad this happened")
        self.assertEqual(result_1['dominant_emotion'], 'joy')
        
        # Test Case 2: Anger
        result_2 = emotion_detector("I am really mad about this")
        self.assertEqual(result_2['dominant_emotion'], 'anger')
        
        # Test Case 3: Disgust
        result_3 = emotion_detector("I feel disgusted just hearing about this")
        self.assertEqual(result_3['dominant_emotion'], 'disgust')
        
        # Test Case 4: Sadness
        result_4 = emotion_detector("I am so sad about this")
        self.assertEqual(result_4['dominant_emotion'], 'sadness')
        
        # Test Case 5: Fear
        result_5 = emotion_detector("I am really afraid that this will happen")
        self.assertEqual(result_5['dominant_emotion'], 'fear')

if __name__ == '__main__':
    unittest.main()