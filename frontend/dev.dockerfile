FROM node:21-alpine

WORKDIR /app/
COPY . .
RUN npm install

CMD ["npm", "run", "dev"]

STOPSIGNAL SIGKILL
EXPOSE 8080

