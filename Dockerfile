FROM python:3.12-alpine
# FROM python:3.22-alpine

# Install PostgreSQL client and other required build tools
RUN apk add --no-cache postgresql-client libpq

RUN pip install --no-cache-dir --upgrade pip

COPY dev_requirements.txt /dev_requirements.txt
RUN pip install --no-cache-dir -r dev_requirements.txt

WORKDIR /usr/local/app/
ADD backendSvc  /usr/local/app/

# Create a non-root user
RUN adduser -D -u 1000 appuser

# Change ownership
RUN chown -R appuser:appuser /usr/local/app/

# Switch to non-root user
USER appuser

# You can also imgore the above 3 steps by the following command
# - sudo chown -R $USER:$USER ./backendSvc

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]