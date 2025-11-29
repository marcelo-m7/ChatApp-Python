FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PORT=8080 \
    HOST=0.0.0.0 \
    SERVER_PORT=3000 \
    SERVER_HOST=0.0.0.0

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

# Garante que os diretórios usados para upload existam
RUN mkdir -p /app/uploads /app/src/uploads

EXPOSE 8080 3000

CMD ["bash", "-lc", "python -m uvicorn server:app --host ${SERVER_HOST:-0.0.0.0} --port ${SERVER_PORT:-3000} & exec python src/main.py"]
