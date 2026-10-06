# Jenkins for the PrestaShop stand.
#
# The jobs build and run the tests image on the host Docker daemon, so the
# container ships the Docker CLI and is started with the socket mounted.
FROM jenkins/jenkins:lts-jdk17

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        gnupg \
        unzip \
    && install -m 0755 -d /etc/apt/keyrings \
    && curl -fsSL https://download.docker.com/linux/debian/gpg \
        -o /etc/apt/keyrings/docker.asc \
    && chmod a+r /etc/apt/keyrings/docker.asc \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
        > /etc/apt/sources.list.d/docker.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends docker-ce-cli \
    && rm -rf /var/lib/apt/lists/*

# The Allure plugin renders the report with this command line tool.
ARG ALLURE_VERSION=2.46.1
RUN curl -sSL -o /tmp/allure.zip \
        "https://github.com/allure-framework/allure2/releases/download/${ALLURE_VERSION}/allure-${ALLURE_VERSION}.zip" \
    && unzip -q /tmp/allure.zip -d /opt \
    && ln -s "/opt/allure-${ALLURE_VERSION}/bin/allure" /usr/local/bin/allure \
    && rm /tmp/allure.zip

# Installed up front so a fresh container needs no manual plugin setup.
RUN jenkins-plugin-cli --plugins \
    allure-jenkins-plugin \
    configuration-as-code \
    git \
    workflow-aggregator

USER jenkins
