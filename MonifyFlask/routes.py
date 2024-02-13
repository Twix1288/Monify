from flask import render_template, request, flash, redirect, url_for, make_response, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, create_refresh_token, get_jwt_identity, \
    get_jwt_header
import os
import secrets
from PIL import Image
from MonifyFlask import app, db, bcrypt, login_user, current_user, logout_user, login_required
from MonifyFlask.forms import LoginForm, RegistrationForm, ProgramCreator, Goals_notesForm, UpdateAccountForm
from MonifyFlask.models import Users, Programs
@app.route('/notes', methods=['GET', 'POST'])
def notes():
    goals_notes = Goals_notesForm()
    return render_template("notes.html", goals_notes=goals_notes)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    login_form = LoginForm(request.form)
    if login_form.validate_on_submit():
        user = Users.query.filter_by(username=login_form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, login_form.password.data):
            flash(f'Welcome back {user.username}', 'success')
            login_user(user, remember=login_form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
    return render_template("login.html", login=login_form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    Register = RegistrationForm(request.form)

    if Register.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(Register.confirmPassword.data).decode('utf-8')
        user = Users(username=Register.username.data, email=Register.email.data, age=Register.age.data,
                     password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {Register.username.data}! You are now able to log in...', 'success')
        return redirect(url_for('login'))

    return render_template("register.html", register=Register)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    update = UpdateAccountForm()
    if update.validate_on_submit():
        if update.picture.data:
            picture_file = save_picture(update.picture.data)
            current_user.image_file = picture_file
        current_user.username = update.username.data
        current_user.email = update.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        update.username.data = current_user.username
        update.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, update=update)

@app.route('/financial', methods=['GET', 'POST'])
@login_required
def finances():
    programs = Programs.query.filter_by(user_id=current_user.id).all()
    return render_template("finances.html", programs = programs)
@app.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    program = ProgramCreator()
    if program.validate_on_submit():
        post = Programs(title=program.name.data, cost_gain=program.Cost_gain.data, priority=program.priority.data,
                        description=program.description.data,
                        user_id = current_user.id)  # Associate post with current user
        db.session.add(post)
        db.session.commit()
        flash(f'Post: {program.name.data} has now been created!', 'success')
        return redirect(url_for('finances'))
    return render_template('posts.html', title='Account', program=program)

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Programs.query.get_or_404(post_id)
    return render_template('programPost.html', post=post)
