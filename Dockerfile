# Use the base Python image
FROM python:3.9-slim

# Update and install additional OS packages if needed
RUN apt-get update && apt-get -y install --no-install-recommends \
   gcc \
   default-mysql-client

# Create a non-root user (optional but recommended)
ARG USER="ashley"
RUN useradd -m -s /bin/bash ${USER}

# Set the working directory
WORKDIR /app

# Copy the requirements file and Makefile to the container
COPY requirements.txt Makefile ./

# Copy your project source code and tests into the container
COPY ./src /app/src
COPY ./tests /app/tests

# Install Python dependencies
RUN pip install --disable-pip-version-check --no-cache-dir -r requirements.txt

# Ensure that the /app directory is owned by the non-root user
RUN chown -R ${USER}:${USER} /app

# Switch to the non-root user (optional but recommended)
USER ${USER}

# Set PYTHONPATH to include /app
ENV PYTHONPATH=/app

# Specify the command to run your application
CMD ["python", "-m", "src.cli"]
