FROM williamfzc/srctx:v0.4.2

RUN apk add --no-cache graphviz curl

COPY . /action_internal

# python lsif
RUN apk add --no-cache python3 py3-pip && \
    pip3 install -r /action_internal/requirements.txt && \
    pip3 install --upgrade git+https://github.com/sourcegraph/lsif-py.git

# scip converter
RUN curl -fLo scip-linux-amd64.tar.gz https://github.com/sourcegraph/scip/releases/download/v0.2.3/scip-linux-amd64.tar.gz \
  && tar xf ./scip-linux-amd64.tar.gz \
  && chmod +x ./scip

# java/kotlin/scala scip/lsif
RUN apk add openjdk17 \
  && curl -fLo coursier https://git.io/coursier-cli \
  && chmod +x coursier \
  && ./coursier bootstrap --standalone -o scip-java com.sourcegraph:scip-java_2.13:0.8.18 --main com.sourcegraph.scip_java.ScipJava \
  && ./scip-java --help

ENTRYPOINT ["python3", "/action_internal/main.py"]
