FROM node:20.15.1-alpine3.19 as develop-stage
WORKDIR /app
COPY package*.json ./
RUN yarn global add @quasar/cli
COPY . .

FROM develop-stage as build-stage
RUN yarn
RUN quasar build

# Use the lightweight Nginx image from the previous stage for the nginx container
FROM nginx:stable-alpine as production-stage
# Copy the build application from the previous stage to the Nginx container
COPY --from=build-stage /app/dist/spa/ /usr/share/nginx/html
# Copy the nginx configuration file
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
