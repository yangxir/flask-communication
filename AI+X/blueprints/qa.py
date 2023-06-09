from flask import Blueprint, render_template, request, g, redirect, url_for
from .forms import QuestionForm, AnswerForm
from exts import db
from decorators import login_required,admin_login_required
from models import QuestionModel, AnswerModel, UserModel

# /auth
bp = Blueprint('AI+X', __name__, url_prefix='/')


# http://127.0.0.1:5000
@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 5  # Set the number of questions per page
    offset = (page - 1) * per_page
    questions = QuestionModel.query.limit(per_page).offset(offset).all()
    total_questions = QuestionModel.query.count()
    pages = total_questions // per_page + (total_questions % per_page > 0)
    return render_template('index.html', questions=questions, total_questions=total_questions, per_page=per_page, pages=pages, page=page)




@bp.route('/qa/public', methods=['GET', 'POST'])
@login_required
def public_question():
    if request.method == 'GET':
        return render_template('public_question.html')
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title, content=content, author=g.user)
            db.session.add(question)
            db.session.commit()
            # todo 跳转到问答详情页
            return redirect('/')
        else:
            print(form.errors)
            return redirect(url_for('AI+X.public_question'))


@bp.route('/qa/detail/<qa_id>')
def qa_detail(qa_id):
    question = QuestionModel.query.get(qa_id)
    return render_template('detail.html', question=question)


@bp.route('/answer/public', methods=['POST'])
@login_required
def public_answer():
    form = AnswerForm(request.form)
    if form.validate():
        content = form.content.data
        question_id = form.question_id.data
        answer = AnswerModel(content=content, question_id=question_id, author_id=g.user.id)
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for('AI+X.qa_detail', qa_id=question_id))
    else:
        print(form.errors)
        return redirect(url_for('AI+X.qa_detail', qa_id=request.form.get('question_id')))


@bp.route('/search')
def search():
    q = request.args.get('q')
    page = request.args.get('page', 1, type=int)
    per_page = 5
    offset = (page - 1) * per_page

    if q:
        questions = QuestionModel.query.filter(QuestionModel.title.contains(q)).limit(per_page).offset(offset).all()
        total_questions = QuestionModel.query.filter(QuestionModel.title.contains(q)).count()
    else:
        questions = QuestionModel.query.limit(per_page).offset(offset).all()
        total_questions = QuestionModel.query.count()

    pages = total_questions // per_page + (total_questions % per_page > 0)

    return render_template('index.html', questions=questions, total_questions=total_questions, per_page=per_page, pages=pages, page=page)

