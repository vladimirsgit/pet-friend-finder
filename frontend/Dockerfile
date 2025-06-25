FROM node:22-alpine

WORKDIR /app

COPY pff-react/package.json .

RUN npm install

COPY pff-react/ .

CMD ["npm", "run", "dev"]