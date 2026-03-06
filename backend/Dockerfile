FROM python:3.12-slim

WORKDIR /app


COPY requirements.txt .

RUN sed -i '/torch==/d' requirements.txt && \
    sed -i '/torchvision==/d' requirements.txt && \
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]