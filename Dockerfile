#############################################
# BUILDER IMAGE: Only for building the code #
#############################################
FROM python:2.7-slim-buster AS builder
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
    python-dev


# Create user for building and installing pip packages inside its home for security purposes
RUN useradd --create-home hubblebuilder
ENV BUILDER_HOME=/home/hubblebuilder
WORKDIR $BUILDER_HOME
USER hubblebuilder

# Cache layer with private requirements
COPY private-requirements.txt .
RUN pip install --user -r private-requirements.txt --find-links https://www.djangoplicity.org/repository/packages/

# Install third party dependencies and create layer cache of them
COPY requirements.txt .
RUN pip install --user -r requirements.txt --find-links https://www.djangoplicity.org/repository/packages/

# Install test dependencies and create layer cache of them
COPY test-requirements.txt .
RUN pip install --user -r test-requirements.txt

######################################
# RUNNER IMAGE: For running the code #
######################################

# FROM djangoplicity/base:initial
FROM python:2.7-slim-buster

# Install here only runtime required packages
# - cssmin and node-uglify are the processors used by django pipeline
# - ffmpeg and mplayer are required for videos processing
# - imagemagick is used for process images and generate derivatives
# - libldap-2.4-2 are runtime libraries for the OpenLDAP use by django-auth-ldap
# - libexempi-dev is required by python-avm-library(libavm) and python-xmp-toolkit
RUN apt-get update && apt-get install -y \
    cssmin \
    ffmpeg \
    imagemagick-6.q16 \
    libldap-2.4-2 \
    mplayer \
    node-uglify \
    libexempi-dev

RUN useradd --create-home hubbleadm
ENV USER_HOME=/home/hubbleadm
WORKDIR $USER_HOME

USER hubbleadm

# Copy pip install results from builder image
COPY --from=builder --chown=hubbleadm /home/hubblebuilder/.local $USER_HOME/.local

# Make sure scripts installed by pip in .local are usable:
ENV PATH=$USER_HOME/.local/bin:$PATH

# ENV DJANGO_SETTINGS_MODULE spacetelescope.settings

RUN mkdir -p static \
    docs/static/ \
    logs \
    tmp \
    import \
    shared

COPY --chown=hubbleadm scripts/ scripts/

COPY --chown=hubbleadm .coveragerc .
COPY --chown=hubbleadm manage.py manage.py
COPY --chown=hubbleadm spacetelescope/ spacetelescope/
