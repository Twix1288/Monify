from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField, HiddenField, FileField
from flask_wtf.file import FileAllowed
from wtforms.validators import Length, DataRequired, Email, EqualTo, NumberRange, ValidationError
from .models import Users
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"autocomplete": "off"})
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=1, max=120)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmPassword = PasswordField('Confirm Password', validators=[
        DataRequired(message='This field is required.'),
        EqualTo('password', message='Passwords must match.')
    ], render_kw={"autocomplete": "new-password"})

    submit = SubmitField('Sign up!')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)], )
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')

    join = SubmitField('Login')


class ProgramCreator(FlaskForm):
    name = StringField('Title', validators=[DataRequired()], render_kw={"autocomplete": "off"})
    Cost_gain = IntegerField('Cost per month: (negative number for taking out money)', validators=[DataRequired()],
                             render_kw={"autocomplete": "off"})
    priority = IntegerField('Priority 1-3', validators=[DataRequired(), NumberRange(min=1, max=3)],
                           render_kw={"autocomplete": "off"})
    description = StringField('Describe your program', validators=[DataRequired(), Length(max=50)],
                              render_kw={"autocomplete": "off"})
    create = SubmitField('Post')


class Goals_notesForm(FlaskForm):
    goalName = StringField('Goal', validators=[DataRequired()], render_kw={"autocomplete": "off"})
    description = StringField('Describe your goal', validators=[DataRequired(), Length(max=50)],
                              render_kw={"autocomplete": "off"})
    accomplishedTime = StringField('When do you want to accomplish this?', validators=[DataRequired()],
                                   render_kw={"autocomplete": "off"})

    create = SubmitField('Done')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = Users.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = Users.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
