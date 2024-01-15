from flask import Flask, render_template, request, flash, redirect, url_for
from templates.config import SECRET_KEY
from flask_bootstrap import Bootstrap
from templates.forms import LoginForm, RegistrationForm, ProgramCreator, Goals_notesForm
from flask_sqlalchemy import SQLAlchemy
from templates.config import SQLALCHEMY_DATABASE_URI
from sqlalchemy import ForeignKey, Text, Column, Integer
from sqlalchemy.orm import relationship

##Initailization
app = Flask(__name__, instance_relative_config=True)
Bootstrap(app)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

db = SQLAlchemy(app)

# Models for Database
class Users(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, unique=True)
    age = Column(Integer, nullable=False)
    email = Column(Text, nullable=False)
    username = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    goals_notes = relationship('Goals_Notes', back_populates='user')
    finances = relationship('FinanceInfo', back_populates='user')

    def __repr__(self):
        return f"<User username={self.username}>"


class FinanceInfo(db.Model):
    __tablename__ = 'finance_info'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    total_amount = Column(Integer, nullable=False)
    choice_gen = Column(Integer, nullable=False)
    allowance = Column(Integer, nullable=False)
    income = Column(Integer, nullable=False)

    user = relationship('Users', back_populates='finances')

    def __repr__(self):
        return (f"<User total_amount={self.total_amount} allowance={self.allowance} income={self.income} "
                f"made all by user={self.user.username}>")


class Goals_Notes(db.Model):
    __tablename__ = 'goals_notes'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    note = Column(Text, nullable=False)

    user = relationship('Users', back_populates='goals_notes')

    def __repr__(self):
        return f"<User note={self.note} made all by user={self.user.username}>"


# Function to create tables
def create_tables():
    with app.app_context():
        db.create_all()
        print("Database tables created.")


# Call the function when the application starts
create_tables()

#Routes to all pages
@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/finances', methods=['GET', 'POST'])
def finances():
    program_creator = ProgramCreator()
    return render_template("finances.html", program_creator=program_creator)


@app.route('/notes', methods=['GET', 'POST'])
def notes():
    goals_notes = Goals_notesForm()
    return render_template("notes.html", goals_notes=goals_notes)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login = LoginForm(request.form)
    if login.validate_on_submit():
        flash(f'Welcome,{login.username.data}!', 'success')
        return redirect(url_for('hello_world'))
    else:
        flash(f'Login Unsuccessful','danger')
    return render_template("login.html", login=login)


@app.route('/register', methods=['GET', 'POST'])
def register():
    register= RegistrationForm(request.form)

    if register.validate_on_submit():
        flash(f'Account created for {register.username.data}!', 'success')
        return redirect(url_for('login'))
        #username = request.form['username']
        #email = request.form['email']
        #age = request.form['age']
        #password = request.form['password']

        #user_login = Users(username=username, email=email, age=age, password=password)
        #db.session.add(user_login)

        #try:
           # db.session.commit()
            #return "User was added"
        #except Exception as e:
         #   db.session.rollback()
          #  print(f"Error: {e}")
          #  return "An error occurred during registration. Please try again later."

    return render_template("register.html", register=register)


if __name__ == '__main__':
    app.run(debug=True)
