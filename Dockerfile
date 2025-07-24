FROM yeonju52/my-tesseract-app:latest

COPY . /app
WORKDIR /app

CMD ["python3", "app.py"]
