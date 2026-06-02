FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install CPU-only torch BEFORE easyocr so pip doesn't pull the CUDA variant (~2.5 GB).
# On macOS local dev torch is also CPU-only, so behaviour is identical.
RUN pip install --no-cache-dir \
        torch torchvision \
        --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /usr/local/lib/python3.12/site-packages/torch/test \
    && find /usr/local/lib/python3.12/site-packages \
        -type d -name "__pycache__" \
        -exec rm -rf {} + 2>/dev/null || true

COPY . .

CMD ["python", "cocoanut_bot.py"]
