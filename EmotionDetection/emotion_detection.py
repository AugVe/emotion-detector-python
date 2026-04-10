import requests
import json

def emotion_detector(text_to_analyze):
    # La URL base que me pasaste + el endpoint de análisis
    url = "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/7d2350d8-16f0-4cb6-a236-e7da9282c6a5/v1/analyze?version=2022-04-07"
    
    # Reemplaza 'TU_API_KEY_AQUI' con la clave que te dio IBM
    api_key = "D3ypmjpuF9XG-0o3ANGPXT-OTQTF60Hg8rg99nLanm7J"
    
    # Estructura de datos que pide IBM Watson Natural Language Understanding
    header = {"Content-Type": "application/json"}
    payload = {
        "text": text_to_analyze,
        "features": {
            "emotion": {}
        }
    }
    
    # Hacemos la petición usando autenticación básica (apikey)
    response = requests.post(url, json=payload, headers=header, auth=('apikey', api_key))
    
    if response.status_code == 200:
        full_response = response.json()
        # Extraemos las emociones del formato de IBM
        emotions = full_response['emotion']['document']['emotion']
        
        # Encontramos la emoción dominante
        dominant_emotion = max(emotions, key=emotions.get)
        
        # Retornamos el diccionario como lo espera tu server.py
        return {
            'anger': emotions['anger'],
            'disgust': emotions['disgust'],
            'fear': emotions['fear'],
            'joy': emotions['joy'],
            'sadness': emotions['sadness'],
            'dominant_emotion': dominant_emotion
        }
    else:
        return None