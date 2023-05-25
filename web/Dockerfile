FROM node:alpine as build-stage

WORKDIR /web

COPY ./package.json ./
COPY ./yarn.lock ./
RUN yarn install

COPY . .
RUN yarn build


# Etapa de producción
FROM nginx:1.21-alpine as production-stage
COPY --from=build-stage /web/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 5173
CMD ["nginx", "-g", "daemon off;"]