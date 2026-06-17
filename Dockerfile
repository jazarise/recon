# Builder Stage
FROM python:3.11-slim as builder

WORKDIR /build
COPY pyproject.toml .
COPY src/ ./src/

# Install build dependencies and build wheel
RUN pip install build && python -m build --wheel

# Runtime Stage
FROM python:3.11-slim as runtime

RUN groupadd -r reconx && useradd -r -g reconx -m reconx

WORKDIR /app

# Install the built wheel
COPY --from=builder /build/dist/*.whl /tmp/
RUN pip install /tmp/*.whl && rm -rf /tmp/*.whl

USER reconx

HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health/live')" || exit 1

EXPOSE 8000
CMD ["python", "-m", "reconx.cli.main", "api", "--port", "8000"]
