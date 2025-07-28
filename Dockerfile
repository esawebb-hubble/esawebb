#############################################
# BUILDER IMAGE: Only for building the code #
#############################################
FROM python:3.8-slim-bullseye AS builder
# Follow Dockerfile RUN best practices (Keep packages organized alphabetically):
# See: https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#run
# - gcc, libsasl2-dev, libsasl2-dev, libssl-dev and python-dev are required by django-auth-ldap
# - git is required to install private dependencies with pip
RUN apt-get update && apt-get install -y \
    gcc \
    git \
    libldap2-dev \
    libsasl2-dev \
    libssl-dev \
    python3-dev


# Create user for building and installing pip packages inside its home for security purposes
RUN useradd --create-home webbbuilder
ENV BUILDER_HOME=/home/webbbuilder
WORKDIR $BUILDER_HOME
USER webbbuilder

# Cache layer with private requirements
COPY private-requirements.txt .
RUN pip install --user -r private-requirements.txt --find-links https://djangoplicity.org/packages/

# Install third party dependencies and create layer cache of them
COPY requirements.txt .
RUN pip install --user -r requirements.txt --find-links https://djangoplicity.org/packages/

# Install test dependencies and create layer cache of them
COPY test-requirements.txt .
RUN pip install --user -r test-requirements.txt

######################################
# RUNNER IMAGE: For running the code #
######################################

# FROM djangoplicity/base:initial
FROM python:3.8-slim-bullseye

# Install here only runtime required packages
# - cssmin and node-uglify are the processors used by django pipeline
# - ffmpeg and mplayer are required for videos processing
# - imagemagick is used for process images and generate derivatives
# - libldap-2.4-2 are runtime libraries for the OpenLDAP use by django-auth-ldap
# - libexempi-dev is required by python-avm-library(libavm) and python-xmp-toolkit
# - rsync and openssh-client are required to synchronize files to CDN77
RUN apt-get update && apt-get install -y \
    cssmin \
    ffmpeg \
    imagemagick-6.q16 \
    libldap-2.4-2 \
    mplayer \
    node-uglify \
    libexempi-dev \
    rsync \
    openssh-client \
    zip

RUN echo "Europe/Berlin" > /etc/timezone && \
    rm /etc/localtime && \
    ln -s /usr/share/zoneinfo/Europe/Berlin /etc/localtime
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

RUN groupadd -g 2000 webbadm && \
    useradd -u 2000 -g webbadm --create-home webbadm

ENV USER_HOME=/home/webbadm
WORKDIR $USER_HOME

USER webbadm

# Copy ImageMagick settings
COPY --chown=webbadm config/imagemagick/policy.xml /etc/ImageMagick-6/

# Copy pip install results from builder image
COPY --from=builder --chown=webbadm /home/webbbuilder/.local $USER_HOME/.local

# Make sure scripts installed by pip in .local are usable:
ENV PATH=$USER_HOME/.local/bin:$PATH

RUN mkdir -p static \
    media/archives/ \
    logs \
    tmp \
    import \
    shared

COPY --chown=webbadm scripts/ scripts/
COPY --chown=webbadm scripts/newrelic.ini ./

COPY --chown=webbadm .coveragerc .
COPY --chown=webbadm manage.py manage.py
COPY --chown=webbadm webb/ webb/
# COPY --chown=webbadm webb/static/fonts/helvetica/ /usr/share/fonts/truetype/helvetica/
