from functools import wraps
from flask import g, redirect, url_for


def login_required(func):
    # 保留func信息
    @wraps(func)
    def inner(*args, **kwargs):
        if g.user:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('auth.login'))

    return inner


def admin_login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if g.admin:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('admin.login'))
    return inner
