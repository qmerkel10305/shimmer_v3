FROM python:3.10

WORKDIR /backend

#Installs dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY ./ /backend/


#Exposes port 8000 for FastAPI
EXPOSE 8000

#Starts the FastAPI server
CMD uvicorn api:app --host=0.0.0.0


STOPSIGNAL SIGKILL