FROM dbcawa/docker_app_dev:pbsv2_dev_latest AS build_dev

ENV POETRY_VERSION=1.6.1
ARG workspace_folder
ENV WORKSPACE_FOLDER=$workspace_folder

RUN apt update && \
    apt install -y sudo && \
    sudo apt install -y locate

# Add a non-root user
ARG USERNAME=container
RUN getent group $USERNAME || groupadd --gid 1000 $USERNAME && \
    getent passwd $USERNAME || useradd --uid 1000 --gid 1000 -m $USERNAME
# Add non-root user to sudoers
RUN usermod -aG sudo $USERNAME && \
    echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && sudo whoami

RUN mkdir -p /app && \
    chown container:container /app

## Make sure to reflect new user in PATH
ENV PATH="/home/${USERNAME}/.local/bin:${PATH}"
USER $USERNAME

# Install Poetry
FROM build_dev AS build_dev_poetry_install

WORKDIR $WORKSPACE_FOLDER
RUN pip install "poetry==$POETRY_VERSION" && \
    echo "Poetry binary location: $(which poetry)" && \
    echo "Poetry version: $(poetry --version)" && \
    echo "Workspace folder: $WORKSPACE_FOLDER" && \
    sleep 1

# Install Poetry dependencies
FROM build_dev_poetry_install AS build_dev_poetry_install_deps

COPY --chown=container:container pyproject.toml poetry.toml poetry.lock ./
RUN echo "$(poetry show -v | head -n 1)" && \
    sleep 1 && \
    poetry install --no-interaction --no-ansi && \
    poetry env info -p && \
    sleep 1

RUN poetry run python manage.py collectstatic --no-input
