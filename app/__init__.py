from typing import Optional, Tuple

from flask import Flask, redirect, render_template, request, url_for

from app.auth import auth_bp
from app.auth.models import User
from app.auth.security import JWT_COOKIE_NAME, clear_auth_cookie, decode_token
from app.db import get_session, init_db, remove_session


def _load_user_from_token() -> Tuple[Optional[User], bool]:
    token = request.cookies.get(JWT_COOKIE_NAME)
    if not token:
        return None, False

    payload = decode_token(token)
    if not payload or "sub" not in payload:
        return None, True

    session = get_session()
    user = session.get(User, int(payload["sub"]))
    return user, user is None


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates")

    app.register_blueprint(auth_bp)

    @app.get("/")
    def read_root():
        user, token_invalid = _load_user_from_token()
        if not user:
            resp = redirect(url_for("auth.login", next=request.path))
            if token_invalid:
                resp = clear_auth_cookie(resp)
            return resp

        return render_template("home.html", user=user)

    init_db()
    app.teardown_appcontext(remove_session)
    return app


app = create_app()
