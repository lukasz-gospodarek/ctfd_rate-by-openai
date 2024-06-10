FROM python

WORKDIR /opt
RUN pip install --no-cache-dir openai fastapi uvicorn

RUN apt install curl

VOLUME '/opt'

ENTRYPOINT ["/usr/local/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8888", "--proxy-headers", "--root-path", "/opt"]