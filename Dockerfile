FROM python:3.10.5-slim

WORKDIR /zunlix_user_service
COPY . /zunlix_user_service

RUN ["/bin/bash", "-c", "mv .env.prod .env"]
RUN pip install -r requirements.txt