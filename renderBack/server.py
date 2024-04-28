from flask import Flask, render_template, redirect, request
from data import db_session
from data.db_session import create_session
import os
from data.users import User
from forms.registerform import RegisterForm
from forms.loginform import LoginForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import requests
import pickle

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
SECRET_KEY = 'IfYoUhAvErEaDtHiSyOuArEgEy'
app.config['SECRET_KEY'] = SECRET_KEY


def main():
    if not os.path.isdir("db"):
        os.mkdir("db")
    db_session.global_init("db/users.db")
    app.run(host="127.0.0.1", port=8000)


@app.route("/", methods=['GET', 'POST'])
def index():
    url = 'http://127.0.0.1:8080/games'
    response = requests.get(url)
    game_dict = {}
    if response.status_code == 200:
        data = response.json()  # Перевод в словарик
        games_list = data.get('games', [])  # список игр из данных, по ключу 'games'
        for game in games_list:  # ПытаЮсь поменять айди на имя
            author_id = int(game['author'])
            author = get_login_by_id(author_id)
            if author:
                game['author'] = author
                game['author_id'] = author_id
        game_dict = games_list
    print(game_dict)
    return render_template('index.html', game_dict=game_dict)


def get_login_by_id(user_id):
    session = create_session()
    user = session.query(User).filter(User.id == user_id).first()
    session.close()
    return user.login if user else None


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.login == form.name.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(login=form.name.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/senddata', methods=['POST', 'GET'])
def senddata():
    url = "http://127.0.0.1:8080/games"
    if request.method == 'POST':
        title = request.form.get('title')
        desk = request.form.get('desk', '')
        author = int(current_user.get_id())
        prev_file = request.files['prev']
        zip_file = request.files['file']
        files = request.files.getlist('files')
        data = {
            "title": title,
            "desc": desk,
            "author": author,
            "prev": ("png", prev_file.read()),
            "file": ("zip", zip_file.read()),
            "images": [(f.filename.split('.')[-1], f.read()) for f in files]
        }
        requests.post(url, data=pickle.dumps(data)).json()
        return redirect('/')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/create")
@login_required
def create():
    return render_template('create.html')


@app.route("/mygames")
@login_required
def mygames():
    url = f'http://127.0.0.1:8080/games?author={int(current_user.get_id())}'
    response = requests.get(url)
    game_dict = {}
    if response.status_code == 200:
        data = response.json()
        games_list = data.get('games', [])
        for game in games_list:
            author_id = int(game['author'])
            author = get_login_by_id(author_id)
            if author:
                game['author'] = author
                game['author_id'] = author_id
        game_dict = games_list
    print(game_dict)
    return render_template('mygames.html', game_dict=game_dict)


@app.route("/privacy")
def privacy():
    return render_template('privacy.html')


@app.route("/terms")
def terms():
    return render_template('terms.html')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


if __name__ == "__main__":
    main()
