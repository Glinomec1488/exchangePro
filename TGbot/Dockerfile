FROM ubuntu


RUN mkdir fakexbackendTG
 
WORKDIR /fakexbackendTG
RUN apt-get update 
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
RUN apt-get install python3-venv -y

COPY . /fakexbackendTG

RUN python3 -m venv .
RUN bin/pip3 install -r requirements.txt

ENTRYPOINT ["bin/python3", "main.py"]