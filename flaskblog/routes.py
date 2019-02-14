import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegisterForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import User, Posts
from flask_login import login_user, current_user, logout_user, login_required


#HOME PAGE
@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Posts.query.paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)

#ABOUT PAGE
@app.route("/about")
def about():
    return render_template('about.html', title='About')

#SIGNUP ROUTE
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm( )
    if form.validate_on_submit():
       hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
       user = User(username=form.username.data, email=form.email.data, password=hashed_password)
       db.session.add(user)
       db.session.commit()
       flash('Your account has been sucessfully created!log in to continue', 'success')
       return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

#LOGIN ROUTE
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.save.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('log in unsucessful!', 'danger')

    return render_template('login.html', title='Login', form=form)

#LOGOUT ROUTE
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

#IMAGE ROUTE
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pic',  picture_fn )
    
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


#USER ACCOUNT ROUTE
@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your Account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email


    image_file = url_for('static', filename='profile_pic/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)
    
    
#NEW POSTS ROUTE
@app.route("/posts/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        posts = Posts(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(posts)
        db.session.commit()
        flash('your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='Create New Post', form=form, legend='Create New Post')

#POSTS ROUTE
@app.route("/posts/<int:post_id>")
def post(post_id):
    posts = Posts.query.get_or_404(post_id)
    return render_template('post.html', title='post.title', posts=posts)

#UPDATE POSTS ROUTE
@app.route("/posts/<int:post_id>/update",  methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    posts = Posts.query.get_or_404(post_id)
    if posts.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        posts.title = form.title.data
        posts.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=posts.id))
    elif request.method == 'GET':
        form.title.data = posts.title
        form.content.data = posts.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')


#DELETE_POSTS ROUTE
@app.route("/posts/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    posts = Posts.query.get_or_404(post_id)
    if posts.author != current_user:
        abort(403)
    db.session.delete(posts)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))
    

