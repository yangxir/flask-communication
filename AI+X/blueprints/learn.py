from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify, abort
import os

from sqlalchemy.sql.functions import current_user

from decorators import login_required
from exts import db
from datetime import datetime
from models import VideoModel, Comment, ReplyComment

bp = Blueprint('learn', __name__, url_prefix='/learn')


@bp.route('/')
def index():
    videos = VideoModel.query.all()
    print(videos)
    return render_template('user/video/learn_AI.html', videos=videos)


@bp.route('/video_detail/<int:video_id>', methods=['GET', 'POST'])
@login_required
def video_detail(video_id):
    video = VideoModel.query.get(video_id)
    # 点击量+1
    video.count += 1
    # 保存更新后的视频对象到数据库
    db.session.add(video)
    db.session.commit()

    comments_1 = Comment.query.filter_by(video_id=video_id).all()
    return render_template('user/video/video_detail.html', video=video, comments=comments_1)


@bp.route('/<int:video_id>/comments', methods=['GET', 'POST'])
@login_required
def comments(video_id):
    if request.method == 'POST':
        # 处理用户提交的评论
        user_id = session.get('user_id')
        content = request.form.get('content')

        comment = Comment(user_id=user_id, content=content, video_id=video_id, create_time=datetime.now())
        db.session.add(comment)
        db.session.commit()

    video = VideoModel.query.get(video_id)
    comments_1 = Comment.query.filter_by(video_id=video_id).all()
    return render_template('user/video/video_detail.html', video=video, comments=comments_1)

@bp.route('/comments/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.user.id != session.get('user_id'):
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    flash('评论已删除。', 'success')
    return redirect(url_for('learn.video_detail', video_id=comment.video_id))
