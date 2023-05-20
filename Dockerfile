FROM williamfzc/srctx:v0.6.0

RUN apk add --no-cache graphviz curl git

COPY . /action_internal

# python lsif
RUN apk add --no-cache python3 py3-pip && \
    pip3 install -r /action_internal/requirements.txt && \
    pip3 install --upgrade git+https://github.com/sourcegraph/lsif-py.git

# scip converter
RUN git clone https://github.com/sourcegraph/scip.git --depth=1 ./scip_repo && \
    cd scip_repo && \
    go build -o scip ./cmd && \
    cd .. && \
    cp ./scip_repo/scip . && \
    rm -rf ./scip_repo && \
    chmod +x ./scip && \
    scip --help

# java/kotlin/scala scip/lsif
RUN apk add openjdk8 gradle maven \
  && curl -fLo coursier https://git.io/coursier-cli \
  && chmod +x coursier \
  && ./coursier bootstrap --standalone -o scip-java com.sourcegraph:scip-java_2.13:0.8.18 --main com.sourcegraph.scip_java.ScipJava \
  && ./scip-java --help

ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk

ENTRYPOINT ["python3", "/action_internal/main.py"]
