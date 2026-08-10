FROM python:3.12-slim

LABEL author=kintil

WORKDIR /backend

COPY /app/requirements_app.txt .

RUN pip install --no-cache-dir -r requirements_app.txt

COPY /config ./config
COPY /app ./app
COPY /artifacts/models ./artifacts/models
COPY /artifacts/metrics ./artifacts/metrics

ENTRYPOINT ["uvicorn"]
CMD ["app.main:app"]

EXPOSE 8000