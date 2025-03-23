FROM python:3.9-slim

WORKDIR /app

# Install system dependencies nya (terutama untuk psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc libc6-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dan install dependencies python nya
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code wg-sync ke container
COPY main.py sync.py status.py utils.py cron.py ./
COPY mikrotik ./mikrotik/
COPY config.json config.json
COPY docker-entrypoint.sh ./

# Set permission + executable untuk docker-entrypoint.sh
RUN chmod +x docker-entrypoint.sh

# Entrypoint lewat sini supaya bisa langsung pilih command yang dijalankan
CMD ["./docker-entrypoint.sh"]