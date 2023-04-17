from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text

from exts import db
from datetime import datetime


class UserModel(db.Model):
    __tablename__ = "user_model"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)
    avatar = db.Column(db.String(200))  # new column for user avatar

    def __repr__(self):
        return self.username

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class AdminModel(db.Model):
    __tablename__ = 'admin_model'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    join_time = db.Column(db.DateTime, default=datetime.now)


class EmailCaptchaModel(db.Model):
    __tablename__ = 'email_captcha'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    captcha = db.Column(db.String(100), nullable=False)


class QuestionModel(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    # 外键
    author_id = db.Column(db.Integer, db.ForeignKey("user_model.id"))
    author = db.relationship(UserModel, backref="questions")


class AnswerModel(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    author_id = db.Column(db.Integer, db.ForeignKey("user_model.id"))

    question = db.relationship(QuestionModel, backref=db.backref('answers', order_by=create_time.desc()))
    author = db.relationship(UserModel, backref="answers")


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))
    user = db.relationship('UserModel')
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))
    replies = db.relationship('ReplyComment', backref='comment', lazy='dynamic')

    def __repr__(self):
        return self.content


class ReplyComment(db.Model):
    __tablename__ = 'reply_comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))
    user = db.relationship('UserModel')
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    reply_to_id = db.Column(db.Integer, db.ForeignKey('reply_comment.id'))
    replies = db.relationship('ReplyComment', backref=db.backref('parent_reply', remote_side=[id]), lazy='dynamic')

    def __repr__(self):
        return self.content


class VideoModel(db.Model):
    __tablename__ = 'video'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file = db.Column(db.String(255))
    title = db.Column(db.String(255))
    count = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    comments = db.relationship('Comment', backref='video', lazy=True)


class CompetitionModel(db.Model):
    __tablename__ = 'competition'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comp_name = db.Column(db.Text, nullable=True)
    start_time = db.Column(db.DateTime, default=datetime.now)
    end_time = db.Column(db.DateTime, default=datetime.now)
    comp_type = db.Column(db.Text, nullable=True)
    comp_level = db.Column(db.Text, nullable=True)


class QuestionnaireModel(db.Model):
    __tablename__ = 'questionnaire'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))
    user = db.relationship('UserModel')
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)
    questions = db.relationship('Questionnaire_QuestionModel', backref='questionnaire', lazy=True, cascade='delete')


class Questionnaire_QuestionModel(db.Model):
    __tablename__ = 'questionnaire_question'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    type = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)
    questionnaire_id = db.Column(db.Integer, db.ForeignKey('questionnaire.id'), nullable=False)
    options = db.relationship('Questionnaire_OptionModel', backref='questionnaire_question', lazy=True,
                              cascade='delete')


class Questionnaire_OptionModel(db.Model):
    __tablename__ = 'questionnaire_option'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questionnaire_question.id'), nullable=False)


class Questionnaire_AnswerModel(db.Model):
    __tablename__ = 'questionnaire_answer'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questionnaire_question.id'), nullable=False)
    option_id = db.Column(db.Integer, db.ForeignKey('questionnaire_option.id', ondelete='SET NULL'))
    content = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'), nullable=False)
