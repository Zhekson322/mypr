FROM python:3.10
WORKDIR /app
COPU requirements.txt
RUN pip install -upgrade setuptools
RUN pip install -r requirements.txt
RUN chmod 755 .
COPY . .