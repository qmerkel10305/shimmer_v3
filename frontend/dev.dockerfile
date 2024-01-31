FROM node:21-alpine

WORKDIR /app/
COPY package.json .
RUN npm install
COPY . .

CMD ["npm", "run", "dev"]

STOPSIGNAL SIGKILL
EXPOSE 8080

