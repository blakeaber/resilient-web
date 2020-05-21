FROM python:3.7

RUN set -ex && \
    pip install dash dash-daq dash-bootstrap-components \
                numpy scipy pandas psycopg2 gunicorn

COPY . /resilientai
WORKDIR /resilientai
EXPOSE 5000

ENV RDS_ENDPOINT blake
ENV RDS_USER ***REMOVED***
ENV RDS_PASS ***REMOVED***

# CMD ["python", "index.py"]
# https://pythonspeed.com/articles/gunicorn-in-docker/
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "index:app.server"]


