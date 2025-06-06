FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY assets ./assets

EXPOSE 8080

CMD ["gunicorn", "app:app"]