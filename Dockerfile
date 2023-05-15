FROM python:3.11

RUN mkdir /arcanapi_app

WORKDIR /arcanapi_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

#RUN chmod a+x scripts/*.sh

RUN alembic upgrade head

WORKDIR app

CMD gunicorn app:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000 --reload