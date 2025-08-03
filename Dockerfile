# Use the official Python runtime image
FROM python:3.13-alpine AS builder

# Create the app directory
RUN mkdir /app

# Set the working directory inside the container
WORKDIR /app

# Set environment variables
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Upgrade pip
RUN pip install --upgrade pip

# Copy the Django project  and install dependencies
COPY requirements.txt  /app/

# run this command to install all dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Production stage
FROM python:3.13-alpine

RUN adduser -D -G www-data www-data && \
    mkdir /app && \
    mkdir -p /var/cache/fastf1 && \
    chown -R www-data:www-data /app /var/cache/fastf1

# Copy the Python dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Set the working directory
WORKDIR /app

# Copy the Django project to the container
COPY --chown=www-data:www-data ./src /app/
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Switch to non-root user
USER www-data

VOLUME /var/cache/fastf1

# Expose the Django port
EXPOSE 8000

# Entrypoint script
ENTRYPOINT ["/entrypoint.sh"]
