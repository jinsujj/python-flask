from flask import Blueprint, render_template, request, url_for, session, g, flash
from pybo.forms import AnswerForm, QuestionForm

from pybo.models import Question, User, Answer, User
from datetime import datetime
from werkzeug.utils import redirect
from logging import Logger
from .. import db


bp = Blueprint("question", __name__, url_prefix="/question")


@bp.before_request
def load_logged_in_user():
    # g 는 플라스크 컨텍스트 변수
    # 이변수는 request 와 마찬가지로 [요청 -> 응답] 과정에서 유효하다
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)
    print("User: " + str(g.user))


@bp.route("/list/")
def _list():
    page = request.args.get("page", type=int, default=1)
    kw = request.args.get("kw", type=str, default="")
    question_list = Question.query.order_by(Question.create_date.desc())

    if kw:
        search = "%%{}%%".format(kw)
        sub_query = (
            db.session.query(Answer.question_id, Answer.content, User.username)
            .join(User, Answer.user_id == User.id)
            .subquery()
        )

        question_list = (
            question_list.join(User)
            .outerjoin(sub_query, sub_query.c.question_id == Question.id)
            .filter(
                Question.subject.ilike(search)
                | Question.content.ilike(search)
                | User.username.ilike(search)
                | sub_query.c.content.ilike(search)
                | sub_query.c.username.ilike(search)
            )
            .distinct()
        )
    question_list = question_list.paginate(page=page, per_page=10)
    return render_template(
        "question/question_list.html", question_list=question_list, page=page, kw=kw
    )


@bp.route("/detail/<int:question_id>/")
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    return render_template(
        "question/question_detail.html", question=question, form=form
    )


@bp.route("/create/", methods={"GET", "POST"})
def create():
    form = QuestionForm()
    print(form.validate_on_submit())
    if request.method == "POST" and form.validate_on_submit():
        question = Question(
            subject=form.subject.data,
            content=form.content.data,
            create_date=datetime.now(),
            user=g.user,
        )

        db.session.add(question)
        db.session.commit()
        return redirect(url_for("main.index"))

    return render_template("question/question_form.html", form=form)


@bp.route("/modify/<int:question_id>", methods=("GET", "POST"))
# @login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)

    print(g.user)
    print(question.user)
    if g.user != question.user:
        flash("수정권한이 없습니다")
        return redirect(url_for("question.detail", question_id=question_id))

    if request.method == "POST":
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)
            question.modify_date = datetime.now()
            db.session.commit()
            return redirect(url_for("question.detail", question_id=question_id))
    else:
        form = QuestionForm()
    return render_template("question/question_form.html", form=form)


@bp.route("/delete/<int:question_id>")
# @login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash("삭제권한이 없습니다")
        return redirect(url_for("question.detail", question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for("question._list"))


@bp.route("/vote/<int:question_id>")
def vote(question_id):
    _question = Question.query.get_or_404(question_id)
    if g.user == _question.user:
        flash("본인이 작성한 글은 추천할 수 없습니다")
    else:
        _question.voter.append(g.user)
        db.session.commit()
    return redirect(url_for("question.detail", question_id=question_id))
