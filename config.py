#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

SECRET_KEY = os.environ.get('SECRET_KEY') or 'il manque quelque chose'
ID_KEY = os.environ.get('ID_KEY') or 'probleme de code'