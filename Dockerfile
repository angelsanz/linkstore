FROM python:2.7

RUN mkdir /code
WORKDIR /code

COPY requirements.txt requirements.txt
COPY requirements-dev.txt requirements-dev.txt
COPY scripts/install-dependencies.bash scripts/install-dependencies.bash
RUN bash scripts/install-dependencies.bash

COPY linkstore linkstore
COPY setup.py setup.py
COPY scripts/install-package.bash scripts/install-package.bash
RUN bash scripts/install-package.bash
