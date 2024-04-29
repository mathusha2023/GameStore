from flask import Flask, render_template, redirect, request
from data import db_session
from data.db_session import create_session
from dotenv import load_dotenv
import os
from data.users import User
from forms.registerform import RegisterForm
from forms.loginform import LoginForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import requests
import pickle

load_dotenv()
HOST = os.getenv('NEAPI_HOST')
PORT = os.getenv('NEAPI_PORT')
SECRET_KEY = os.getenv('NEAPI_SECRET_KEY')
API_HOST = os.getenv("API_HOST")
API_PORT = os.getenv('API_PORT')
api_url = f'http://{API_HOST}:{API_PORT}'
print(api_url)
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = SECRET_KEY


def main():
    if not os.path.isdir("db"):
        os.mkdir("db")
    db_session.global_init("db/users.db")
    app.run(host=HOST, port=PORT)


@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
@app.route("/games", methods=['GET', 'POST'])
def index():
    name = request.args.get("name", None)
    url = f'{api_url}/games' if name is None else f'{api_url}/games?name={name}'
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
    return render_template('index.html', game_dict=game_dict, api_url=api_url, title="Главная")


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
    return render_template('register.html', title='Регистрация', form=form, api_url=api_url)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect("/index")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form, api_url=api_url)


@app.route('/senddata', methods=['POST', 'GET'])
def senddata():
    url = f"{api_url}/games"
    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('desc', '')
        author = int(current_user.get_id())
        prev_file = request.files['prev']
        zip_file = request.files['file']
        files = request.files.getlist('files')
        if not prev_file.filename.endswith('.png'):
            prev_file = open('url_for(static, filename=images/default.png)', 'rb')

        images = []
        for file in files:
            images.append(("png", file.read()))

        data = {
            "title": title,
            "desc": desc,
            "author": author,
            "prev": ("png", prev_file.read()),
            "file": ("zip", zip_file.read()),
            "images": images
        }
        req = requests.post(url, data=pickle.dumps(data))
        if req.status_code == 200:
            return redirect(f'/game/{req.json()["id"]}')
        else:
            return redirect('/index')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/index")


@app.route("/create")
@login_required
def create():
    return render_template('create.html', api_url=api_url, title="Создать игру")


@app.route("/mygames")
@login_required
def mygames():
    url = f'{api_url}/games?author={int(current_user.get_id())}'
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
    return render_template('mygames.html', game_dict=game_dict, api_url=api_url, title="Мои игры")


@app.route('/game/<game_id>')
def game_detail(game_id):
    game_data = {}
    url = f'{api_url}/game/{game_id}'
    response = requests.get(url)
    if response.status_code == 200:
        game_data = response.json()
        author_id = int(game_data['author'])
        author = get_login_by_id(author_id)
        if author:
            game_data['author'] = author
            game_data['author_id'] = author_id
    print(game_data)
    return render_template('game.html', game=game_data, api_url=api_url, title=game_data["title"])


@app.route("/delete/<game_id>")
def delete(game_id):
    requests.delete(game_id)
    return redirect('/index')


@app.route("/privacy")
def privacy():
    return render_template('privacy.html', title="Политика конфиденциальности")


@app.route("/terms")
def terms():
    return render_template('terms.html', title="Условия пользования")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


if __name__ == "__main__":
    main()
