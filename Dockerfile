# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 5000

# Run app using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]