FROM python:latest

WORKDIR /app

RUN pip install "fastapi[standard]"
RUN pip install requests

COPY ./ ./

CMD ["bash","run.sh"]
