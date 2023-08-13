FROM python:3.11

WORKDIR /app

COPY requirements.txt requirements.txt

RUN  pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

COPY . .

ENTRYPOINT ["python3", "src/main.py"]
