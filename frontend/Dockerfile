FROM node:20-alpine AS base

# Install pnpm via corepack
RUN corepack enable pnpm

FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app
COPY package.json ./
RUN pnpm install

FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN pnpm run build

FROM base AS runner
WORKDIR /app
ENV NODE_ENV production

RUN pnpm install -g serve
COPY --from=builder /app/dist ./dist

EXPOSE 3000
CMD ["serve", "-s", "dist", "-l", "3000"]
