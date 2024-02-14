FROM python:3.10

WORKDIR /backend

COPY ./requirements.txt /backend/requirements.txt

#Installs dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY ./ /backend/


#Exposes port 8000 for FastAPI
EXPOSE 8000

#Starts the FastAPI server
CMD uvicorn api:app --host=0.0.0.0 --port=5000


STOPSIGNAL SIGKILL