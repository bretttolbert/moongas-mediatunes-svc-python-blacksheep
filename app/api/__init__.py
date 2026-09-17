from flask import Blueprint

bp = Blueprint("api", __name__)

from app.api import routes  # type: ignore  # noqa: E402,F401
