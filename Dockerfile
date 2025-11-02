FROM python:3.9-slim
WORKDIR /app
RUN pip install requirements.txt
COPY app/ .
CMD ["python", "app.py"]
