FROM python:3.8-slim-buster
EXPOSE 8000
WORKDIR /app 
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . .
RUN python manage.py collectstatic --noinput
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]