# # Use the official Python 3.11.3 image as the base
# FROM python:3.11.3

# # Set the working directory inside the container
# WORKDIR /app

# # Copy the requirements file and install the dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the entire project directory into the container
# COPY . .

# # Copy the Gunicorn configuration file
# COPY gunicorn.conf.py .

# # Expose the port your FastAPI application will run on
# EXPOSE 8000

# # Set the command to start the FastAPI application with Gunicorn and custom config
# CMD ["gunicorn", "-c", "gunicorn.conf.py", "main:app"]

# syntax=docker/dockerfile:1

FROM python:3.11.3

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 3100

CMD ["gunicorn", "main:app"]
