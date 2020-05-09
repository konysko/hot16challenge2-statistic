FROM node:slim

WORKDIR /usr/src/app

COPY package.json ./
COPY package-lock.json ./

RUN npm i -g npm
RUN npm install

COPY . .
