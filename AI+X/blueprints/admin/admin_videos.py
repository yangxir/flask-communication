import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename

from decorators import admin_login_required
from models import VideoModel
from exts import db
from  utils import get_static_path
bp = Blueprint('admin_videos', __name__, url_prefix='/admin_videos')
static_dir = get_static_path()
# 允许上传的视频文件类型
ALLOWED_EXTENSIONS = {'mp4'}


# 检查上传的文件是否为允许的类型
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# 视频列表
@bp.route('/')
@admin_login_required
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Set the number of questions per page
    videos = VideoModel.query.paginate(page=page, per_page=per_page)
    return render_template('admin/video/admin_video.html', videos=videos)


# 添加视频
@bp.route('/upload', methods=['GET', 'POST'])
@admin_login_required
def upload_video():
    print(request.method)
    if request.method == 'POST':
        # 检查文件是否上传
        print(request.files)
        if 'video' not in request.files:
            flash('未选择文件', 'error')
            return redirect(request.url)
        file = request.files['video']

        # 检查文件名是否合法
        print("file.filename=", file.filename)
        if file.filename == '':
            flash('文件名不能为空', 'error')
            return redirect(request.url)
        if not allowed_file(file.filename):
            flash('不支持的文件类型', 'error')
            return redirect(request.url)
        # 保存文件
        filename = file.filename
        print(filename)

        file.save(os.path.join(static_dir, filename))
        # 添加视频到数据库
        title = request.form.get('title')
        count = request.form.get('count', 0, type=int)
        video = VideoModel(title=title, file=filename, count=count)
        db.session.add(video)
        db.session.commit()
        flash('添加视频成功', 'success')
        return redirect(url_for('admin_videos.index'))
    return render_template('admin/video/admin_videos_add.html')


# 删除视频
@bp.route('/delete/<int:video_id>', methods=['GET', 'POST'])
def delete_video(video_id):
    video = VideoModel.query.get_or_404(video_id)
    if request.method == 'POST':
        # 删除文件
        os.remove(os.path.join(static_dir, video.file))
        # 删除视频记录
        db.session.delete(video)
        db.session.commit()
        flash('删除成功', 'success')
        return redirect(url_for('admin_videos.index'))
    return render_template('admin/video/admin_videos_delete.html', video=video)
