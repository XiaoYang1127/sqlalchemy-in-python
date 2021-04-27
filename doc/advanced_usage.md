# sqlalchemy 高阶用法整理

## 1. 批量插入

```python
session.execute(
    User.__table__.insert(),
    [{'name': randint(1, 100),'age': randint(1, 100)} for i in xrange(10000)]
)
session.commit()
```

## 2. 如何让执行的 SQL 语句增加前缀

```python
session.query(User.name).prefix_with('HIGH_PRIORITY').all()
session.execute(
    User.__table__.insert().prefix_with('IGNORE'),
     {'id': 1, 'name': '1'}
)
```

## 3. 如何替换一个已有主键的记录（类似 insert on duplicate key update)

```python
user = User(id=1, name='ooxx', age=10)
session.merge(user)
session.commit()
```

## 4. 如何使用无符号整数

```python
from sqlalchemy.dialects.mysql import INTEGER
id = Column(INTEGER(unsigned=True), primary_key=True)
```

## 5. 模型的属性名需要和表的字段名不一样

```python
from_ = Column('from', CHAR(10))
```

## 6. 获取字段的 c 长度

```python
User.name.property.columns[0].type.length
```

## 7. 包含

```python
query.filter(User.name.contains(subname))
```

## 8. 别名

```python
from sqlalchemy.orm import aliased
User111 = aliased(User)
query.filter(User111.name.contains(subname))
```

## 9. 关联查询

```python
# 不使用 join
session.query(User.name, Address.email_address).filter(User.id==Address.user_id).filter(Address.email_address=="test@test.com").all()

# 有外键情况下
session.query(User).join(Address).filter(Address.email_address=="test@test.com").all()

# 无外键情况下
session.query(User.name).join(Address, User.id==Address.user_id).filter(Address.email_address=="test@test.com").all()
```

## 10. 子查询

```python
# sql 形式
mysql> SELECT users.*, adr_count.address_count FROM users LEFT OUTER JOIN
    ->     (SELECT user_id, count(*) AS address_count
    ->         FROM addresses GROUP BY user_id) AS adr_count
    ->     ON users.id=adr_count.user_id

# 子查询
sbq = session.query(Address.user_id, func.count('*').label('address_count')).group_by(Address.user_id).subquery()
session.query(User.name, sbq.c.address_count).outerjoin(sbq, User.id==sbq.c.user_id).all()
```

## 11. 外键数据自动删除

```python
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    addresses = relationship("Address", order_by="Address.id", backref="user", cascade="all, delete, delete-orphan")


class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True)
    email_address = Column(String(32), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
```

# 12. 悲观锁

```python
# session 1
addr = Address.query.filter_by(user_id=3).with_for_update().first

# session 2
addr = Address.query.filter_by(user_id=3).with_for_update().first
```
