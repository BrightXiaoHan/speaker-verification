ARG PYTHON_VERSION=3.9
FROM python:${PYTHON_VERSION} as base

RUN sed -i s@/deb.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list \
    && sed -i s@/security.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list

# 将时区设置为上海
ENV TZ=Asia/Shanghai \
    DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y tzdata libsndfile1 \
    && ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime \
    && echo ${TZ} > /etc/timezone \
    && dpkg-reconfigure --frontend noninteractive tzdata \
    && rm -rf /var/lib/apt/lists/*


ARG SOURCE_DIR=/root/repo
# 安装Python依赖库
WORKDIR ${SOURCE_DIR}

# 安装Python依赖库
ADD requirements.txt .
RUN pip install --upgrade pip -i https://pypi.douban.com/simple  \
  && pip --no-cache-dir install -r requirements.txt -i https://pypi.douban.com/simple

# 下载模型
ADD download_models.py .
ADD cache /root/.cache
RUN python3 download_models.py

# 添加模型代码
ADD . .

EXPOSE 80
ENTRYPOINT ["python3"]

