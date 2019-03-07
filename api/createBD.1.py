from app import db
from model import Users, Post, Category, Person, EmailAddress, Role
db.drop_all()
db.create_all()

# num = 100
# while num>0:
#     admin = Users('admin'+str(num), 'admin@example.com'+str(num))
#     db.session.add(admin)
#     num = num-1
admin = Users('admin', 'admin@example.com')
guest = Users('guest', 'guest@example.com')

py = Category('Python')
js = Category('Javascript')
p = Post('Hello Python!', 'Python is pretty cool', py)
p1 = Post('Python web', 'Python web is easy', py)
j = Post('Hello Javascript!', 'Javascript is pretty cool', js)
# db.session.add(py)

person1 = Person('张三')
person2 = Person('李四')

address1 = EmailAddress('zhangsan@qq.com', person1)
address2 = EmailAddress('lisi@163.com', person2)
address3 = EmailAddress('lisi2@163.com', person2)
address4 = EmailAddress('lisi3@163.com', person2)
address5 = EmailAddress('lisi4@163.com', person2)

ro1 = Role(name="admin")
# 先将ro1对象添加到会话中，可以回滚。
db.session.add(ro1)
# db.session.add_all([person1,person2])
# db.session.commit()


db.session.add_all([admin, guest, py, p, person1, person2,
                    js, j, address1, address2, address3, address4, address5 ])

db.session.commit()

a = person2.emails.all()
for email in a:
  print(email.email)
db.session.close()
