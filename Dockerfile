FROM python:3.7

RUN set -ex && \
    pip install dash dash-daq dash-bootstrap-components \
                numpy scipy pandas psycopg2 gunicorn boto3

COPY . /resilientai
WORKDIR /resilientai
EXPOSE 5000

ENV RDS_USER blake
ENV RDS_PASS !?ba94!:fx7
ENV RDS_ENDPOINT resilient-ai-db-dev.cpyof9gq0ppq.us-east-1.rds.amazonaws.com
ENV RDS_PORT 5432

# CMD ["python", "index.py"]
# https://pythonspeed.com/articles/gunicorn-in-docker/
CMD ["gunicorn", "-w", "5", "--bind", "0.0.0.0:5000", "index:server"]


