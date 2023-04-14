import base64

from flask import Flask, session, g, jsonify, request

import config
import requests
from exts import db, mail
from models import UserModel, AdminModel
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp
from blueprints.learn import bp as learn_bp
from blueprints.questionnaire import bp as questionnaire_bp
from blueprints.competition import bp as competition_bp
from blueprints.user import bp as user_bp
from blueprints.admin.admin import bp as admin_bp
from blueprints.admin.admin_user import bp as admin_user_bp
from blueprints.admin.admin_question import bp as admin_question_bp
from blueprints.admin.admin_questionnaire import bp as admin_questionnaire_bp
from blueprints.admin.admin_competition import bp as admin_competition_bp
from blueprints.admin.admin_videos import bp as admin_video_bp
from blueprints.admin.admin_answers import bp as admin_answer_bp_1
from blueprints.admin.admin_comments import bp as admin_comments_bp
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap4
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config.from_object(config)

db.init_app(app)
mail.init_app(app)
# admin.init_app(app)
bootstrap = Bootstrap4(app)
app.jinja_env.filters['b64encode'] = base64.b64encode
migrate = Migrate(app, db)

app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(learn_bp)
app.register_blueprint(questionnaire_bp)
app.register_blueprint(competition_bp)
app.register_blueprint(user_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(admin_user_bp)
app.register_blueprint(admin_question_bp)
app.register_blueprint(admin_questionnaire_bp)
app.register_blueprint(admin_competition_bp)
app.register_blueprint(admin_video_bp)
app.register_blueprint(admin_answer_bp_1)
app.register_blueprint(admin_comments_bp)


@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = UserModel.query.get(user_id)
        setattr(g, 'user', user)
    else:
        setattr(g, 'user', None)


@app.before_request
def admin_before_request():
    admin_id = session.get('admin_id')
    if admin_id:
        admin = AdminModel.query.get(admin_id)
        setattr(g, 'admin', admin)
    else:
        setattr(g, 'admin', None)


@app.context_processor
def my_context_processor():
    return {'user': g.user}


@app.context_processor
def admin_context_processor():
    return {'admin': g.admin}


if __name__ == '__main__':
    app.run()
