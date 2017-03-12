FROM ubuntu:latest

RUN apt-get update && apt-get install -y python3 python3-pip git
RUN git clone https://github.com/cloudy/Number-Theory-PKC-Project.git /opt/nt
RUN pip3 install --upgrade pip && pip3 install -r /opt/nt/requirements.txt

EXPOSE 12345
WORKDIR /opt/nt/

ENTRYPOINT ["python3", "/opt/nt/app.py"]