# Use the official Python 3.13 image
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Copy your requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all your python scripts into the container
COPY . .

# Expose the API port
EXPOSE 8001

# The command that runs when the container starts
CMD ["python", "main.py"]