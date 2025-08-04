# Imagen base robusta compatible con drivers ODBC
FROM python:3.10-bullseye

# Variables de entorno
ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    TZ=America/Bogota

# Instalar dependencias de sistema necesarias para pyodbc + ODBC SQL Server
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libssl-dev \
    libffi-dev \
    libpq-dev \
    libcurl4 \
    libstdc++6 \
    libkrb5-3 \
    libgssapi-krb5-2 \
    unixodbc \
    unixodbc-dev \
    odbcinst \
    curl \
    gnupg \
    tzdata \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copiar el código
COPY . /app
WORKDIR /app

# Puerto para Streamlit en Render
EXPOSE 10000

# Comando de ejecución
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=10000", "--server.address=0.0.0.0"]
