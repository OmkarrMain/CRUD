# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set environment variables to ensure Python output is not buffered
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app

# Expose the port that the application runs on
EXPOSE 5000

# Define the command to run the application
CMD ["python", "app.py"]
