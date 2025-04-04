# 使用官方 Python 镜像作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖和 Chrome
RUN apt-get update && apt-get install -y \
    wget \
    gnupg2 \
    unzip \
    curl \
    && curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 安装 ChromeDriver
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | awk -F'.' '{print $1}') \
    && wget -q "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${CHROME_VERSION}.0.6261.94/linux64/chromedriver-linux64.zip" -O /tmp/chromedriver.zip \
    && unzip /tmp/chromedriver.zip -d /tmp/ \
    && mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \
    && chmod +x /usr/local/bin/chromedriver \
    && rm -rf /tmp/chromedriver*

# 创建非 root 用户
RUN groupadd -r chrome && useradd -r -g chrome -G audio,video chrome \
    && mkdir -p /home/chrome && chown -R chrome:chrome /home/chrome

# 设置 Chrome 沙盒
RUN mkdir -p /opt/chrome \
    && chown -R chrome:chrome /opt/chrome \
    && chmod -R 755 /opt/chrome

# 复制项目文件
COPY . /app/

# 创建并设置权限
RUN mkdir -p /app/data /app/logs \
    && chown -R chrome:chrome /app \
    && chmod -R 755 /app

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 切换到非 root 用户
USER chrome

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PATH="/usr/local/bin:${PATH}"

# 设置 Chrome 的一些重要环境变量
ENV CHROME_BIN=/usr/bin/google-chrome
ENV CHROME_PATH=/usr/bin/google-chrome
ENV CHROMIUM_FLAGS="--headless --no-sandbox --disable-gpu --disable-dev-shm-usage"

# 暴露端口
EXPOSE 5001

# 启动命令
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers=2", "--threads=4", "--timeout=120", "app:app"] 