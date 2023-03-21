FROM debian:bookworm-slim
WORKDIR /app
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install --no-install-recommends -y libglib2.0-0 libgl1 proj-bin libboost-python-dev libexiv2-dev python3-dev python3-venv build-essential && rm -rf /var/lib/apt/lists/*
RUN python3 -m venv venv
COPY ./requirements.txt /app/requirements.txt
RUN /app/venv/bin/pip3 install --no-cache-dir --upgrade -r /app/requirements.txt
COPY ./src /app
CMD ["/app/venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
