# Usa un'immagine leggera di Python
FROM python:3.10-slim

# Imposta la directory di lavoro nel container
WORKDIR /app

# Copia il file delle dipendenze
COPY requirements.txt .

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# Copia tutto il progetto
COPY . .

# Esponi la porta su cui gira uvicorn
EXPOSE 8000

# Comando per far partire FastAPI con ricarica
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]