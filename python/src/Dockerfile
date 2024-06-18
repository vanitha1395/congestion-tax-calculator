# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app directory
COPY . .

# Expose the port the app will run on (change if needed)
EXPOSE 8080

# Set the command to run the app
CMD ["python", "main.py"]