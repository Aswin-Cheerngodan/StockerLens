FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
libpng-dev \
libjpeg-dev \
libtiff5-dev \
ffmpeg \
&& rm -rf /var/lib/apt/lists/*

WORKDIR /code

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Expose port
EXPOSE 8000

CMD [ "python", "-m", "app.api.main" ]



