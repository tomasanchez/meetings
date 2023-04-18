FROM node:alpine

WORKDIR /web

COPY ./package.json ./
COPY ./yarn.lock ./
RUN yarn install

COPY . .
EXPOSE 5173
CMD ["yarn" , "dev"]


