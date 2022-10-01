# syntax=docker/dockerfile:1
FROM python:3.8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /pegb_ecommerce
COPY requirements.txt /pegb_ecommerce/
RUN pip install -r requirements.txt
COPY . /pegb_ecommerce/
