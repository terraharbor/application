FROM python:alpine3.22

ENV PYTHONUNBUFFERED=1 \
    STATE_DATA_DIR=/data

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN addgroup -S app && adduser -S app -G app
USER app

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
