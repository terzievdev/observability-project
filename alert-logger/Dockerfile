FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir fastapi==0.115.6 uvicorn[standard]==0.32.1
COPY main.py .
CMD ["python", "main.py"]
