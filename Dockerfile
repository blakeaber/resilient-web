FROM python:3.7

RUN set -ex && \
    pip install dash dash-daq dash-bootstrap-components \
                numpy scipy pandas psycopg2

COPY . /app
WORKDIR /app

ENV DASH_DEBUG_MODE True
ENV APP_PORT 5000

EXPOSE 5000

CMD ["python", "index.py"]
