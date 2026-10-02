FROM python:3.12-slim

# CHROME_ARGS is read by conftest.py and added to ChromeOptions. In a container the
# sandbox cannot be used and /dev/shm is small, so both flags are required.
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    CHROME_ARGS="--no-sandbox --disable-dev-shm-usage"

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        firefox-esr \
        fonts-liberation \
        libasound2 \
        libgbm1 \
        libgtk-3-0 \
        libnss3 \
        libxss1 \
        xdg-utils \
    && curl -sSL -o /tmp/chrome.deb \
        https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y --no-install-recommends /tmp/chrome.deb \
    && rm /tmp/chrome.deb \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tests

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# There is no display inside the container, so headless mode is always enabled.
# Arguments passed to ``docker run`` replace CMD, so any option from conftest.py
# (--browser, --url, --headless) can still be supplied by the caller.
ENTRYPOINT ["pytest", "--headless"]
CMD ["--browser", "chrome"]
