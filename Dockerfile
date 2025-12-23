FROM python:3.9-slim
RUN apt-get update && apt-get install -y \
    python3-tk \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . .
RUN ls -la
CMD ["python", "file_operations.py"]