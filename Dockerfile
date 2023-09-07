ARG BASE=nvidia/cuda:11.8.0-base-ubuntu22.04
FROM ${BASE}
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y --no-install-recommends gcc g++ make python3 python3-dev python3-pip python3-venv python3-wheel espeak-ng libsndfile1-dev && rm -rf /var/lib/apt/lists/*
RUN pip3 install llvmlite --ignore-installed

WORKDIR /root
COPY . /root
COPY SteveJobs.wav /opt/voices/SteveJobs.wav
RUN pip3 install torch torchaudio --extra-index-url https://download.pytorch.org/whl/cu118
RUN rm -rf /root/.cache/pip
RUN make install

# ENTRYPOINT ["tts"]
EXPOSE 5002
CMD ["python3", "TTS/server/YourTTSService.py"]


# # 使用 Python 3.9 作为基础镜像
# FROM  --platform=linux/amd64 python:3.9 

# # 设置工作目录
# WORKDIR /app

# # 将当前目录下的所有文件复制到容器的 /app 目录
# COPY . /app
# COPY SteveJobs.wav /opt/voices/SteveJobs.wav

# RUN pip install --upgrade pip
# # 安装依赖
# RUN pip install -e .[all,dev,notebooks]

# # 暴露端口 5002
# EXPOSE 5002

# # 启动命令
# CMD ["python3", "TTS/server/YourTTSService.py"]






# # 使用官方的 Ubuntu 22.04 基础镜像
# FROM  --platform=linux/amd64 ubuntu:22.04

# # 更新系统并安装依赖
# RUN apt-get update && apt-get upgrade -y
# RUN apt-get install -y --no-install-recommends gcc g++ make python3 python3-dev python3-pip python3-venv python3-wheel espeak-ng libsndfile1-dev && rm -rf /var/lib/apt/lists/*

# # 安装 Python 依赖
# RUN pip3 install llvmlite --ignore-installed

# # 设置工作目录
# WORKDIR /root

# # 拷贝所有文件到工作目录
# COPY . /root
# COPY SteveJobs.wav /opt/voices/SteveJobs.wav

# # 安装 PyTorch 和 torchaudio
# RUN pip3 install torch torchaudio

# # 清除 pip 缓存
# RUN rm -rf /root/.cache/pip

# # 运行安装脚本
# RUN make install

# # 暴露端口
# EXPOSE 5002

# # 设置默认命令
# CMD ["python3", "TTS/server/YourTTSService.py"]











