================
MDPress 博客系统
================

************
Introduction
************

MDPress 是基于 Flask 和 Redis 的博客系统，使用 Python 编程语言编写，不含 MySQL 或者 MongoDB 等"重"数据库。之所以会诞生 MDPress，是因为目前博客系统界中 Python 编写的博客系统都不符合我的要求，同时流行的 Wordpress 太多笨重，Ghost 又是使用 Nodejs 编写，而我的需求也简单，不外乎：

1. 博客的编辑系统足够方便简单，而且需要支持 Markdown 语法
2. 我有兴致的时候可以快速编辑一个小组件玩玩

经过几个月的断断续续业余时间折腾，出来的结果——MDPress 足够满足我的需求，它的编辑器基于 `Editor.md <https://pandao.github.io/editor.md/examples/index.html>`_
，同时又是使用 Flask 框架，整个代码架构松耦合，给扩展提供了无限的可能。 

========
源码地址
========

MDPress 源码地址： `Github <https://github.com/yetship/mdpress>`_


====
博客示例
====

你可以访问 `http://www.mdpress.me <http://www.mdpress.me>`_
进行效果尝试

============
MDPress 特性
============

1. 强大的分类结构支持
2. 智能的搜索系统
3. 可指定行数的代码和高亮
4. 方便得图片上传和云管理
5. 定制化的文章缓存

========
安装指南
========

1. 创建虚拟环境

执行以下命令::

    virtualenv mdpenv 
    source mdpenv/bin/activator

2. 安装依赖

执行以下命令::

    apt-get install python-lxml
    apt-get install libmysqlclient-dev
    apt-get install libffi-dev

    pip install urllib3 --upgrade

    pip install -r utils/requirements.txt


3. 配置 Redis

使用文本编辑器打开配置文件::

    vim config/development.py

确保你的 Redis 实例已经启动并且地址正确::

    REDIS_CONFIG = {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 10
    }

4. 运行服务器

是时候将服务器跑起来了::

    python manager runserver

确保没报错之后就打开浏览器访问以下网址::
 
    http://localhost:5000

你将会看到主页。

**Run Worker**

worker 需要单独运行::

    celery -A celery_worker.celery worker --loglevel=info

========
系统依赖
========

MDPress 依赖于以下环境::

    Python == 2.7
    Reids >= 3.0.0

========
关于作者
========

1. 作者博客：`Angiris Council <https://liuliqiang.info>`_
2. Github：`Yetship <https://github.com/yetship>`_



============
博客系统截图
============

**Index**

.. image:: http://ooo.0o0.ooo/2016/07/27/579978371acf9.jpg


**Archive**

.. image:: http://ooo.0o0.ooo/2016/07/27/5799783689c9f.jpg

**Admin Login**

.. image:: http://ooo.0o0.ooo/2016/07/27/5799783457de9.jpg
**Admin Main**

.. image:: http://ooo.0o0.ooo/2016/07/27/5799783ceb8a4.jpg
**Post List**

.. image:: http://ooo.0o0.ooo/2016/07/27/5799783a4fa9d.jpg
**Post Editing**

.. image:: http://ooo.0o0.ooo/2016/07/27/5799783c46069.jpg
**Tags List**

.. image:: http://ooo.0o0.ooo/2016/07/27/579978398a840.jpg



========
更新历史
========


- v0.1
	- 2015-02-18 14:38:03

	1. create project, and implement base feature

- v0.2
	- 2015-02-21 11:57:03

	1. add save and view post feature

- v0.3
	- 2016-06-04 13:03:31

	1. refactor whole project structure

- v0.4
	- 2016-7-28 22:34:36

	1. add redis models support
	2. add theme and jade template support

- v0.5
    - 2016-10-29 14:45:22
    
        1. change persistence to mysql
        2. add frontend cache support

- v1.0.0
    - 2016-10-31 22:47:33

        1. 发布 v1.0 版本
