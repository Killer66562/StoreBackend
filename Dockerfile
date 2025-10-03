FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install cryptography
RUN pip install fastapi-mail
RUN pip install --no-cache-dir -r requirements.txt

COPY src /app

EXPOSE 8000

CMD [ "/bin/bash", "-c", "alembic upgrade head; python create_admin.py; python main.py" ]