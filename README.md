# Emotion Detector API 🤖🧠

Este proyecto es una aplicación web interactiva que utiliza Inteligencia Artificial (IBM Watson Natural Language Understanding) para analizar las emociones en un texto proporcionado por el usuario.

## ✨ Características
- **Backend:** Desarrollado con **FastAPI** (Python).
- **IA:** Integración con la API de **IBM Watson** para detección de emociones (Anger, Disgust, Fear, Joy, Sadness).
- **Frontend:** Interfaz limpia construida con HTML, CSS y JavaScript (Vanilla JS).
- **Comunicación:** Uso de `fetch` para peticiones asíncronas sin recargar la página.

## 🚀 Cómo ejecutar el proyecto

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/AugVe/emotion-detector-python.git](https://github.com/AugVe/emotion-detector-python.git)

2. **Crear y activar un Entorno Virtual**
Esto asegura que las librerías del proyecto no interfieran con otras aplicaciones de tu sistema:

- **Crear el entorno:** `python -m venv venv`
- **Activar en Mac/Linux:** `source venv/bin/activate`
- **Activar en Windows:** `venv\Scripts\activate`

3. **Instalar las dependencias**
Una vez activado el entorno, instala automáticamente FastAPI, Requests y Uvicorn:

```bash
pip install -r requirements.txt
```

4. **Configurar la API Key**
Debes tener una instancia de **Natural Language Understanding** en IBM Cloud. 
Edita el archivo `EmotionDetection/emotion_detection.py` y coloca tu propia **API Key** y **URL** en las variables correspondientes.

5. **Ejecutar la aplicación**
Inicia el servidor local de FastAPI con el siguiente comando:

```bash
uvicorn server:app --reload
```

Finalmente, abre tu navegador y ve a: [http://127.0.0.1:8000](http://127.0.0.1:8000)