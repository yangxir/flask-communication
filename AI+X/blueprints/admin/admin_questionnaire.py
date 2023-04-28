from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app

from blueprints.forms import QuestionnaireForm, Questionnaire_QuestionForm
from decorators import admin_login_required
from exts import db
# /admin

from flask.views import MethodView

from models import QuestionnaireModel, Questionnaire_QuestionModel, Questionnaire_OptionModel, Questionnaire_AnswerModel

bp = Blueprint('admin_questionnaire', __name__, url_prefix='/admin_questionnaire')


@bp.route('/', methods=['GET', 'POST'])
@admin_login_required
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 5  # Set the number of questions per page
    offset = (page - 1) * per_page
    questionnaires = QuestionnaireModel.query.limit(per_page).offset(offset).all()
    total_questionnaires = QuestionnaireModel.query.count()
    pages = total_questionnaires // per_page + (total_questionnaires % per_page > 0)
    return render_template('admin/questionnaire/questionnaire.html', questionnaires=questionnaires,
                           total_questionnaires=total_questionnaires, per_page=per_page,
                           pages=pages, page=page
                           )


@bp.route('/add_questionnaire', methods=['GET', 'POST'])
@admin_login_required
def add_questionnaire():
    if request.method == 'POST':
        form = QuestionnaireForm(request.form)
        questionnaire = QuestionnaireModel(title=form.title.data,
                                           description=form.description.data)
        db.session.add(questionnaire)
        db.session.commit()
        flash('调查表添加成功', 'success')
        return redirect(url_for('admin_questionnaire.edit_questionnaire', questionnaire_id=questionnaire.id))
    return render_template('admin/questionnaire/add_questionnaire.html')


@bp.route('/edit_questionnaire/<int:questionnaire_id>', methods=['GET', 'POST'])
@admin_login_required
def edit_questionnaire(questionnaire_id):
    questionnaire = QuestionnaireModel.query.get_or_404(questionnaire_id)
    form = QuestionnaireForm(obj=questionnaire)
    if request.method == 'POST':
        form.populate_obj(questionnaire)
        db.session.commit()
        flash('调查表更新成功', 'success')
        return redirect(url_for('admin_questionnaire.edit_questionnaire', questionnaire_id=questionnaire.id))
    return render_template('admin/questionnaire/edit_questionnaire.html', questionnaire=questionnaire, form=form)


@bp.route('/add_question/<int:questionnaire_id>', methods=['GET', 'POST'])
@admin_login_required
def add_question(questionnaire_id):
    form = Questionnaire_QuestionForm(request.form)
    if request.method == 'POST':
        question = Questionnaire_QuestionModel(content=form.content.data,
                                               type=form.type.data,
                                               questionnaire_id=questionnaire_id,
                                               user_id=111)
        db.session.add(question)
        db.session.commit()
        if form.type.data == '1':  # 如果是选择题
            return redirect(url_for('admin_questionnaire.add_option', question_id=question.id))
        else:
            flash('问题添加成功', 'success')
            return redirect(url_for('admin_questionnaire.edit_questionnaire', questionnaire_id=questionnaire_id))
    return render_template('admin/questionnaire/add_question.html', form=form)


@bp.route('/edit_question/<int:question_id>', methods=['GET', 'POST'])
@admin_login_required
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
        return redirect(url_for('admin_questionnaire.edit_questionnaire', questionnaire_id=question.questionnaire_id))

    form.content.data = question.content
    form.type.data = question.type

    return render_template('admin/questionnaire/edit_question.html', question=question, form=form)


@bp.route('/delete_questionnaire/<int:questionnaire_id>', methods=['GET', 'POST'])
@admin_login_required
def delete_questionnaire(questionnaire_id):
    questionnaires = QuestionnaireModel.query.get(questionnaire_id)
    if questionnaires is None:
        flash('问卷不存在', 'error')
    else:
        try:
            # 删除该问卷下的所有答案
            for questionnaire in questionnaires:
                for quesiton in questionnaire.questions:
                    answer = Questionnaire_AnswerModel.query.filter_by(question_id=quesiton.id)
                    for answer in answer:
                        db.session.delete(answer)
                        print('删除成功')
                # 删除该问卷下的所有问题和选项
                for question in questionnaire.questions:
                    op = Questionnaire_OptionModel.query.filter_by(question_id=question.id)
                    for option in op:
                        db.session.delete(option)
                    db.session.delete(question)
                db.session.expunge(questionnaire)  # 从会话中分离出问卷对象

                # 删除该问卷
                db.session.delete(questionnaire)
                db.session.commit()
                flash('问卷删除成功', 'success')
        except Exception as e:
            db.session.rollback()
            flash('删除问卷失败', 'error')
            current_app.logger.error('删除问卷失败：%s' % str(e))

    return redirect(url_for('admin_questionnaire.index'))

@bp.route('/add_option/<int:question_id>', methods=['GET', 'POST'])
@admin_login_required
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
        return redirect(url_for('admin_questionnaire.edit_question', question_id=question_id))
    return render_template('admin/questionnaire/add_option.html', form=form, question=question)


@bp.route('/delete_question/<int:question_id>', methods=['POST', 'GET'])
def delete_question(question_id):
    question = Questionnaire_QuestionModel.query.get_or_404(question_id)

    db.session.delete(question)
    db.session.commit()

    flash('问题删除成功', 'success')
    return redirect(url_for('admin_questionnaire.edit_questionnaire', questionnaire_id=question.questionnaire_id))


@bp.route('/questionnaire/<int:questionnaire_id>/stats')
def questionnaire_stats(questionnaire_id):
    questionnaire = QuestionnaireModel.query.get(questionnaire_id)
    if not questionnaire:
        return 'Questionnaire not found'
    questions_answers = []
    for question in questionnaire.questions:
        answers = Questionnaire_AnswerModel.query.filter_by(question_id=question.id).all()
        answer_count = {}
        for answer in answers:
            if answer.option_id:
                option_content = Questionnaire_OptionModel.query.get(answer.option_id).content
            else:
                option_content = answer.content
            if option_content not in answer_count:
                answer_count[option_content] = 0
            answer_count[option_content] += 1
        questions_answers.append({'question': question.content, 'answers': answer_count})
    return render_template('admin/questionnaire/questionnaire_stats.html', questionnaire=questionnaire,
                           questions_answers=questions_answers)
