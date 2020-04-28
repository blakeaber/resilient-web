FROM python:3.7

RUN set -ex && \
    pip install dash dash-daq dash-bootstrap-components numpy pandas scipy

EXPOSE 8050
COPY . /app
WORKDIR /app

ENV DASH_DEBUG_MODE True

CMD ["python", "index.py"]
