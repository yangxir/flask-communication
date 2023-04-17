# flask-communication


## 环境依赖
- python3.7+
- MySQL


## 部署步骤
1. 修改 `config.py` 中的信息，包括邮箱、数据库等（需要先在 `admin` 表中添加账户 `admin` 密码 `admin`，在用户表中添加 `id` 为 `113`，用户名为 `admin`，密码随意，其他随意）。
2. 修改 `auth.py` 中函数 `edit_self` 中的 `avatar_path`、`thumbnail_path` 后面的绝对路径，改为自己的。
3. 修改 `blueprints` 中的 `/admin/admin_videos.py` 中的 `upload_video` 函数中 `file.save` 后面的绝对路径，改为自己的。
4. 修改 `blueprints` 中的 `/admin/admin_videos.py` 中的 `delete_video` 函数中 `os.remove` 后面的绝对路径，改为自己的。
5. 修改 `utils.py` 中的 `font` 后面的绝对路径，改为自己的。

6. 安装依赖（有依赖包没有加完全，需要自己查找）：
```
$ pip install -r requirements.txt

```
7. 数据库迁移。先删除 migrations 文件夹，然后运行以下三个指令：
 ```
  $flask db init
  $flask db migrate
  $flask db upgrade
  ```

## 目录结构描述
├ Readme.md                  // 帮助文档
├ app.py                     // Flask 初始化文件
├ config.py                  // 配置文件
├ decorators.py              // 装饰器（登陆检测）
├ dirtree.txt                // 目录树
├ exts.py                    // 工具类初始化
├ models.py                  // 数据库模型
├ requirements.txt           // 列出了所有依赖包以及版本号，方便在其他位置生成相同的虚拟环境以及依赖
├ utils.py                   // 工具函数
├─blueprints                 // 蓝图（视图）
│ ├─admin                    // 管理员蓝图
│ ├─competition              // 竞赛蓝图
│ ├─forms                    // 表单蓝图
│ ├─learn                    // 学习视频蓝图
│ ├─qa                       // 问题蓝图
│ ├─questionnaire            // 问卷蓝图
│ └─user                     // 用户蓝图（已不使用）
├─migrations                // 数据库迁移文件夹     
├─static                    // CSS、JS、图片等静态文件
└─templates                 // Jinja2 模板文件夹


## 版本更新
# v1.0.0
1. 新增功能：个人中心可以进入，编辑、查看自己的评论、问题、问卷。
2. 新增功能：管理员可以查看问卷回答情况。
3. 新增功能：视频开放评论区。