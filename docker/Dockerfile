FROM python:3.12-slim
WORKDIR /backend
COPY requirements.txt ./
RUN pip install -r requirements.txt || true
COPY . ./
EXPOSE 8000 8501
COPY docker/start.sh /backend/start.sh
RUN chmod +x /backend/start.sh

CMD ["/bin/bash","/backend/start.sh"]
