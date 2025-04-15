#!/usr/bin/env bash

apt update && apt install -y python3-setuptools
pipx install poetry==${POETRY_VERSION}
poetry self add poetry-dotenv-plugin
