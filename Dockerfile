# dockerfile, docker image, container
FROM python:3.12.0
WORKDIR /app
COPY . /app
ADD app.py .

RUN pip install requests beautifulsoup4

CMD [ "python","./app.py" ]