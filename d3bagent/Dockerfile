FROM python:3.11.1-alpine3.16
RUN mkdir /d3bagent && cd /d3bagent
WORKDIR /d3bagemt
COPY ./requirements.txt .
RUN ls /d3bagent
RUN pip install -r requirements.txt
COPY . .
RUN export FLASK_APP=app.py
EXPOSE 5000
CMD flask run --host=0.0.0.0