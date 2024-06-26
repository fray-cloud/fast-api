# Dockerfile

# 베이스 이미지 설정
FROM python:3.12-slim

# 작업 디렉토리 설정
WORKDIR /app

# FastAPI 애플리케이션 소스코드를 이미 가져왔으므로 클론은 불필요

# requirements.txt를 복사하여 패키지 설치
COPY . .

# 필요한 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 포트 노출
EXPOSE 8000

# alembic revision --autogenerate


# FastAPI 애플리케이션 실행
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
