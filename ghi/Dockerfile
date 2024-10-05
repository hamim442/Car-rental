# Use the official Node.js image to build the application
FROM node:lts-bullseye AS build

# Set the working directory
WORKDIR /app

# Copy the package.json and package-lock.json to the working directory
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code to the working directory
COPY . ./

# Build the application
RUN npm run build

# Use Nginx to serve the built application
FROM nginx:alpine

# Copy the build output to Nginx's default html directory
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Command to run Nginx
CMD ["nginx", "-g", "daemon off;"]
