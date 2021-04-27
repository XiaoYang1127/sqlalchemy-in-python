# sqlalchemy-in-python

## 1. 背景

- SQLAlchemy 是一个 Python 的 SQL 工具包以及数据库对象映射框架
- 包含整套企业级持久化模式，专门为高效和高性能的数据库访问

## 2. 特点

- 增加，删除，修改采用 ORM 方式进行
- 查询，insert from select, insert on duplicate key 等采用 sql expression 或 raw sql 实现

## 3. 环境安装

- 安装 python3.7.5
- 安装依赖
  - cd sqlalchemy-in-python
  - python3 -m venv venv
  - source venv/bin/activate
  - pip3 install -r requirements.txt

## 4. 运行配置

- 执行 z_sql/db.sql 语句，重建数据库与数据表
- 修改[代码](./script/db/orm_db.py) 里面的 `passwd = "your password"`，该你的 mysql 密码
- 修改[代码](./script/db/redis_db.py) 里面的 `password="your password"`，为你的 redis 密码
- 运行主进程
  - cd script
  - python main.py main
- 运行用例测试
  - cd script
  - python main.py test

## 5. sqlalchemy 介绍

- 默认值
  - 建表结构（初始化实例）有效的要使用参数 server_default，即"desc 表结构"可以查到默认值，而且其值必须是字符串
  - 往表中插入记录默认值有效用参数 default
  - 示例：port = Column(Integer, default=14119, server_default="14419")
- on duplicate key update 实现
  - 查看 model/base.py 中的 insert_for_update
  - 参考：https://stackoverflow.com/questions/6611563/sqlalchemy-on-duplicate-key-update
- 会话 (session) 和 连接 (connection)
  - 创建一个 session，连接池会分配一个 connection。当 session 在使用后显示地调用 session.close()，也不能把这个连接关闭，而是由连接池管理并复用连接
  - session 使用连接来操作数据库，一旦任务完成 session 会将数据库 connection 交还给 pool
  - 确保 session 在使用完成后用 session.close、session.commit 或 session.rollback 把连接还回 pool，`这是一个必须在意的习惯`

## 6. sqlalchemy 异常分析

- 问题：Can't reconnect until invalid transaction is rolled back
  - 应用程序里的逻辑代码有问题，在进行数据库的写入操作后，缺少 commit、rollback、close 的操作将连接放回连接池，连接池没法管理，当这个连接被数据库回收后，也就出现了上面的异常
  - create_engine 时指定的连接池中的连接的回收时间大于数据库配置的未活动连接过期时间
- 预连接
  - 所有的 sqlAlchemy 池实现都有一个共同点，即它们都没有`预创建`连接，即所有的实现都要等到第一次使用后才能创建连接
  - 为了避免第一次请求建立连接较慢，我们采取了`强制预连接`的处理，即每次起服后，创建一定数量的数据连接
  - 参考官网：https://www.osgeo.cn/sqlalchemy/core/pooling.html

## 7. 高级用法

- [详情](./doc/advanced_usage.md)
