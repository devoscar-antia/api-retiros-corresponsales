# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only necessary files and directories
COPY main.py .
COPY alembic.ini .
COPY requirements.txt .

# Copy all necessary directories
COPY alembic/ alembic/
COPY auth/ auth/
COPY db/ db/
COPY functions/ functions/
COPY globals/ globals/
COPY models/ models/
COPY routers/ routers/
COPY schemas/ schemas/
COPY scripts/ scripts/
COPY services/ services/
COPY tests/ tests/

# Expose the port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"] 