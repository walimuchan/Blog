import os


from flask import Flask, render_template, url_for, flash, redirect
from forms import RegisterForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = 'c94f02178b1dd338f3f5a012606fe5f6'



posts = [
    {
        'title':'Uganda Crowned Miss World!',
        'author':'Walimuchan Phiona',
        'content':'First post',
        'date':'Jan 25,2019'
    },

    {
        'title':'City on Fire!',
        'author':'Samuel Ogol',
        'content':'Second post',
        'date':'Jan 31,2019'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm( )
    if form.validate_on_submit():
       flash('Your account has been sucessfully created!', 'success')
       return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
       flash('sucessfully logged in!')
       return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)




if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)