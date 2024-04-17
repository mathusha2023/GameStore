from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from forms.registerform import RegisterForm
from forms.loginform import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'niggers'


def main():
    db_session.global_init("db/users.db")
    app.run(host="127.0.0.1", port=8000)


@app.route("/")
def index():
    return "Тута будет основной чето"


@app.route('/register', methods=['GET', 'POST'])
def reqister():
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
        return redirect('/')
    return render_template('login.html', title='Авторизация', form=form)


# @app.route('/<>')
# def about2():
#     return 'Здесь будет информация об одной игре лол'
@app.route('/about')
def about3():
    return 'Здесь будет информация об авторе сайта.'


if __name__ == "__main__":
    main()
