# Imagen base
FROM python:3.13-slim

# Carpeta interna del contenedor
WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el proyecto
COPY . .

# Puerto de streamlit
EXPOSE 8501

# Ejecutar app
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]