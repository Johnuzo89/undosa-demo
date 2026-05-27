FROM python:3.10-slim

WORKDIR /app

RUN pip install --no-cache-dir flwr==1.8.0 numpy

RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

COPY server.py .

CMD ["python", "-u", "server.py"]
