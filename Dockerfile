FROM python

RUN apt update -y
RUN apt upgrade -y
RUN apt install python3-pip -y

COPY app/ app/
COPY README.md README.md
COPY .env .env
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

CMD ["python3", "app/aaas.py"]