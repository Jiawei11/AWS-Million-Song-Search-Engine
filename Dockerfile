# Docker image for flask python run
# VERSION 1.0
# Author: Weiye
# ��������ʹ��python:3.9
FROM python:3.9
# ָ����������Ŀ¼Ϊ /project/
WORKDIR /project/
# ��װ ��Ŀ����
RUN pip install pandas flask psycopg2 -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

COPY . .
# ����
ENTRYPOINT ["python","app.py"]

# ����
# docker build -t weiye/flask-project:v1 .

# run
#docker run -it -p 7090:7090 --name flask-project \
#-v /mydata/flaskProject:/project \
#-d weiye/flask-project:v1
