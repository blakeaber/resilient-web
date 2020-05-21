FROM python:3.7

RUN set -ex && \
    pip install dash dash-daq dash-bootstrap-components \
                numpy scipy pandas psycopg2 gunicorn

COPY . /resilientai
WORKDIR /resilientai
EXPOSE 5000

ENV RDS_ENDPOINT blake
ENV RDS_USER !?ba94!:fx7
ENV RDS_PASS resilient-ai-db-dev.cpyof9gq0ppq.us-east-1.rds.amazonaws.com

# CMD ["python", "index.py"]
# https://pythonspeed.com/articles/gunicorn-in-docker/
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "index:app.server"]


