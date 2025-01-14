# Use the official Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy local files into the container
COPY . /app

# Install system dependencies for Selenium and Chrome
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    libnss3 \
    libgconf-2-4 \
    libx11-xcb1 \
    libasound2 \
    libxrender1 \
    libxtst6 \
    libxi6 \
    fonts-liberation \
    libu2f-udev \
    libappindicator3-1 \
    xdg-utils \
    && wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && rm -f google-chrome-stable_current_amd64.deb

# Download and install ChromeDriver
RUN wget -q https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.264/linux64/chromedriver-linux64.zip \
    && unzip chromedriver-linux64.zip -d /usr/local/bin/ \
    && mv /usr/local/bin/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \
    && rm -rf chromedriver-linux64.zip /usr/local/bin/chromedriver-linux64 \
    && chmod +x /usr/local/bin/chromedriver

# Install Python dependencies
RUN pip install pandas beautifulsoup4 selenium

# Set PATH for ChromeDriver
ENV PATH="/usr/local/bin:${PATH}"

# Command to run the script
CMD ["python", "main.py"]
