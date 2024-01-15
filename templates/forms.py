from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField
from wtforms.validators import Length, DataRequired, Email, EqualTo, NumberRange

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=1, max=120)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmPassword = PasswordField('Confirm Password', validators=[
        DataRequired(message='This field is required.'),
        EqualTo('password', message='Passwords must match.')
    ])

    submit = SubmitField('Sign up!')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')

    join = SubmitField('Login')

class ProgramCreator(FlaskForm):
    programName = StringField('Title', validators=[DataRequired()])
    requiredCost = StringField('Cost($$/month)', validators=[DataRequired()])
    priority = StringField('Priority 1-3', validators=[DataRequired(), NumberRange(min=1, max=3)])

    create = SubmitField('Done')

class Goals_notesForm(FlaskForm):
    goalName = StringField('Goal', validators=[DataRequired()])
    description = StringField('Describe your goal', validators=[DataRequired(), Length(max=50)])
    accomplishedTime = StringField('When do you want to accomplish this?', validators=[DataRequired()])

    create = SubmitField('Done')
