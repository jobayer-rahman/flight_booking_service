FROM python:3.12-alpine

RUN pip install --no-cache-dir --upgrade pip

COPY dev_requirements.txt /dev_requirements.txt
RUN pip install --no-cache-dir -r dev_requirements.txt


WORKDIR /usr/local/app/

ADD backendSvc  /usr/local/app/

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]