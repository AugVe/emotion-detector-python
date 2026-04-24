# STAGE 1: Builder
# We use a full python image to have all the necessary tools to compile dependencies
FROM python:3.11 AS builder

WORKDIR /app

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies in a separate step to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# STAGE 2: Runtime
# We use a much smaller 'slim' image for the final container
FROM python:3.11-slim

WORKDIR /app

# Copy only the installed libraries from the builder stage
COPY --from=builder /install /usr/local

# Copy the application source code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Set the command to run the application
CMD ["python", "server.py"]