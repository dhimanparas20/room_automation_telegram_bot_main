# Use the smallest official Python runtime
FROM python:3.11.11-alpine

# Set environment variables for Python to optimize runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy only requirements.txt first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code into the container
COPY . .

# Set the entry point to run your Python script
ENTRYPOINT ["python"]

# Specify the script to run as the default argument
CMD ["app.py"]