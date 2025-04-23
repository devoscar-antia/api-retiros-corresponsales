# Build stage
FROM node:20-alpine as build

WORKDIR /app

# Copy package files
COPY package.json pnpm-lock.yaml ./

# Install pnpm
RUN npm install -g pnpm

# Install dependencies
RUN pnpm install

# Copy the source code and configuration files
COPY src ./src
COPY public ./public
COPY index.html .
COPY tsconfig.json .
COPY tsconfig.node.json .
COPY tsconfig.app.json .
COPY vite.config.ts .
COPY eslint.config.js .

# Build the application
RUN pnpm run build

# Production stage
FROM nginx:alpine

# Copy the built files from the build stage
COPY --from=build /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"] 