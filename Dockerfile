# tesseract 및 기본 Python 환경이 갖춰진 이미지로부터 시작
FROM yeonju52/my-tesseract-app:latest

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0:5001", "app:app"]
