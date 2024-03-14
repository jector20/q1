FROM python:3.11

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY q1_server.py /app

CMD [ "python", "q1_server.py" ]



