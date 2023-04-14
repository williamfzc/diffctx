FROM williamfzc/srctx:v0.2.0

RUN apk add --no-cache python3 py3-pip

COPY . .

ENTRYPOINT ["python3", "./main.py"]
