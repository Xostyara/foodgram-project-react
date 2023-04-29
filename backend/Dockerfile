FROM python:3.8.5

WORKDIR /backend

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ] 
