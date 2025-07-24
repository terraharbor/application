FROM python:alpine3.22

ENV PYTHONUNBUFFERED=1 \
    STATE_DATA_DIR=/data

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN apk add --no-cache su-exec
RUN addgroup -S app && adduser -S app -G app

COPY . .

RUN mkdir -p /data && chown -R app:app /data

RUN chown -R app:app /app

EXPOSE 8000

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]