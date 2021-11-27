from flask import Flask, render_template,request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import time
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'the random string'
db = SQLAlchemy(app)
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

#######################MODELS###############################

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50))
    email =  db.Column(db.String(50))
    password = db.Column(db.String(50))
    role = db.Column(db.Integer)
    image = db.Column(db.String(50))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500))
    section = db.Column(db.Integer)
    author = db.Column(db.Integer, db.ForeignKey('user.id'))
    author_name = db.Column(db.String(50))
    author_image = db.Column(db.String(50))
    likes = db.Column(db.Integer, default=0)
    


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20))
    name = db.Column(db.String(50))
    instructor = db.Column(db.Integer, db.ForeignKey('user.id'))



class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String(100))
    date = db.Column(db.Integer)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))

class Saved(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.Integer, db.ForeignKey('post.id'))
    user = db.Column(db.Integer, db.ForeignKey('user.id'))

class Attend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course = db.Column(db.Integer, db.ForeignKey('course.id'))
    student = db.Column(db.Integer, db.ForeignKey('user.id'))




    



######################ROUTES################################
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form['email']
        password = request.form['password']
        data = User.query.filter_by(email=email,
                                    password=password).first()

        if data is not None:
            session['user'] = data.id
            print(session['user'])
            return redirect(url_for('index'))

        return render_template('incorrectLogin.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        if not re.fullmatch(regex, email):
            return render_template('invalidEmail.html')
        data = User.query.filter_by(email=email).first()
        if data is not None:
            return render_template('invalidEmail.html')
        new_user = User(name=request.form['name'],
                        email=email,
                        password=request.form['password'], role=request.form['role'],
                        image=request.form['image']
                        )

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')



@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('name', None)
    return redirect(url_for('login'))


@app.route('/index')
def index():
    user_id = session['user']
    username = User.query.get(session['user']).name
    today = time.strftime("%m/%d/%Y")
    showPost = Post.query.filter_by(section=0).order_by(desc(Post.id)).all()
    reminder = Reminder.query.filter_by(user=user_id).filter_by(date = today).all()
    return render_template('index.html', reminder=reminder, showPost=showPost)

@app.route('/ShowOpportunity')
def ShowOpportunity():
    user_id = session['user']
    username = User.query.get(session['user']).name
    today = time.strftime("%m/%d/%Y")
    showPost = Post.query.filter_by(section=1).order_by(desc(Post.id)).all()
    reminder = Reminder.query.filter_by(user=user_id).filter_by(date = today).all()
    return render_template('index.html', reminder=reminder, showPost=showPost)

@app.route('/ShowResource')
def ShowResource():
    user_id = session['user']
    username = User.query.get(session['user']).name
    today = time.strftime("%m/%d/%Y")
    showPost = Post.query.filter_by(section=2).order_by(desc(Post.id)).all()
    reminder = Reminder.query.filter_by(user=user_id).filter_by(date = today).all()
    return render_template('index.html', reminder=reminder, showPost=showPost)


@app.route('/AddPost', methods=['GET', 'POST'])
def AddPost():
    if request.method == 'POST':
        user_id = session['user']
        
        new_post = Post(content=request.form['content'],section=request.form['section'], 
                                author=user_id,author_name=User.query.get(user_id).name,
                                author_image=User.query.get(user_id).image)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('index'))

    else:
        return render_template('addPost.html')

@app.route('/AddReminder', methods=['GET', 'POST'])
def AddReminder():
    if request.method == 'POST':
        user_id = session['user']
        new_reminder = Reminder(note=request.form['note'],date=request.form['date'], 
                                user=user_id)
        db.session.add(new_reminder)
        db.session.commit()
        return redirect(url_for('index'))

    else:
        return render_template('addReminder.html')


@app.route('/like')
def like():
    post_id = int(request.args['id'])
    post =  Post.query.get(post_id)
    post.likes += 1
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/save')
def save():
    post_id = int(request.args['id'])
    user_id = session['user']
    data = Saved.query.filter_by(post=post_id,
                                    user=user_id).first()
    if data is None :
      new_saved = Saved(post=post_id, user=user_id)
      db.session.add(new_saved)
      db.session.commit()
    return redirect(url_for('index'))

@app.route('/AddCourse')
def AddCourse():
    user_id = session['user']
    new_course = Course(code=request.form['code'],name=request.form['name'],instructor=user_id)
    db.session.add(new_course)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/attend')
def attend():
    user_id = session['user']
    code = request.form['code']
    course = Course.query.filter_by(code=code).one()
    new_attend = Attend(course=course,student=user_id)
    db.seesion.add(new_attend)
    db.session.commit()
    return redirect(url_for('index'))








    



######################MAIN################################

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)