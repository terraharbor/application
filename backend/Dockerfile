FROM python:alpine3.22

ENV PYTHONUNBUFFERED=1 \
    STATE_DATA_DIR=/data

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

RUN apk add --no-cache su-exec         # ← 3 Ko
RUN addgroup -S app && adduser -S app -G app

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]