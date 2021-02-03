FROM python:3
ENV PYTHONUNBUFFERED 1
WORKDIR /vehicle_collisions
COPY requirements.txt /vehicle_collisions/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /vehicle_collisions/