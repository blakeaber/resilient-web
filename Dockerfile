FROM python:3.7

RUN set -ex && \
    pip install dash dash-daq dash-bootstrap-components numpy scipy pandas

EXPOSE 5000
COPY . /app
WORKDIR /app

ENV DASH_DEBUG_MODE True
ENV APP_PORT 5000

CMD ["python", "index.py"]
