# 使用Python官方镜像作为基础镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 复制requirements.txt文件到容器中
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件到容器中
COPY . .

# 创建缓存目录
RUN mkdir -p /app/cache

# 设置环境变量
ENV FLASK_ENV=production
ENV HOST=0.0.0.0
ENV PORT=5000

# 暴露端口
EXPOSE 5000

# 启动应用
CMD ["python", "main.py"]