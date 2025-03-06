FROM python:3.12-slim

WORKDIR /bot_workdir

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
