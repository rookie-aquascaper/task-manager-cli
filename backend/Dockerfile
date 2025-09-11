# Dockerfile za Task Manager CLI

# 1) Bazna slika sa Python-om
FROM python:3.12-slim

# 2) Radni direktorijum u containeru
WORKDIR /app

# 3) Kopiraj requirements (ako postoji)
COPY requirements.txt .

# 4) Ažuriraj pip i instaliraj zavisnosti (pytest je u requirements za test)
RUN python -m pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# 5) Kopiraj ceo repo (kod) u container
COPY . .

# 6) Po defaultu pokreni CLI skriptu
#    - za interaktivni meni pokreni sa `docker run -it ...`
ENTRYPOINT ["python", "task_manager.py"]
