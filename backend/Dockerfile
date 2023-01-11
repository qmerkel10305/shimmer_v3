FROM debian:bookworm-slim
WORKDIR /app
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install --no-install-recommends -y libglib2.0-0 libgl1 proj-bin libboost-python-dev libexiv2-dev python3-pip python3-dev build-essential && rm -rf /var/lib/apt/lists/*
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY ./src /app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
