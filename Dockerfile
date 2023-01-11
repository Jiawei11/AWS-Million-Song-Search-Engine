# Docker image for flask python run
# VERSION 1.0
# Author: Weiye
# 基础镜像使用python:3.9
FROM python:3.9
# 指定容器工作目录为 /project/
WORKDIR /project/
# 安装 项目依赖
RUN pip install pandas flask psycopg2 -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

COPY . .
# 运行
ENTRYPOINT ["python","app.py"]

# 编译
# docker build -t weiye/flask-project:v1 .

# run
#docker run -it -p 7090:7090 --name flask-project \
#-v /mydata/flaskProject:/project \
#-d weiye/flask-project:v1
