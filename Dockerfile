FROM williamfzc/srctx:v0.2.1

RUN apk add --no-cache python3 py3-pip

COPY . /action_internal

RUN pip3 install -r /action_internal/requirements.txt && \
    pip3 install --upgrade git+https://github.com/sourcegraph/lsif-py.git

ENTRYPOINT ["python3", "/action_internal/main.py"]
