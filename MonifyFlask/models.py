from datetime import datetime
from sqlalchemy import ForeignKey, Text, Column, Integer
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, current_user, logout_user, login_required
from flask_migrate import Migrate

login_manager = LoginManager()
db = SQLAlchemy()
# Models for Database
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))
class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, unique=True)
    age = Column(Integer, nullable=False)
    email = Column(Text, nullable=False)
    username = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    image_file = db.Column(db.String(20), nullable= False, default='default.png')
    goals_notes = relationship('Goals_Notes', back_populates='user')
    finances = relationship('FinanceInfo', back_populates='user')

    def __repr__(self):
        return f"<User username={self.username}>"


class FinanceInfo(db.Model):
    __tablename__ = 'finance_info'
    id = db.Column(Integer, primary_key=True)
    user_id = db.Column(Integer, ForeignKey('users.id'))
    total_amount = db.Column(db.Integer, nullable=False)
    income = db.Column(Integer, nullable=False)
    date = db.Column(db.DateTime, nullable= False, default = datetime.utcnow)

    user = relationship('Users', back_populates='finances')

    def __repr__(self):
        return (f"<User total_amount={self.total_amount} allowance={self.allowance} income={self.income} "
                f"made all by user={self.user.username}>")


class Goals_Notes(db.Model):
    __tablename__ = 'goals_notes'
    id = db.Column(Integer, primary_key=True)
    user_id = db.Column(Integer, ForeignKey('users.id'))
    note = db.Column(Text, nullable=False)

    user = relationship('Users', back_populates='goals_notes')

    def __repr__(self):
        return f"<User note={self.note} made all by user={self.user.username}>"

