# -*- coding: utf-8 -*-
#
# webb.org
# Copyright 2014 ESO & ESA/Hubble
#
# Authors:
#   Mathias Andre <mandre@eso.org>

from __future__ import absolute_import

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app
