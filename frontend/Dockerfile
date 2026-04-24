# Build stage
FROM node:18-alpine AS build

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy application code
COPY . .

# Build the application
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built assets from build stage
COPY --from=build /app/build /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Permissions 
RUN chgrp -R 0 /var/cache/nginx /var/run /var/log/nginx /usr/share/nginx/html && \
    chmod -R g+rwX /var/cache/nginx /var/run /var/log/nginx /usr/share/nginx/html && \
    chmod g+rw /etc/nginx/conf.d/default.conf

# Run as non-root user
USER 1001

# Expose port 8080
EXPOSE 8080

# Start nginx
CMD ["nginx", "-g", "daemon off;"]