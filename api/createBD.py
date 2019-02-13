from app import db, Users
db.create_all()

# num = 100
# while num>0:
#     admin = Users('admin'+str(num), 'admin@example.com'+str(num))
#     db.session.add(admin)
#     num = num-1
admin = Users('admin', 'admin@example.com')
guest = Users('guest', 'guest@example.com')
db.session.add(admin)
db.session.add(guest)
db.session.commit()
db.session.close()
