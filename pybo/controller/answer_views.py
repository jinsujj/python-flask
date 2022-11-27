from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g, flash, session

from werkzeug.utils import redirect

from pybo import db
from pybo.models import Question, Answer, User

from ..forms import AnswerForm, QuestionForm

bp = Blueprint("answer", __name__, url_prefix="/answer")


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


@bp.route("/create/<int:question_id>", methods=("POST",))
def create(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    print(g.user)
    if form.validate_on_submit():
        content = request.form["content"]
        answer = Answer(
            content=content,
            create_date=datetime.now(),
            user=g.user,
        )
        question.answer_set.append(answer)
        db.session.commit()
        return redirect(url_for("question.detail", question_id=question_id))
    return render_template(
        "question/question_detail.html", question=question, form=form
    )


@bp.route("/modify/<int:answer_id>", methods=("GET", "POST"))
def modify(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    if g.user != answer.user:
        flash("수정권한이 없습니다")
        return redirect(url_for("question.detail", question_id=answer.question.id))
    if request.method == "POST":
        form = AnswerForm()
        if form.validate_on_submit():
            form.populate_obj(answer)
            answer.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for("question.detail", question_id=answer.question.id))
    else:
        form = AnswerForm(obj=answer)
    return render_template("answer/answer_form.html", form=form)


@bp.route("/delete/<int:answer_id>")
def delete(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    question_id = answer.question.id
    if g.user != answer.user:
        flash("삭제권한이 없습니다")
    else:
        db.session.delete(answer)
        db.session.commit()
    return redirect(url_for("question.detail", question_id=question_id))
