import os

FEATURE_FLAGS = {
    "ENABLE_TEMPLATE_PROCESSING": True,
    "DASHBOARD_RBAC": False,  # disabled — was blocking public role access per-dashboard
    "SQLLAB_ASYNC_TIME_LIMIT_SEC": 60 * 5
}

ENABLE_PROXY_FIX = True

# Allow anonymous read-only access to dashboards (no login required for embeds).
# Public role gets same permissions as Gamma (read-only dashboard/chart access).
AUTH_ROLE_PUBLIC = "Public"
PUBLIC_ROLE_LIKE = "Gamma"

# Exempt dashboard views from CSRF checks so anonymous iframe embeds work.
WTF_CSRF_EXEMPT_LIST = [
    "superset.views.core",
    "superset.dashboards.api",
    "superset.charts.api",
    "superset.explore.api",
]

SECRET_KEY = os.environ.get("SECRET_KEY")

SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE")

# Allow embedding dashboards in iframes (for experiments dashboard).
# Keep Talisman enabled — only relax framing policy for known origins.
TALISMAN_CONFIG = {
    "frame_options": False,  # disable X-Frame-Options header; use CSP frame-ancestors instead
    "content_security_policy": {
        "default-src": ["'self'"],
        "script-src": ["'self'", "'unsafe-inline'", "'unsafe-eval'"],
        "style-src": ["'self'", "'unsafe-inline'"],
        "img-src": ["'self'", "data:", "blob:"],
        "font-src": ["'self'", "data:"],
        "connect-src": ["'self'"],
        "frame-ancestors": [
            "'self'",
            "http://100.124.184.101:*",   # Tailscale dev
            "http://localhost:*",
            os.environ.get("EXPERIMENTS_DASHBOARD_ORIGIN", ""),
        ],
    },
}