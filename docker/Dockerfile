FROM python:3.11-slim

WORKDIR /app

COPY docker/requirements.txt ./
RUN apt-get update && apt-get install -y build-essential cmake && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501
CMD ["streamlit", "run", "app/ui.py", "--server.address=0.0.0.0", "--server.port=8501"]
