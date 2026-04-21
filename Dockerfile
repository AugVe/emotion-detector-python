# Use an official lightweight Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies if needed (none required for this specific project, 
# but good to keep the structure clean)
# Set environment variables to prevent Python from writing .pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy only the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Inform Docker that the container listens on the specified port at runtime
EXPOSE 8000

# Run the application using uvicorn
# We use 0.0.0.0 to allow external access (essential for cloud deployment)
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]