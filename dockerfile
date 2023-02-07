# Use an official Python runtime as the base image
FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# # Set the working directory to /app
# WORKDIR /app

# # Copy the current directory contents into the container at /app
# COPY . /app
RUN apt-get update && apt-get install -y git ninja-build libglib2.0-0 libsm6 libxrender-dev libxext6 libgl1-mesa-glx
# Install the required packages
RUN pip3 install --no-cache-dir -r requirements.txt

# # Set environment variable
# ENV FLASK_APP=app.py

# Expose port 80
# EXPOSE 8080

# Define the command to run the application
# CMD ["flask", "run", "--host=0.0.0.0"]
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
