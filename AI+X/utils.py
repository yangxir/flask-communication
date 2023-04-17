import os

import jieba
from collections import Counter

from PIL import Image
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
from wordcloud import WordCloud

from models import Comment

# 设置中文字体
font = FontProperties(fname='E:/A-10-Temporary_test/last_test/flask-qa-main/AI+X/static/AaMaKeTi-2.ttf')


def generate_word_cloud():
    comments = Comment.query.all()

    # 将评论内容取出，并用空格分隔成一个个单词
    words = []
    for comment in comments:
        words.extend(jieba.cut(comment.content))

    # 统计每个单词的出现次数
    counter = Counter(words)

    # 使用WordCloud生成词云
    wc = WordCloud(font_path='msyh.ttc', width=800, height=600, background_color='white')
    wc.generate_from_frequencies(counter)

    # 保存词云图片到静态文件夹
    image_path = os.path.join(os.path.dirname(__file__), 'static', 'images', 'word_cloud.png')

    wc.to_file(image_path)

    return image_path


def get_comments_statistics():
    comments = Comment.query.all()

    # 将评论内容取出，并用空格分隔成一个个单词
    words = []
    for comment in comments:
        words.extend(jieba.cut(comment.content))

    # 统计每个单词的出现次数
    counter = Counter(words)

    # 计算每个单词出现的百分比
    total_count = sum(counter.values())
    comment_count = len(comments)
    reply_count = sum(comment.replies.count() for comment in comments)
    top_words = dict(counter.most_common(10))

    return total_count, comment_count, reply_count, top_words


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # allowed avatar file extensions

    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_avatar_thumbnail(avatar_filename, thumbnail_filename, size=(100, 100)):

    with Image.open(avatar_filename) as img:
        img = img.convert('RGB')  # 将图片转换为 RGB 模式
        img.thumbnail(size)
        img.save(thumbnail_filename)
