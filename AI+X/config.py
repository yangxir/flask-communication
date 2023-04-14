SECRET_KEY = 'adsdadadas'

# 数据库配置
HOSTNAME = '127.0.0.1'
PORT = 3306
USERNAME = 'root'
PASSWORD = '1234'
DATABASE = 'flask_db2'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 邮箱配置
MAIL_SERVER = 'smtp.qq.com'
MAIL_PROT = 465
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = "935488599@qq.com"
MAIL_PASSWORD = "ixggichnrfujbecb"
MAIL_DEFAULT_SENDER = "935488599@qq.com"
# ixggichnrfujbecb


ALLOWED_EXTENSIONS = {'mp4'}
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB
UPLOAD_FOLDER = '/static/movie'
