FROM python:3.11.1-alpine3.16
RUN mkdir /d3bfed && cd /d3bfed
WORKDIR /d3bfed
COPY ./requirements.txt .
RUN ls /d3bfed
RUN pip install -r requirements.txt
COPY . .
RUN export FLASK_APP=dataManager.py
EXPOSE 5000
CMD flask run --host=0.0.0.0