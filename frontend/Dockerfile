FROM node:20-alpine AS builder

WORKDIR /app

COPY fuelspy/package*.json ./

RUN npm ci

COPY fuelspy/ ./

ARG NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
ENV NEXT_PUBLIC_API_BASE_URL=$NEXT_PUBLIC_API_BASE_URL

RUN npm run build

# Production stage
FROM node:20-alpine

WORKDIR /app

RUN npm install -g next

COPY --from=builder /app/.next ./.next
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/public ./public
COPY --from=builder /app/node_modules ./node_modules

ENV NODE_ENV=production

EXPOSE 3000

CMD ["npm", "start"]