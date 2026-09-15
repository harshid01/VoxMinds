FROM node:22-alpine
WORKDIR /app
COPY frontend/package*.json /app/frontend/
RUN cd /app/frontend && npm install
COPY frontend /app/frontend
