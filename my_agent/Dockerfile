FROM python:3.11-slim AS builder
WORKDIR /app
RUN pip install --no-cache-dir virtualenv
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install the minimal runtime dependencies for the HTTP entrypoint
RUN pip install --no-cache-dir google-adk uvicorn fastapi

FROM python:3.11-slim AS runner
WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY . /app
EXPOSE 8080

CMD ["sh", "-c", "python -m uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}"]

