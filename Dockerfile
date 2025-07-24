FROM yeonju52/my-tesseract-app:latest

COPY . /app
WORKDIR /app

CMD ["gunicorn", "-b", "0.0.0.0:$PORT", "app:app", "--timeout", "120", "--workers", "1", "--preload"]
