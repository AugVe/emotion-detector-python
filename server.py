from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
# Importamos tu función del paquete que creamos
from EmotionDetection.emotion_detection import emotion_detector

# 1. Creamos la instancia de la aplicación
app = FastAPI()

# 2. Configuramos el acceso a las carpetas que creaste
# Esto permite que el HTML encuentre al JS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Esto permite que FastAPI sepa dónde buscar el index.html
templates = Jinja2Templates(directory="templates")

# 3. RUTA PRINCIPAL: Lo que se ve al entrar a http://127.0.0.1:8000
@app.get("/", response_class=HTMLResponse)
async def render_index_page(request: Request):
    # Agregamos "context=" antes del diccionario
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={"request": request}
    )

# 4. RUTA DE ANÁLISIS: Donde el JS envía el texto
@app.get("/emotionDetector")
async def sent_detector(textToAnalyze: str):
    # 1. SEGURIDAD: Validamos antes de llamar a IBM (ahorra tiempo y errores)
    if not textToAnalyze or not textToAnalyze.strip():
        raise HTTPException(status_code=400, detail="Invalid text! Please try again!")

    # Llamamos a la lógica core de IBM
    response = emotion_detector(textToAnalyze)

    print(f"DEBUG: Texto enviado -> {textToAnalyze}")
    print(f"DEBUG: Respuesta de la función emotion_detector -> {response}")

    # 2. MANEJO DE ERROR PRO: Si IBM no pudo procesarlo
    if response is None or response.get('dominant_emotion') is None:
        raise HTTPException(status_code=400, detail="Invalid text! Please try again!")

    # 3. TU LÓGICA DE FORMATEO (Se queda igual porque tu JS la necesita)
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