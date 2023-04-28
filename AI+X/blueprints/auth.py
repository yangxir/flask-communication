import os

from falcon import secure_filename
from flask import Blueprint, render_template, jsonify, redirect, url_for, session, current_app, flash

from decorators import login_required
from exts import mail, db
from flask_mail import Message
from flask import request
import random
from models import EmailCaptchaModel, UserModel, QuestionModel, AnswerModel, Comment, QuestionnaireModel, \
    Questionnaire_QuestionModel, Questionnaire_AnswerModel, Questionnaire_OptionModel
from utils import allowed_file, save_avatar_thumbnail, get_avatar_path
from .forms import RegisterForm, LoginForm, AvatarUploadForm, EditProfileForm
from werkzeug.security import generate_password_hash, check_password_hash

# /auth
bp = Blueprint('auth', __name__, url_prefix='/auth')
avatar_dir = get_avatar_path()


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        form = LoginForm(request.form)
        if form.validate():
            return redirect('/')
        else:
            print(form.errors)
            return redirect(url_for('auth.login'))


# GET: 从服务器获取数据
# POST:将客户端数据提交给服务器
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        # 验证用户提交的邮箱和邮箱验证码是否一致
        # 表单验证: flask-wtf: wtforms
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email, username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            print(form.errors)
            return redirect(url_for('auth.register'))


# 没有指定方法，默认GET
@bp.route('/captcha/email', methods=['GET'])
def get_email_captcha():
    email = request.args.get('email')
    # 随机数字组合
    captcha = random.randint(1000, 9999)
    message = Message(subject='注册验证码', recipients=[email], body=f'您的验证码是{captcha}')
    mail.send(message)
    # memcached 存储在内存里，断电就无了
    # redis 数据类型更强大，同步机制（硬盘）
    # 这里用数据库存储，开销大
    email_already_in = EmailCaptchaModel.query.filter_by(email=email)
    # 如果之前发送过验证码，那么覆盖掉过去的，保留最新的
    if email_already_in.first():
        email_already_in.first().captcha = captcha
    # 之前没有发送过，直接加入数据库
    else:
        email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
        db.session.add(email_captcha)
    db.session.commit()
    return jsonify({'code': 200, 'message': '', 'data': None})


@bp.route("/start")
def start():
    return render_template("start.html")


@bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@bp.route('/user_self/<int:user_id>', methods=['GET', 'POST'])
@login_required
def user_self(user_id):
    user = UserModel.query.filter_by(id=user_id).first_or_404()
    return render_template('user/self/index.html', user=user)


@bp.route('/user_self/<int:user_id>/questions', methods=['GET'])
@login_required
def user_questions(user_id):
    user = UserModel.query.filter_by(id=user_id).first_or_404()
    questions = QuestionModel.query.filter_by(author_id=user_id).order_by(QuestionModel.create_time.desc()).all()
    return render_template('user/self/questions.html', user=user, questions=questions)


@bp.route('/user_self/<int:user_id>/answers', methods=['GET'])
@login_required
def user_answers(user_id):
    user = UserModel.query.filter_by(id=user_id).first_or_404()
    answers = AnswerModel.query.filter_by(author_id=user_id).order_by(AnswerModel.create_time.desc()).all()
    return render_template('user/self/answers.html', user=user, answers=answers)


@bp.route('/user_self/<int:user_id>/comments', methods=['GET'])
@login_required
def user_comments(user_id):
    user = UserModel.query.filter_by(id=user_id).first_or_404()
    comments = Comment.query.filter_by(user_id=user_id).order_by(Comment.create_time.desc()).all()
    return render_template('user/self/comments.html', user=user, comments=comments)


# 用户制作的问卷
@bp.route('/user_self/<int:user_id>/questionnaires', methods=['GET'])
@login_required
def user_questionnaires(user_id):
    user = UserModel.query.filter_by(id=user_id).first_or_404()
    questionnaires = QuestionnaireModel.query.filter_by(user_id=user_id).order_by(
        QuestionnaireModel.created_at.desc()).all()
    return render_template('user/self/questionnaires.html', user=user, questionnaires=questionnaires)




@bp.route('/edit_self/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_self(user_id):
    user = UserModel.query.filter_by(id=user_id).first_or_404()
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        avatar = request.files.get('avatar')
        if avatar:
            avatar_filename = secure_filename(avatar.filename)
            avatar.save(os.path.join(avatar_dir, avatar_filename))  # 将任意位置图片保存到项目位置
            avatar_path = os.path.join(avatar_dir,
                                       avatar_filename)

            thumbnail_path = os.path.join(avatar_dir, 'thumbnails',
                                          avatar_filename)
            save_avatar_thumbnail(avatar_path, thumbnail_path)
            user.avatar = avatar_filename
        if password:
            user.set_password(password)
        if username:
            user.username = username
        if email:
            user.email = email
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('auth.user_self', user_id=user_id))
    return render_template('user/self/edit.html', title='修改个人信息', user=user)
