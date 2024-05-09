FROM python:3.11

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src /app

RUN alembic upgrade head
CMD ["python", "main.py"]

EXPOSE 8000