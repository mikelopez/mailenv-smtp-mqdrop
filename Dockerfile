# Stage 1: Build
FROM golang:1.22-alpine AS builder

WORKDIR /app

RUN apk add --no-cache zeromq-dev gcc g++ musl-dev

# Create go.mod inside container if missing
RUN go mod init mailenv-smtp-mqdrop || true

# Copy source
COPY . .

# Ensure dependencies are fetched
RUN go mod tidy


RUN go build -o mqdrop .

# Stage 2: Runtime
FROM alpine:3.19

WORKDIR /app

RUN apk add --no-cache zeromq

COPY --from=builder /app/mqdrop .

RUN mkdir -p /app/mailenv-data
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

CMD ["/app/entrypoint.sh"]
