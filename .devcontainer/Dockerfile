ARG IMAGE=bullseye
FROM mcr.microsoft.com/devcontainers/${IMAGE}

ENV PYTHONUNBUFFERED 1

# OS パッケージと Node.js のみインストール
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends postgresql-client curl build-essential \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリ
WORKDIR /workspace
