FROM python:3.8

WORKDIR /backend

COPY ./ /backend/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD uvicorn api:app --reload