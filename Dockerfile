FROM python:3.11.9-alpine3.20

ENV PYTHONUNBEFFERED 1

COPY .requirements.txt /tmp/requirements.txt

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        b3b-user && \
    mkdir bt_results && \
    mkdir data
        
ENV PATH="/py/bin:$PATH"

USER b3b-user
