# Use the official Python image from the Docker Hub
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the project code into the container at /app
COPY . /app/

# Expose port 8000 to the outside world
EXPOSE 8000

# Default command to run Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
