# Use an official Python runtime as the base image
FROM python:3.8-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required packages
RUN pip3 install -r requirements.txt

# Set environment variable
ENV FLASK_APP=app.py

# Expose port 80
EXPOSE 8080

# Define the command to run the application
CMD ["flask", "run", "--host=0.0.0.0"]
