# AI+X Communication Platform

## Introduction
- This is just a web system developed based on flask.
- Designed by yangxir.
- Based on the basic knowledge learned from the qa project of Zhiliao Chuanke, expand the development.
- Original Unexpanded Project Go to https://github.com/yangxir/-qa-

## Environment Dependencies
- python3.7+
- MySQL
- FLask

## Deployment Steps
1. Modify the information in `config.py`, including mailbox, database, etc.

2. Install dependencies (some dependency packages are not added completely, you need to find them yourself):
```
$ pip install -r requirements.txt
```
3. Database migration. First delete the migrations folder, then enter the project file and run the following three commands:
```
$flask db init
$flask db migrate
$flask db upgrade
```
4. (You need to add the account `admin` password `admin` in the `admin` table first).
5. (You need to add id`113` username `admin` and password to `usermodel` table, others are optional)
## Directory structure description
├ Readme.md // Help document

├ app.py // Flask initialization file

├ config.py // Configuration file

├ decorators.py // Decorator (login detection)

├ dirtree.txt // Directory tree

├ exts.py // Tool class initialization

├ models.py // Database model

├ requirements.txt // Lists all dependent packages and version numbers to facilitate generating the same virtual environment and dependencies in other locations

├ utils.py // Tool function

├─blueprints // Blueprint (view)

│ ├─admin // Administrator blueprint

│ ├─competition // Competition blueprint

│ ├─forms // Form blueprint

│ ├─learn // Learning video blueprint

│ ├─qa // Question blueprint

│ ├─questionnaire // Questionnaire blueprint

│ └─user // User blueprint (no longer used)

├─migrations // Database migration folder

├─static // CSS, JS, pictures and other static files

└─templates // Jinja2 template folder

## Version update
# v1.0.1
1. New feature: You can enter the personal center to edit and view your own comments, questions, and questionnaires.
2. New feature: Administrators can view the answers to the questionnaire.
3. New feature: Video open comment area.
4. Pagination query function.

## Version update
# v1.0.1
1. Fix the pagination query code bug. Some python versions cannot use .pagination
2. Fix the problem that the search question page does not use the pagination query function.
3. New features: Add web icon AI, favicon.ico.
4. Modify the URL navigation bar title.

## Version update
# v1.0.2
1. The video name becomes unique
2. Fixed the problem that deleting a questionnaire cannot delete the questions, options, and answers in the questionnaire.
3. Fixed the problem that deleting a video cannot delete the comments of the video.
4. Fixed the problem that deleting a user cannot delete the questions, answers, and questionnaires posted by the user.
5. Fixed the problem that deleting a question cannot delete the answer to the question.

## 截图
![主页.png](https://s2.loli.net/2023/04/17/Su9IvAVnzJeUabr.png)

![个人主页.png](https://s2.loli.net/2023/04/17/6oquDryjEApbKRC.png)

![调查问卷页面.png](https://s2.loli.net/2023/04/17/hNSgDHWiavkuBZ9.png)

![管理员界面.png](https://s2.loli.net/2023/04/17/pCHmIcoF5hq1l9U.png)

![学习视频页面.png](https://s2.loli.net/2023/04/17/yuYXIB8nOjhPWHR.png)

![用户管理.png](https://s2.loli.net/2023/04/17/ZkYNp37eb9gsWHK.png)

![视频界面.png](https://s2.loli.net/2023/04/17/LWAj9KdMxaRu4Jw.png)

![视频评论界面.png](https://s2.loli.net/2023/04/17/dH1VlweFvEbG98f.png)

# 中文
# AI+X交流平台

## 介绍
- 这只是一款基于flask开发的网页系统。
- yangxir设计。
- 基于知了传课的qa项目学习的基础知识，进行扩展开发。
- 原 未扩展项目 转到 https://github.com/yangxir/-qa-

## 环境依赖
- python3.7+
- MySQL
- FLask

## 部署步骤
1. 修改 `config.py` 中的信息，包括邮箱、数据库等

2. 安装依赖（有依赖包没有加完全，需要自己查找）：
```
$ pip install -r requirements.txt
```
3. 数据库迁移。先删除 migrations 文件夹，然后进入项目文件运行以下三个指令：
 ```
  $flask db init
  $flask db migrate
  $flask db upgrade
  ```
4. （需要先在 `admin` 表中添加账户 `admin` 密码 `admin`）。
5. (需要在`usermodel`表中添加 id`113` username `admin`密码随意，其他随意)
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
# v1.0.1
1. 新增功能：个人中心可以进入，编辑、查看自己的评论、问题、问卷。
2. 新增功能：管理员可以查看问卷回答情况。
3. 新增功能：视频开放评论区。
4. 分页查询功能。

## 版本更新
# v1.0.1
1. 修复分页查询代码bug，一些python版本中无法使用.pagination
2. 修复搜搜问题页面没有使用分页查询功能。
3. 新增功能：增加网页图标AI,favicon.ico。
4. 修改网址导航栏标题。 

## 版本更新
# v1.0.2
1. 视频名称变为唯一
2. 修复删除调查问卷不能删除问卷中的问题、选项、回答。
3. 修复删除视频不能删除视频的评论。
4. 修复删除用户不能删除用户发布的问题、回答、调查问卷。
5. 修复删除问题不能删除问题的回答。
