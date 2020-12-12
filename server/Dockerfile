FROM python:3.9.1

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8000

COPY run.py .
COPY ./weather_api ./weather_api

CMD python run.py
