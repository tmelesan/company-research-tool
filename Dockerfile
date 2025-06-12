FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Copy and make startup script executable (before switching to non-root user)
COPY start-services.sh /app/start-services.sh
RUN chmod +x /app/start-services.sh

# Create a non-root user and change ownership
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose ports for both API and Web servers
EXPOSE 8000 8501

# Default command runs both services
CMD ["/app/start-services.sh"]
