# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /code
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /code
COPY . ./

# Set the environment variable for Django
# ENV DJANGO_SETTINGS_MODULE=myproject.settings

# Run Django migrations
RUN python manage.py collectstatic && \
	python manage.py migrate

# Expose the port that Django is running on
EXPOSE 8000

# Define the command to start the server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

