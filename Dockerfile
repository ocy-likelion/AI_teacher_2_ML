# tesseract 미리 설치된 베이스 이미지 사용
FROM yeonju52/my-tesseract-app:latest

# 작업 디렉토리 설정
WORKDIR /app

# 프로젝트 파일 복사
COPY . .

# 파이썬 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 기본 실행 명령
CMD ["python", "main.py"]
