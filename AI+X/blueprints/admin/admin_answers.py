from flask import Blueprint, render_template, request, g, redirect, url_for, flash
from blueprints.forms import QuestionForm, AnswerForm, EditAnswerForm
from decorators import admin_login_required
from exts import db
from models import AnswerModel, UserModel

# /auth
bp = Blueprint('admin_answer', __name__, url_prefix='/admin_answer')


# http://127.0.0.1:5000
@bp.route('/')
@admin_login_required
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 5  # Set the number of questions per page
    offset = (page - 1) * per_page
    answers = AnswerModel.query.limit(per_page).offset(offset).all()
    total_answers = AnswerModel.query.count()
    pages = total_answers // per_page + (total_answers % per_page > 0)
    print(answers)

    return render_template('admin/answer/admin_answer.html', answers=answers,
                           total_answers=total_answers, per_page=per_page,
                           pages=pages, page=page)


@bp.route('/add_answer', methods=['GET', 'POST'])
@admin_login_required
def add_answer():
    print(request.method)

    if request.method == 'POST':
        print(request.form)
        form = AnswerForm(request.form)
        new_answer = AnswerModel(
            question_id=form.question_id.data,
            content=form.content.data,
            author_id = '111'
        )

        db.session.add(new_answer)
        db.session.commit()
        flash('New question was added successfully!', 'success')
        return redirect(url_for('admin_answer.index'))
    return render_template('admin/answer/add_answer.html')


@bp.route('/delete_answer/<answer_id>', methods=['GET', 'POST'])
@admin_login_required
def delete_answer(answer_id):
    answer = AnswerModel.query.get_or_404(answer_id)
    db.session.delete(answer)
    db.session.commit()
    return redirect(url_for('admin_answer.index'))
