FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 复制 requirements.txt 并安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 复制 combined.m3u 文件
COPY build/combined.m3u /app/combined.m3u

# 设置默认命令
CMD ["python", "server.py"]
