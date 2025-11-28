from urllib.parse import urlparse

from flask import Blueprint, jsonify, make_response, redirect, render_template, request, url_for
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from app.auth.models import User
from app.auth.security import (
    JWT_COOKIE_NAME,
    clear_auth_cookie,
    create_token,
    decode_token,
    set_auth_cookie,
)
from app.db import get_session

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


def wants_json_response() -> bool:
    if request.is_json:
        return True
    best = request.accept_mimetypes.best_match(["application/json", "text/html"])
    return best == "application/json" and request.accept_mimetypes[best] > request.accept_mimetypes.get(  # type: ignore[index]
        "text/html", 0
    )


def _safe_next_url(default: str) -> str:
    next_url = request.args.get("next") or default
    parsed = urlparse(next_url)
    if parsed.scheme or parsed.netloc:
        return default
    return next_url


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    error = None
    if request.method == "POST":
        data = request.get_json(silent=True) or request.form
        email = (data.get("email") or "").strip().lower()
        password = (data.get("password") or "").strip()

        if not email or not password:
            error = "Informe email e senha."
        else:
            session = get_session()
            user = User(email=email, password_hash=generate_password_hash(password))
            session.add(user)
            try:
                session.commit()
            except IntegrityError:
                session.rollback()
                error = "Email já cadastrado."
            else:
                if wants_json_response():
                    resp = jsonify({"message": "Usuário criado com sucesso"})
                    resp.status_code = 201
                    return resp
                return redirect(url_for("auth.login"))

        if wants_json_response():
            status = 400
            return jsonify({"error": error}), status

    return render_template("signup.html", error=error)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    error = None
    token_in_cookie = request.cookies.get(JWT_COOKIE_NAME)
    if request.method == "GET" and token_in_cookie:
        payload = decode_token(token_in_cookie)
        if payload:
            return redirect(url_for("read_root"))
        error = "Sessão expirada. Faça login novamente."

    if request.method == "POST":
        data = request.get_json(silent=True) or request.form
        email = (data.get("email") or "").strip().lower()
        password = (data.get("password") or "").strip()

        if not email or not password:
            error = "Informe email e senha."
        else:
            session = get_session()
            user = session.query(User).filter(User.email == email).first()
            if not user or not check_password_hash(user.password_hash, password):
                error = "Credenciais inválidas."
            else:
                token = create_token(user.id, user.email)
                if wants_json_response():
                    resp = jsonify(
                        {
                            "token": token,
                            "token_type": "Bearer",
                            "user": {"email": user.email},
                        }
                    )
                else:
                    next_url = _safe_next_url(url_for("read_root"))
                    resp = redirect(next_url)

                return set_auth_cookie(resp, token)

        status = 401 if error == "Credenciais inválidas." else 400
        if wants_json_response():
            return jsonify({"error": error}), status

    status_code = 200
    if error == "Credenciais inválidas.":
        status_code = 401
    elif error:
        status_code = 400

    response = make_response(render_template("login.html", error=error), status_code)
    if token_in_cookie and error:
        clear_auth_cookie(response)
    return response


@auth_bp.get("/logout")
def logout():
    resp = redirect(url_for("auth.login"))
    return clear_auth_cookie(resp)
