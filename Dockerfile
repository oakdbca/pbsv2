# syntax = docker/dockerfile:1.2

FROM ubuntu:22.04 as builder_base_oim_pbsv2

LABEL maintainer="asi@dbca.wa.gov.au"
LABEL org.opencontainers.image.source="https://github.com/dbca-wa/pbsv2"

ENV DEBIAN_FRONTEND=noninteractive \
    DEB_PYTHON_INSTALL_LAYOUT=deb \
    DEBUG=True \
    TZ=Australia/Perth \
    PRODUCTION_EMAIL=True \
    SECRET_KEY="ThisisNotRealKey" \
    SITE_DOMAIN='dbca.wa.gov.au' \
    BPAY_ALLOWED=False \
    POETRY_VERSION=1.6.1 \
    NODE_MAJOR=20

# Use Australian Mirrors
RUN sed 's/archive.ubuntu.com/au.archive.ubuntu.com/g' /etc/apt/sources.list > /etc/apt/sourcesau.list && \
    mv /etc/apt/sourcesau.list /etc/apt/sources.list

RUN --mount=type=cache,target=/var/cache/apt apt-get update && \
    apt-get upgrade -y && \
    apt-get install --no-install-recommends -y \
    binutils \
    ca-certificates \
    cron \
    curl \
    gdal-bin \
    gnupg \
    gcc \
    git \
    htop \
    libmagic-dev \
    libproj-dev \
    libpq-dev \
    libspatialindex-dev \
    mtr \
    patch \
    postgresql-client \
    python3-dev \
    python3-pip \
    python3-setuptools \
    python3-gdal \
    rsyslog \
    software-properties-common \
    sqlite3 \
    ssh \
    sudo \
    tzdata \
    vim \
    wget && \
    update-ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# install node 20
RUN mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
    echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" \
    | tee /etc/apt/sources.list.d/nodesource.list && \
    apt-get update && \
    apt-get install -y nodejs && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    pip install --upgrade pip

COPY cron /etc/cron.d/dockercron
COPY startup.sh pre_startup.sh /
COPY ./timezone /etc/timezone
RUN chmod 0644 /etc/cron.d/dockercron && \
    crontab /etc/cron.d/dockercron && \
    touch /var/log/cron.log && \
    service cron start && \
    chmod 755 /startup.sh && \
    chmod +s /startup.sh && \
    chmod 755 /pre_startup.sh && \
    chmod +s /pre_startup.sh && \
    groupadd -g 5000 oim && \
    useradd -g 5000 -u 5000 oim -s /bin/bash -d /app && \
    usermod -a -G sudo oim && \
    echo "oim  ALL=(ALL)  NOPASSWD: /startup.sh" > /etc/sudoers.d/oim && \
    mkdir /app && \
    chown -R oim.oim /app && \
    mkdir /container-config/ && \
    chown -R oim.oim /container-config/ && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
    touch /app/rand_hash

# Install python dependencies
FROM builder_base_oim_pbsv2 as python_dependencies_pbsv2

WORKDIR /app
USER oim
ENV PATH=/app/.local/bin:$PATH
COPY --chown=oim:oim gunicorn.conf.py manage.py manage.sh startup.sh pyproject.toml poetry.lock ./
RUN pip install "poetry==$POETRY_VERSION"
RUN --mount=type=cache,target=~/.cache/pypoetry/cache poetry install --only main --no-interaction --no-ansi

COPY --chown=oim:oim govapp ./govapp
COPY --chown=oim:oim .git ./.git

# Collect static files
FROM python_dependencies_pbsv2 as collect_static_pbsv2
RUN touch /app/.env && \
    poetry run python manage.py collectstatic --no-input

# Do a clean install of the vue 3 application
FROM collect_static_pbsv2 as install_build_vue3_pbsv2

RUN cd /app/govapp/frontend/pbs ; npm ci --omit=dev && \
    cd /app/govapp/frontend/pbs ; npm run build

# Launch the application
FROM install_build_vue3_pbsv2 as launch_pbsv2

EXPOSE 8080
HEALTHCHECK --interval=1m --timeout=5s --start-period=10s --retries=3 CMD ["wget", "-q", "-O", "-", "http://localhost:8080/"]
CMD ["/pre_startup.sh"]
