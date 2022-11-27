from flask import Blueprint, url_for
from werkzeug.utils import redirect

bp = Blueprint("main", __name__, url_prefix="/")


@bp.route("/hello")
def hello_pybo():
    return "hello Pybo!!"


@bp.route("/")
def index():
    3 / 0  # 강제로 오류발생
    return redirect(url_for("question._list"))
