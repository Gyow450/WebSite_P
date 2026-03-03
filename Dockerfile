# 使用官方 Python 3.11 镜像
FROM python:3.11-slim

# 工作目录
WORKDIR /app

# 先装依赖（利用缓存，后面改代码不用重装包）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 再复制源代码
COPY . .

# 暴露端口
EXPOSE 5001

# 启动命令
CMD ["gunicorn", "-b", "0.0.0.0:5001", "app:app"]