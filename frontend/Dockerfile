FROM node:18

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build

# Для dev-сборки можно временно заменить на:
# CMD ["npm", "run", "dev"]
CMD ["npx", "serve", "-s", "build", "-l", "3000"]