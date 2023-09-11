FROM python:3.11

ADD ./requirements.txt /opt
RUN pip install --no-cache-dir -r /opt/requirements.txt

ADD ./ /opt
WORKDIR /opt

ENTRYPOINT python ./game/main.py
