FROM python:3.7

RUN set -ex && \
    pip install dash dash-daq dash-bootstrap-components \
                numpy scipy pandas psycopg2

COPY . /app
WORKDIR /app
EXPOSE 5000

CMD ["python", "index.py"]
