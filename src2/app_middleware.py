# -*- coding: utf-8 -*-

from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
# from starlette_wtf import CSRFProtectMiddleware
import secrets
# from core.custom_middleware import LoggerMiddleware
# from settings import config_settings

middleware = [
    Middleware(
        SessionMiddleware,
        secret_key=secrets.token_hex(32),
        max_age=86400,
        same_site="strict",
        session_cookie="session_set",
    ),
    # Middleware(CSRFProtectMiddleware, csrf_secret=config_settings.csrf_secret),
    # Middleware(PrometheusMiddleware),
    # Middleware(LoggerMiddleware),
]
