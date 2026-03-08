import os

FEATURE_FLAGS = {
    "ENABLE_TEMPLATE_PROCESSING": True,
    "DASHBOARD_RBAC": False,
    "SQLLAB_ASYNC_TIME_LIMIT_SEC": 60 * 5
}

ENABLE_PROXY_FIX = True

AUTH_ROLE_PUBLIC = "Public"
PUBLIC_ROLE_LIKE = "Gamma"

WTF_CSRF_ENABLED = False

SECRET_KEY = os.environ.get("SECRET_KEY")
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE")


def FLASK_APP_MUTATOR(app):
    """Auto-login anonymous users as a read-only public account for dashboard embeds."""

    @app.before_request
    def auto_login_anonymous():
        from flask_login import current_user, login_user

        if current_user.is_authenticated:
            return

        sm = app.appbuilder.sm
        pub_user = sm.find_user(username="public_viewer")
        if pub_user:
            login_user(pub_user, remember=False)


# Allow embedding dashboards in iframes (for experiments dashboard).
TALISMAN_CONFIG = {
    "frame_options": False,
    "content_security_policy": {
        "default-src": ["'self'"],
        "script-src": ["'self'", "'unsafe-inline'", "'unsafe-eval'"],
        "style-src": ["'self'", "'unsafe-inline'"],
        "img-src": ["'self'", "data:", "blob:"],
        "font-src": ["'self'", "data:"],
        "connect-src": ["'self'"],
        "frame-ancestors": [
            "'self'",
            "http://100.124.184.101:*",
            "http://localhost:*",
            os.environ.get("EXPERIMENTS_DASHBOARD_ORIGIN", ""),
        ],
    },
}
