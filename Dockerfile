FROM python:alpine

RUN pip install --no-cache-dir schedule boto3

COPY job.py /

CMD ["python", "-u", "/job.py"]
