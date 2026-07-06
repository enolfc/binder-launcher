FROM jupyter/base-notebook:latest

USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends git curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER jovyan

WORKDIR /home/jovyan

COPY --chown=jovyan:users . /home/jovyan

RUN python -m pip install .

RUN jupyter server extension enable \
      --py binder_launcher \
      --sys-prefix


CMD ["jupyter", "lab", \
     "--ServerApp.root_dir=/home/jovyan", \
     "--ServerApp.ip=0.0.0.0", \
     "--ServerApp.allow_origin=*", \
     "--ServerApp.token=", \
     "--ServerApp.password=", \
     "--ServerApp.log_level=DEBUG"]
