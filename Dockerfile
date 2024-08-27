FROM python:3.11.9-alpine3.20

COPY ./requirements.txt /tmp/requirements.txt
COPY ./b3b /app/b3b
COPY ./* /app
WORKDIR /app
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        b3b-user 
        
ENV PATH="/py/bin:$PATH"
ENV TRADEDIR="/b3b/results"

USER b3b-user
