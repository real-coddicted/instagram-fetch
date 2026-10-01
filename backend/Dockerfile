FROM python:3.11-slim

WORKDIR /app

RUN useradd --create-home --shell /usr/sbin/nologin appuser

# Install uv for fast dependency resolution
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy requirements file (since your project uses requirements.txt instead of pyproject.toml)
COPY requirements.txt ./

# Install dependencies into the system environment using uv
RUN uv pip install --system --no-cache -r requirements.txt

# Copy application code
COPY app ./app

# Fix permissions
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8082

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8082"]
