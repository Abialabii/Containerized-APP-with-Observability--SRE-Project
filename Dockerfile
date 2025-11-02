FROM python:3.9-slim
WORKDIR /app
RUN pip install Flask prometheus_client
COPY app/ .
CMD ["python", "app.py"]
