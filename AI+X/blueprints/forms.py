import wtforms
from flask import session
from werkzeug.security import check_password_hash
from wtforms.validators import DataRequired, Length
from wtforms.validators import Email, EqualTo, InputRequired

from exts import db
from models import UserModel, EmailCaptchaModel, AdminModel


class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message='邮箱格式错误!')])
    captcha = wtforms.StringField(validators=[Length(min=4, max=4, message='验证码格式错误！')])
    username = wtforms.StringField(validators=[Length(min=3, max=20, message='用户名格式错误！')])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message='密码格式错误！')])
    password_confirm = wtforms.StringField(validators=[EqualTo('password')])

    # 自定义验证
    # 1. 邮箱是否被注册
    # 2. 验证码是否正确
    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message='该邮箱已经被注册！')

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).first()
        if not captcha_model:
            raise wtforms.ValidationError(message='邮箱或验证码错误！')
        # 删除验证码
        else:
            db.session.delete(captcha_model)
            db.session.commit()


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message='邮箱格式错误!')])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message='密码格式错误！')])

    # 自定义验证
    # 邮箱是否注册
    def validate_email(self, field):
        email = field.data
        password = self.password.data
        user = UserModel.query.filter_by(email=email).first()
        # 没有此用户
        if not user:
            raise wtforms.ValidationError(message='该邮箱未注册！')
        else:
            # 账号密码正确
            if check_password_hash(user.password, password):
                # cookie:
                # 使用cookie存储登录授权
                # flask中的session经过加密存储在cookie中
                session['user_id'] = user.id
            # 账号密码错误
            else:
                raise wtforms.ValidationError(message='账号密码错误！')


class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[Length(min=3, max=100, message='问题标题格式错误!')])
    content = wtforms.StringField(validators=[Length(min=3, message='问题描述格式错误！')])


class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[Length(min=1, message='回答最短需要1个字！')])
    question_id = wtforms.IntegerField(validators=[InputRequired(message='必须传入问题Id！')])


class AdminLoginForm(wtforms.Form):
    admin = wtforms.StringField(validators=[Length(min=3, max=20, message='用户名格式错误！')])
    password = wtforms.StringField(validators=[Length(min=3, max=10, message='密码格式错误！')])

    def validate_admin(self, field):
        admin = field.data
        password = self.password.data
        admin_test = AdminModel.query.filter_by(admin_name=admin).first()

        # 没有此用户
        if not admin_test:
            raise wtforms.ValidationError(message='还不是管理员，请从后台添加')
        else:
            # 账号密码正确
            if admin_test.password == password:
                # cookie:
                # 使用cookie存储登录授权
                # flask中的session经过加密存储在cookie中
                session['admin_id'] = admin_test.id
            # 账号密码错误
            else:
                raise wtforms.ValidationError(message='账号密码错误！')


class Admin_AddUser(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message='邮箱格式错误!')])
    username = wtforms.StringField(validators=[Length(min=3, max=20, message='用户名格式错误！')])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message='密码格式错误！')])

    def validate_new_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message='该邮箱已经被注册！,请管理员重新选择邮箱')


class AddCompetitionForm(wtforms.Form):
    name = wtforms.StringField('竞赛名称')
    start_time = wtforms.DateTimeField('开始时间', format="%Y-%m-%d %H:%M:%S", validators=[DataRequired()],
                                       render_kw={"placeholder": "选择时间"})
    end_time = wtforms.DateTimeField('结束时间', format="%Y-%m-%d %H:%M:%S", validators=[DataRequired()],
                                     render_kw={"placeholder": "选择时间"})
    type = wtforms.SelectField('类型',
                               choices=[('算法竞赛', '算法竞赛'), ('数据竞赛', '数据竞赛'), ('智能交通竞赛', '智能交通竞赛'), ('机器人竞赛', '机器人竞赛'),
                                        ('计算机视觉竞赛', '计算机视觉竞赛')])
    level = wtforms.SelectField('级别', choices=[('国家级', '国家级'), ('省级', '省级'), ('市级', '市级'), ('国际级', '国际级')])


class EditCompetitionForm(wtforms.Form):
    name = wtforms.StringField('Name', validators=[DataRequired()])
    start_time = wtforms.DateTimeField('Start Time', validators=[DataRequired()], format='%Y-%m-%d %H:%M:%S')
    end_time = wtforms.DateTimeField('End Time', validators=[DataRequired()], format='%Y-%m-%d %H:%M:%S')
    type = wtforms.StringField('Type', validators=[DataRequired()])
    level = wtforms.StringField('Level', validators=[DataRequired()])


class EditUserForm(wtforms.Form):
    username = wtforms.StringField('用户名', validators=[DataRequired(), Length(min=3, max=20)])
    email = wtforms.StringField('邮箱', validators=[DataRequired(), Email()])
    submit = wtforms.SubmitField('保存')


class Search_User(wtforms.Form):
    keyword = wtforms.StringField(validators=[DataRequired(message='关键字不能为空')])


class EditAnswerForm(wtforms.Form):
    question_id = wtforms.IntegerField('问题ID', validators=[DataRequired()])
    content = wtforms.StringField('评论内容', validators=[DataRequired()])
    submit = wtforms.SubmitField('保存')


class AddVideoForm(wtforms.Form):
    video_name = wtforms.StringField('视频名称', validators=[DataRequired(message="视频名称不能为空"),
                                                         Length(min=1, max=50, message="视频名称长度在1-50字符之间")])
    video_file = wtforms.FileField('上传视频文件', validators=[DataRequired(message="请选择要上传的视频文件")])
    submit = wtforms.SubmitField('添加')


class QuestionnaireForm(wtforms.Form):
    title = wtforms.StringField('标题',
                                validators=[DataRequired(message='标题不能为空'), Length(max=255, message='标题不能超过255个字符')])
    description = wtforms.TextAreaField('描述', validators=[DataRequired(message='描述不能为空')])


class OptionForm(wtforms.Form):
    content = wtforms.StringField('选项内容', validators=[DataRequired()])


class Questionnaire_QuestionForm(wtforms.Form):
    content = wtforms.StringField('问题内容', validators=[DataRequired()])
    type = wtforms.SelectField('问题类型', choices=[(str(i), t) for i, t in enumerate(['问答题', '单选题'])], coerce=int)
    options = wtforms.FieldList(wtforms.FormField(OptionForm), min_entries=4, max_entries=4)


class Answer_QuestionnaireForm(wtforms.Form):
    def __init__(self, questions=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if questions:
            for question in questions:
                # 如果是单选题，动态生成选项
                if question.type == 1:
                    choices = [(str(option.id), option.content)
                               for option in question.options]
                    field = wtforms.RadioField(
                        label=question.content,
                        choices=choices,
                        validators=[InputRequired()],
                    )
                # 其他题目类型，生成文本框
                else:
                    field = wtforms.StringField(
                        label=question.content,
                        validators=[InputRequired()],
                    )
                self[str(question.id)] = field
