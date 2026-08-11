#Builder
FROM python:3.12-slim AS builder

WORKDIR /install

RUN apt-get update && \
    apt-get install -y \
    --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*
COPY /app/requirements_app.txt .

RUN pip install \
    --no-cache-dir \
    --prefix=/runtime \
    -r requirements_app.txt


# Images yg dipakai
FROM python:3.12-slim

LABEL author=kintil

WORKDIR /backend

COPY --from=builder /runtime /usr/local

COPY /reference ./reference
COPY /config ./config
COPY /app ./app
COPY /artifacts/models ./artifacts/models
COPY /artifacts/metrics ./artifacts/metrics

EXPOSE 8000

ENTRYPOINT ["uvicorn"]
CMD ["app.main:app","--host","0.0.0.0","--port","8000"]

