# tornado + sqlalchemy + redis + mysql

## 1. 背景

- tornado 是一个用 Python 编写的异步 HTTP 服务器，同时也是一个 web 开发框架
- SQLAlchemy 是一个 Python 的 SQL 工具包以及数据库对象映射框架。它包含整套企业级持久化模式，专门为高效和高性能的数据库访问

## 2. 特点

- 支持 restful api 风格
- 缓存采用 redis，持久化采用 mysql
- 关于 ORM 实现
  - 增加，删除，修改采用 ORM 方式进行
  - 查询，insert from select, insert on duplicate key 等采用 sql expression

## 3. 安装

- 安装 python3.7.5
- 安装依赖
  - cd sqlalchemy-in-python
  - python3 -m venv venv
  - source venv/bin/activate
  - pip3 install -r requirements.txt

## 4. 运行

### linux

- ./run_mine

## 5. 用例测试

- 测试用例在 script/tests 下，如有增加，修改 start.py 里面的 do_unittest 函数即可
- 双击 run_unittest.exe，进行自动化测试

## 6. 其他

- 如有疑问，提交 issues，定期回复
