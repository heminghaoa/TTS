# 使用 Python 3.9 作为基础镜像
FROM python:3.9

# 设置工作目录
WORKDIR /app

# 将当前目录下的所有文件复制到容器的 /app 目录
COPY . /app

# 安装依赖
RUN pip install --no-cache-dir -e .[all,dev,notebooks]

# 暴露端口 5002
EXPOSE 5002

# 启动命令
CMD ["python3", "TTS/server/YourTTSService.py"]




# ARG BASE=nvidia/cuda:11.8.0-base-ubuntu22.04
# FROM ${BASE}
# RUN apt-get update && apt-get upgrade -y
# RUN apt-get install -y --no-install-recommends gcc g++ make python3 python3-dev python3-pip python3-venv python3-wheel espeak-ng libsndfile1-dev && rm -rf /var/lib/apt/lists/*
# RUN pip3 install llvmlite --ignore-installed

# WORKDIR /root
# COPY . /root
# RUN pip3 install torch torchaudio --extra-index-url https://download.pytorch.org/whl/cu118
# RUN rm -rf /root/.cache/pip
# RUN make install
# ENTRYPOINT ["tts"]
# CMD ["--help"]
