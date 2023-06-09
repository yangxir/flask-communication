from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify, abort
import os

from sqlalchemy.sql.functions import current_user

from decorators import login_required
from exts import db
from datetime import datetime
from models import VideoModel, Comment

bp = Blueprint('learn', __name__, url_prefix='/learn')


@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 5  # Set the number of questions per page
    offset = (page - 1) * per_page
    videos = VideoModel.query.limit(per_page).offset(offset).all()
    total_videos = VideoModel.query.count()
    pages = total_videos // per_page + (total_videos % per_page > 0)
    print(videos)
    return render_template('user/video/learn_AI.html', videos=videos ,total_videos=total_videos, per_page=per_page,
                           pages=pages, page=page)


@bp.route('/video_detail/<int:video_id>', methods=['GET', 'POST'])
@login_required
def video_detail(video_id):
    video = VideoModel.query.get(video_id)
    # 点击量+1
    video.count += 1
    # 保存更新后的视频对象到数据库
    db.session.add(video)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    per_page = 5  # Set the number of questions per page
    offset = (page - 1) * per_page
    comments_1 = Comment.query.filter_by(video_id=video_id).limit(per_page).offset(offset).all()
    total_comments = Comment.query.count()
    pages = total_comments // per_page + (total_comments % per_page > 0)

    return render_template('user/video/video_detail.html', video=video, comments=comments_1 ,
                           total_comments=total_comments, per_page=per_page,
                           pages=pages, page=page
                           )


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
    page = request.args.get('page', 1, type=int)
    per_page = 5  # Set the number of questions per page
    offset = (page - 1) * per_page
    comments_1 = Comment.query.filter_by(video_id=video_id).limit(per_page).offset(offset).all()
    total_comments = Comment.query.count()
    pages = total_comments // per_page + (total_comments % per_page > 0)
    video = VideoModel.query.get(video_id)

    return render_template('user/video/video_detail.html', video=video, comments=comments_1,
                           total_comments=total_comments, per_page=per_page,
                           pages=pages, page=page)

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
