FROM python:3.12-slim
WORKDIR /app

# Install system dependencies required by Chromium (rimossi i font problematici)
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    libnss3 \
    libxss1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libgbm-dev \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Installa Chromium
RUN python -m rebrowser_playwright install chromium

COPY . .
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]