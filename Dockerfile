FROM python:3.9-rc-alpine

RUN pip install --no-cache-dir boto3

COPY run.py /

CMD ["python", "-u", "/run.py"]
