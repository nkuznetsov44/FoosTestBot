FROM node:alpine as build
WORKDIR .
ENV PATH /node_modules/.bin:$PATH
COPY package.json ./
COPY package-lock.json ./
RUN npm install
COPY . ./
RUN npm run build

FROM nginx:stable-alpine
COPY --from=build /build /usr/share/nginx/html
COPY /nginx-conf.d /etc/nginx/conf.d
CMD ["nginx", "-g", "daemon off;"]