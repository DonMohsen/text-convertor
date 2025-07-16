#!/bin/bash

# Update system & install dependencies
apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    libgl1 \
    libglib2.0-0

# Start the app
uvicorn main:app --host 0.0.0.0 --port 10000
