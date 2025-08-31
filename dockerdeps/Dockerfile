FROM public.ecr.aws/lambda/python:3.10
WORKDIR /var/task
COPY requirements.txt .
RUN pip install --no-cache-dir firebase-admin==5.3.0 boto3==1.24.12 requests==2.28.1 protobuf==3.20.3 grpcio==1.46.0 -t .