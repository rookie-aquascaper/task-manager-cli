# Koristimo zvaničnu Python sliku
FROM python:3.12-slim

# Postavimo radni direktorijum
WORKDIR /app

# Kopiramo fajlove u kontejner
COPY . /app

# Za CLI aplikaciju nije nam potreban pytest
CMD ["python3", "task_manager.py"]
