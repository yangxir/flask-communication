import base64
import io
from datetime import datetime
from io import BytesIO

import matplotlib
from flask import Blueprint, render_template, request, g, redirect, url_for, flash
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties
from matplotlib_inline.backend_inline import FigureCanvas

from blueprints.forms import QuestionForm, AnswerForm
from exts import db
from decorators import  admin_login_required
from models import  UserModel, Comment,VideoModel

# /auth
from utils import get_comments_statistics, generate_word_cloud

bp = Blueprint('admin_comments', __name__, url_prefix='/admin_comments')
matplotlib.use('Agg')
matplotlib.rcParams['font.family'] = 'AaMakeTi-2'
# http://127.0.0.1:5000
# /admin_comments


@bp.route('/')
@admin_login_required
def index():
    comments = Comment.query.all()
    return render_template('admin/comments/index.html', comments=comments)

@bp.route('/delete_comment/<int:comment_id>', methods=['POST'])
@admin_login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash('评论删除成功', 'success')
    return redirect(url_for('admin_comments.index'))

@bp.route('/word_cloud')
@admin_login_required
def word_cloud():
    # 调用 generate_word_cloud() 函数生成词云图片并返回图片的路径
    image_path = generate_word_cloud()
    return render_template('admin/comments/word_cloud.html', image_path=image_path)


@bp.route('/statistics')
@admin_login_required
def statistics():
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['AaMakeTi-2']
    font = FontProperties(fname='E:/A-10-Temporary_test/last_test/flask-qa-main/AI+X/static/AaMaKeTi-2.ttf', size=14)

    # 获取评论统计数据
    total_count, comment_count, reply_count, top_words = get_comments_statistics()

    # 将数据处理为饼图所需的格式
    labels = list(top_words.keys())
    data = list(top_words.values())

    # 生成饼图
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90, textprops={'fontproperties': font})
    ax.axis('equal')
    plt.title('top 10 words', fontsize=20)

    # 将饼图转化为字节流并编码为base64
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image = base64.b64encode(buf.getvalue()).decode('ascii')

    # 将编码后的图像嵌入到HTML中的<img>标签中
    html = '<img src="data:image/png;base64,{}" width="100%">'.format(image)

    return render_template('admin/comments/statistics.html', html=html, total_count=total_count,
                           reply_count=reply_count)