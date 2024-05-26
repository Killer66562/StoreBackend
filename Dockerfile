FROM python:3.11

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src /app

EXPOSE 8000

CMD [ "/bin/bash", "-c", "alembic upgrade head; python fake.py; python main.py" ]