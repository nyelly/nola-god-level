# Use a Node.js base image for building the Vue app
FROM node:lts-alpine AS build-stage

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json to leverage Docker's caching
COPY package*.json ./

# Install project dependencies
RUN npm install

# Copy the rest of the application files
COPY . .

# Build the Vue application for production
RUN npm run build

# Use a lightweight Nginx image to serve the static built files
FROM nginx:stable-alpine AS production-stage

# Copy the built Vue app from the build-stage to Nginx's serving directory
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Expose port 80 for Nginx
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]