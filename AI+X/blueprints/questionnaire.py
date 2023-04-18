from datetime import datetime

import wtforms
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from sqlalchemy.sql.functions import current_user

from blueprints.forms import Answer_QuestionnaireForm, QuestionnaireForm, Questionnaire_QuestionForm
from decorators import login_required

from exts import db
from models import QuestionnaireModel, Questionnaire_AnswerModel, Questionnaire_QuestionModel, Questionnaire_OptionModel

bp = Blueprint('questionnaire', __name__, url_prefix='/questionnaire')


@bp.route('/', methods=['GET', 'POST'])
def index():
    # 实例化Questionnaire类对象
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Set the number of questions per page
    questionnaires = QuestionnaireModel.query.paginate(page=page, per_page=per_page)
    user_id = session.get('user_id')
    return render_template('user/questionnaire/questionnaire.html', questionnaires=questionnaires, user_id = user_id)


@bp.route('/answer/<int:questionnaire_id>', methods=['GET', 'POST'])
@login_required
def answer_questionnaire(questionnaire_id):
    questionnaire = QuestionnaireModel.query.get(questionnaire_id)
    if questionnaire is None:
        flash('问卷不存在')
        return redirect(url_for('questionnaire.index'))

    questions = questionnaire.questions
    if request.method == 'POST':
        answers = [Questionnaire_AnswerModel(
            question_id=question.id,
            option_id=request.form.get(f'question_{question.id}') if question.type == 1 else None,
            content=request.form.get(f'question_{question.id}') if question.type == 0 else None,
            user_id=int(session.get('user_id')),
            created_at=datetime.now(),
            updated_at=datetime.now())
            for question in questions
        ]
        db.session.add_all(answers)
        db.session.commit()
        flash('感谢您的答复。')
        return redirect(url_for('questionnaire.index'))

    return render_template('user/questionnaire/answer_questionnaire.html', questionnaire=questionnaire, questions=questions)


@bp.route('/add_questionnaire', methods=['GET', 'POST'])
@login_required
def add_questionnaire():
    if request.method == 'POST':
        form = QuestionnaireForm(request.form)
        questionnaire = QuestionnaireModel(title=form.title.data,
                                           description=form.description.data,
                                           user_id=session.get('user_id'))
        db.session.add(questionnaire)
        db.session.commit()
        flash('调查表添加成功', 'success')
        return redirect(url_for('questionnaire.edit_questionnaire', questionnaire_id=questionnaire.id))
    return render_template('user/questionnaire/add_questionnaire.html')


@bp.route('/edit_questionnaire/<int:questionnaire_id>', methods=['GET', 'POST'])
@login_required
def edit_questionnaire(questionnaire_id):
    questionnaire = QuestionnaireModel.query.get_or_404(questionnaire_id)
    form = QuestionnaireForm(obj=questionnaire)
    if request.method == 'POST':
        form.populate_obj(questionnaire)
        db.session.commit()
        flash('调查表更新成功', 'success')
        return redirect(url_for('questionnaire.edit_questionnaire', questionnaire_id=questionnaire.id))
    return render_template('user/questionnaire/edit_questionnaire.html', questionnaire=questionnaire, form=form)


@bp.route('/add_question/<int:questionnaire_id>', methods=['GET', 'POST'])
@login_required
def add_question(questionnaire_id):
    form = Questionnaire_QuestionForm(request.form)
    if request.method == 'POST':
        question = Questionnaire_QuestionModel(content=form.content.data,
                                               type=form.type.data,
                                               questionnaire_id=questionnaire_id)
        db.session.add(question)
        db.session.commit()
        if form.type.data == '1':  # 如果是选择题
            return redirect(url_for('questionnaire.add_option', question_id=question.id))
        else:
            flash('问题添加成功', 'success')
            return redirect(url_for('questionnaire.edit_questionnaire', questionnaire_id=questionnaire_id))
    return render_template('user/questionnaire/add_question.html', form=form)



@bp.route('/edit_question/<int:question_id>', methods=['GET', 'POST'])
@login_required
def edit_question(question_id):
    question = Questionnaire_QuestionModel.query.filter_by(id=question_id).first_or_404()
    form = Questionnaire_QuestionForm(request.form)
    print(request.method)
    if request.method == 'POST':
        question.content = form.content.data
        question.type = form.type.data
        db.session.commit()
        print(question.content)
        print(question.type)
        flash('The competition has been updated successfully.', 'success')
        return redirect(url_for('questionnaire.edit_questionnaire', questionnaire_id=question.questionnaire_id))

    form.content.data = question.content
    form.type.data = question.type

    return render_template('user/questionnaire/edit_question.html', question=question, form=form)



@bp.route('/delete_questionnaire/<int:questionnaire_id>', methods=['GET', 'POST'])
@login_required
def delete_questionnaire(questionnaire_id):
    questionnaire = QuestionnaireModel.query.get(questionnaire_id)
    if not questionnaire:
        flash('调查问卷不存在', 'error')
        return redirect(url_for('questionnaire.index'))

    db.session.delete(questionnaire)
    db.session.commit()
    flash('调查问卷删除成功', 'success')

    return redirect(url_for('questionnaire.index'))

@bp.route('/add_option/<int:question_id>', methods=['GET', 'POST'])
@login_required
def add_option(question_id):
    question = Questionnaire_QuestionModel.query.get_or_404(question_id)
    form = Questionnaire_QuestionForm(request.form)
    if request.method == 'POST':
        options = form.options.data
        for content in options:
            question_option = Questionnaire_OptionModel(
                content=content['content'],
                question_id=question.id
            )
            db.session.add(question_option)
        db.session.commit()
        flash('New question option was added successfully!', 'success')
        return redirect(url_for('questionnaire.edit_question', question_id=question_id))
    return render_template('user/questionnaire/add_option.html', form=form, question=question)


@bp.route('/delete_question/<int:question_id>', methods=['POST', 'GET'])
def delete_question(question_id):
    question = Questionnaire_QuestionModel.query.get_or_404(question_id)

    db.session.delete(question)
    db.session.commit()

    flash('问题删除成功', 'success')
    return redirect(url_for('questionnaire.edit_questionnaire', questionnaire_id=question.questionnaire_id))
