FROM yeonju52/my-tesseract-app:latest

COPY . /app
WORKDIR /app

# # 개발 서버용 (간단히 실행할 때)
# CMD ["python3", "app.py"]

# 배포용 서버
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
