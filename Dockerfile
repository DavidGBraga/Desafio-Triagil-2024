FROM python:3.12

WORKDIR /usr/src/app

COPY . .

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

CMD  ["python", "pokeservices.py"]
