FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py ./
COPY milo ./milo
COPY levels ./levels

# The commit being served, shown at /health.
ARG GIT_COMMIT=unknown
ENV GIT_COMMIT=${GIT_COMMIT}

RUN useradd --system --uid 10001 milo
USER milo
EXPOSE 8000
CMD ["python", "main.py"]
