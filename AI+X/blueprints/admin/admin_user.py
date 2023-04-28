from flask import Blueprint, render_template, jsonify, redirect, url_for, session, flash
from flask import request
from werkzeug.security import generate_password_hash

from decorators import admin_login_required
from exts import db
from models import UserModel, AnswerModel, QuestionModel, QuestionnaireModel, Questionnaire_AnswerModel, \
    Questionnaire_OptionModel, Questionnaire_QuestionModel
from blueprints.forms import Admin_AddUser, Search_User, EditUserForm

# /admin
bp = Blueprint('admin_user', __name__, url_prefix='/admin_user')


@bp.route("/index")
@admin_login_required
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 5  # Set the number of questions per page
    offset = (page - 1) * per_page
    users = UserModel.query.limit(per_page).offset(offset).all()
    total_users = UserModel.query.count()
    pages = total_users // per_page + (total_users % per_page > 0)
    return render_template('admin/user/admin_user.html', users=users,
                           total_users=total_users, per_page=per_page,
                           pages=pages, page=page
                           )


@bp.route('useradd/', methods=['GET', 'POST'])
@admin_login_required
def add_user():
    if request.method == 'GET':
        return render_template('admin/user/admin_adduser.html')
    else:

        form = Admin_AddUser(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email, username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('admin_user.index', add_message=['success']))
        else:
            print(form.errors)
            return render_template('admin/user/admin_adduser.html', add_message=['false'])


@bp.route('/search', methods=['GET', 'POST'])
def search():
    form = Search_User(request.form)
    if form.validate():
        keyword = form.keyword.data
        users = UserModel.query.filter(UserModel.username.like(f'%{keyword}%') |
                                       UserModel.email.like(f'%{keyword}%') |
                                       UserModel.id.like(f'%{keyword}%')).all()
        return render_template('admin/user/search_user.html', form=form, users=users)
    return render_template('admin/user/search_user.html', form=form)


class DeleteUserForm:
    pass


@bp.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])
def delete_user(user_id):
    user = UserModel.query.filter_by(id=user_id).first_or_404()
    form = DeleteUserForm()
    if request.method == 'POST':
        AnswerModel.query.filter_by(author_id=user.id).delete()
        QuestionModel.query.filter_by(author_id=user.id).delete()
        Questionnaire_AnswerModel.query.filter_by(user_id=user.id).delete()

        # 删除与该用户相关联的所有问卷及其问题和选项
        questionnaires = QuestionnaireModel.query.filter_by(user_id=user.id).all()
        for questionnaire in questionnaires:
            # 删除与该问卷相关联的所有问题及其选项
            Questionnaire_QuestionModel.query.filter_by(questionnaire_id=questionnaire.id).delete()
            db.session.delete(questionnaire)
        db.session.commit()

        db.session.delete(user)
        db.session.commit()
        flash('The user has been deleted successfully.', 'success')
        return redirect(url_for('admin_user.index'))
    return render_template('admin/user/delete_user.html', user=user, form=form)


@bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = UserModel.query.filter_by(id=user_id).first_or_404()
    form = EditUserForm(request.form, obj=user)
    if request.method == 'POST':
        if form.validate():
            form.populate_obj(user)
            db.session.commit()
            flash('The user has been updated successfully.', 'success')
            return redirect(url_for('admin_user.index'))
    return render_template('admin/user/edit_user.html', user=user, form=form)
