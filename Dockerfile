FROM python:3.8
COPY . /lsfterm
WORKDIR /lsfterm
CMD python3 lsfterm
