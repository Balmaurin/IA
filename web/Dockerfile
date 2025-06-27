# ----------- SHEILY-light Frontend Dockerfile -----------
FROM node:20-alpine AS builder
WORKDIR /web
COPY package.json package-lock.json* ./
RUN npm ci --omit=dev
COPY . .
RUN npm run build

FROM nginx:1.25-alpine
COPY --from=builder /web/out /usr/share/nginx/html
EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]
