# 1. Usar la imagen base de Python 3.11 (ajusta la etiqueta si es necesario)
FROM python:3.11.9-slim

# 2. Establecer el directorio de trabajo
WORKDIR /app

# Establecer variables de entorno recomendadas
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Copiar solo el archivo de requerimientos primero
COPY requirements.txt .

# 4. Instalar dependencias del sistema (compilador C++) y luego las de Python
RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

# 4. Instalar las dependencias (usando el requirements.txt)
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar el resto del código del proyecto
# Asegúrate de tener un .dockerignore para excluir venv, .git, __pycache__, etc.
COPY . .

# 6. Exponer el puerto 8000
EXPOSE 8000

# 7. Comando para ejecutar la aplicación (sin --reload para producción)
# Ajusta "main:app" si tu archivo principal o variable FastAPI son diferentes
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]