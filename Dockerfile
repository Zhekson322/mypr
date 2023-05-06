FROM python:3

WORKDIR /bot

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /bot

CMD [ "python", "main.py" ]