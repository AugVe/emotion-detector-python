// 1. Definimos la función que se activa al hacer clic en el botón
let analyzeEmotion = () => {
    
    // 2. Capturamos el texto que el usuario escribió en el área de texto
    // Usamos el ID "textToAnalyze" que definimos en el index.html
    let textToAnalyze = document.getElementById("textToAnalyze").value;

    // 3. Preparamos el envío al servidor
    // 'fetch' inicia una petición HTTP a la ruta que creamos en server.py
    // 'encodeURIComponent' asegura que si hay espacios o símbolos, la URL no se rompa
    fetch(`/emotionDetector?textToAnalyze=${encodeURIComponent(textToAnalyze)}`)
        
        // 4. Primer paso de la respuesta: el servidor responde que recibió el mensaje
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la comunicación con el servidor');
            }
            return response.json(); // Convertimos la respuesta de Python en un objeto JS
        })

        // 5. Segundo paso de la respuesta: procesamos los datos finales
        .then(data => {
            // Buscamos el div vacío y le "inyectamos" el resultado formateado
            // Recordá que 'data.result' viene de la clave que definimos en el return de FastAPI
            document.getElementById("system_response").innerHTML = data.result;
        })

        // 6. Por si algo sale mal (ej: se cortó internet o el servidor se cayó)
        .catch(error => {
            console.error('Error:', error);
            document.getElementById("system_response").innerHTML = "Hubo un error al procesar tu solicitud.";
        });
}