# Using the official Python image from the Docker Hub
FROM python:3.9-slim

# Setting environment variables to ensure Python output is not buffered
ENV PYTHONUNBUFFERED 1

# Setting the working directory inside the container
WORKDIR /app

# Copying the requirements file into the container
COPY requirements.txt /app/

# Installing the Python dependencies
RUN pip install -r requirements.txt

# Copying the rest of the application code into the container
COPY . /app

# Setting the port that the application runs on
EXPOSE 5000

# Definiing the command to run the application
CMD ["python", "app.py"]
