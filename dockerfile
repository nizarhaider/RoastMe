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
RUN apt-get update && apt-get install libgl1 -y


RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install gunicorn
# # Set environment variable
ENV FLASK_APP=main.py

# Expose port 80
# EXPOSE 8080

# Define the command to run the application
# CMD ["flask", "run", "--host=0.0.0.0"]
RUN cd $APP_HOME

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
