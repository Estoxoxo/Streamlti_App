# Utiliza una imagen base oficial de Python 3.12
FROM python:3.12-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de requirements.txt en el contenedor
COPY requirements.txt .

# Instala las dependencias necesarias
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copia el resto de los archivos del proyecto en el contenedor
COPY . .

# Expone el puerto que Streamlit utiliza
EXPOSE 8501

# Comando para ejecutar la aplicación de Streamlit
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
