from flask import Blueprint, render_template, jsonify, redirect, url_for, session

from flask import request
from blueprints.forms import RegisterForm, LoginForm, AdminLoginForm

# /admin
from decorators import admin_login_required

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('admin/admin_login.html')
    else:
        form = AdminLoginForm(request.form)
        if form.validate():
            print("success")
            return redirect(url_for('admin.index'))
        else:
            print("fail")
            print(form.errors)
            return redirect(url_for('admin.login'))


@bp.route("/index")
@admin_login_required
def index():
    return render_template('admin/admin_index.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')
