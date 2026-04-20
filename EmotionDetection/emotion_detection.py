import requests
import json
from dotenv import load_dotenv
import os

def emotion_detector(text_to_analyze):
    # La URL base que me pasaste + el endpoint de análisis
    url = os.getenv("WATSON_URL")
    
    # Reemplaza 'TU_API_KEY_AQUI' con la clave que te dio IBM
    api_key = os.getenv("WATSON_API_KEY")
    
    # Estructura de datos que pide IBM Watson Natural Language Understanding
    header = {"Content-Type": "application/json"}
    payload = {
        "text": text_to_analyze,
        "features": {
            "emotion": {}
        }
    }
    
    
    try:
            response = requests.post(url, json=payload, headers=header, auth=('apikey', api_key))
            
            if response.status_code == 200:
                full_response = response.json()
                emotions = full_response['emotion']['document']['emotion']
                dominant_emotion = max(emotions, key=emotions.get)
                
                return {
                    'anger': emotions['anger'],
                    'disgust': emotions['disgust'],
                    'fear': emotions['fear'],
                    'joy': emotions['joy'],
                    'sadness': emotions['sadness'],
                    'dominant_emotion': dominant_emotion
                }
            else:
                # Esto saldrá en los logs de Render si IBM falla
                print(f"ERROR IBM: Status {response.status_code} - {response.text}")
                return None
    except Exception as e:
        print(f"ERROR CONEXION: {e}")
        return None