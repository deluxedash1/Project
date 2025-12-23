FROM python:3.9-slim
RUN apt-get update && apt-get install -y \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY main.py .
COPY guiModule.py .
CMD ["python", "main.py"]