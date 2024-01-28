FROM node:21-alpine as builder

WORKDIR /app/
COPY src/ ./src
COPY public/ ./public
COPY index.html package.json package-lock.json vite.config.js ./
RUN npm install && npm run build

FROM nginx 
COPY --from=builder /app/dist/ /usr/share/nginx/html

EXPOSE 80

