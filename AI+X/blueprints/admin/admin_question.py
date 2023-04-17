from datetime import datetime

from flask import Blueprint, render_template, request, g, redirect, url_for, flash
from blueprints.forms import QuestionForm, AnswerForm
from exts import db
from decorators import login_required, admin_login_required
from models import QuestionModel, AnswerModel, UserModel

# /auth
bp = Blueprint('admin_question', __name__, url_prefix='/admin_question')


# http://127.0.0.1:5000
@bp.route('/')
@admin_login_required
def index():
    questions = QuestionModel.query.all()
    return render_template('admin/question/admin_question.html', questions=questions)


@bp.route('/add_question', methods=['GET', 'POST'])
@admin_login_required
def add_question():
    print(request.form)
    if request.method == 'POST':
        form = QuestionForm(request.form)
        new_question = QuestionModel(
            title=form.title.data,
            content=form.content.data,
            author_id = '111'
        )
        print(new_question.title)
        db.session.add(new_question)
        db.session.commit()
        flash('New question was added successfully!', 'success')
        return redirect(url_for('admin_question.index'))
    return render_template('admin/question/add_question.html')


class DeleteQuestionForm:
    pass


@bp.route('/delete_question/<int:question_id>', methods=['GET', 'POST'])
@admin_login_required
def delete_question(question_id):
    question = QuestionModel.query.get_or_404(question_id)
    form = DeleteQuestionForm()
    if request.method == 'POST':
        db.session.delete(question)
        db.session.commit()
        return redirect(url_for('admin_question.index'))
    return render_template('admin/question/delete_question.html',
                           question=question, form=form)


@bp.route('/edit_question/<int:question_id>', methods=['GET', 'POST'])
@admin_login_required
def edit_question(question_id):
    question = QuestionModel.query.get_or_404(question_id)
    form = QuestionForm(obj=question)
    if request.method=='POST':
        form.populate_obj(question)
        db.session.commit()
        flash('Question updated successfully!', 'success')
        return redirect(url_for('admin_question.index'))
    return render_template('admin/question/edit_question.html', form=form)
