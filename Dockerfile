FROM yeonju52/my-tesseract-app:latest

COPY . /app
WORKDIR /app

CMD ["sh", "-c", "gunicorn -b 0.0.0.0:$PORT app:app"]
