from flask import Blueprint, render_template

from models import UserModel

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route("/<user_id>")
def index(user_id):
    user = UserModel.query.filter_by(id = user_id).first()
    return render_template('user/base.html',user=user)
