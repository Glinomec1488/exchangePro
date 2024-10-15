FROM ubuntu
FROM httpd

RUN mkdir fakex
 
WORKDIR /fakex
RUN apt-get update 
RUN apt-get install npm -y

COPY . /fakex

RUN npm run build:dev
RUN npm install -g serve

ENTRYPOINT ["serve", "-s" ,"build"]

EXPOSE 3000