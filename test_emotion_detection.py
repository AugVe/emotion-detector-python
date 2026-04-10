import unittest
from EmotionDetection.emotion_detection import emotion_detector

class TestEmotionDetection(unittest.TestCase):
    def test_emotion_detector(self):
        # Caso 1: Alegría
        result_1 = emotion_detector("I am glad this happened")
        self.assertEqual(result_1['dominant_emotion'], 'joy')
        
        # Caso 2: Rabia
        result_2 = emotion_detector("I am really mad about this")
        self.assertEqual(result_2['dominant_emotion'], 'anger')
        
        # Caso 3: Tristeza
        result_3 = emotion_detector("I am so sad about this")
        self.assertEqual(result_3['dominant_emotion'], 'sadness')

if __name__ == '__main__':
    unittest.main()