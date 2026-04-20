# 1. Usamos una imagen de Python liviana
FROM python:3.11-slim

# 2. Seteamos el directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiamos el archivo de requerimientos
COPY requirements.txt .

# 4. Instalamos las librerías
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamos todo el contenido de tu carpeta actual al contenedor
COPY . .

# 6. Exponemos el puerto donde corre FastAPI
EXPOSE 8000

# 7. El comando para arrancar la app cuando el contenedor se encienda
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]