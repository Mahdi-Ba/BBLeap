# Use a slim base image
FROM python:3.11
# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port 8000
EXPOSE 8000

# Run health check script
# Copy health check script
COPY health_check.sh /app
RUN chmod +x /app/health_check.sh

# Run health check script and stop build if pytest encounters errors
RUN /app/health_check.sh

## create tables
CMD ["alembic","upgrade","head"]
## Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
