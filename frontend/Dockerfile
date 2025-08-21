FROM docker.io/library/node:24-alpine3.21 AS build-stage
RUN npm install -g typescript
WORKDIR /app
COPY ./tsconfig.json ./
COPY ./web/ts ./web/ts
RUN tsc 

FROM nginx:stable-alpine3.21-perl
COPY ./nginx.conf /etc/nginx/nginx.conf
COPY --from=build-stage /app/web /usr/share/nginx
COPY ./web /usr/share/nginx
EXPOSE 80
