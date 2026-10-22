FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY templates/ ./templates/

RUN useradd --system --uid 10001 --create-home appuser \
    && chown -R appuser:appuser /app

ENV HOME=/home/appuser
ENV TMPDIR=/tmp

USER 10001

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--worker-tmp-dir", "/tmp", "app:app"]
