from app.models import User, Post, Post_Tag, Project, Project_Tag

u = User(username ='Hunter', email = 'hvanlear@gmail.com')
u.set_password(password = 'Freeman78337833!')

db.session.add(u)
db.session.commit()

p = Post(title = 'Test', body = 'Test', user_id = 1)
db.session.add(p)
db.session.commit()