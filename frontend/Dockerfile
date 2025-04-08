# 1️⃣ Use official Node image for build stage
FROM node:20 AS builder

WORKDIR /app

# 2️⃣ Copy and install deps
COPY package*.json ./
RUN npm install

# 3️⃣ Copy the rest and build
COPY . .
RUN npm run build

# 4️⃣ Use nginx for final stage
FROM nginx:alpine

# 5️⃣ Copy built React files to nginx's public directory
COPY --from=builder /app/dist /usr/share/nginx/html

# 6️⃣ Expose port and start nginx
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
