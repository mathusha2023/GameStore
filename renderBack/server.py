from flask import Flask
from data import db_session
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'niggers'

def main():
    db_session.global_init("db/users.db")
    # app.run(host="127.0.0.1", port=8000)
@app.route("/")
def index():
    return "Тута будет основной чето"
@app.route('/register')
def about():
    return 'Здесь будет регистрация'
@app.route('/login', methods=['GET', 'POST'])
def about1():
    return 'Здесь будет вход'
# @app.route('/<>')
# def about2():
#     return 'Здесь будет информация об одной игре лол'
@app.route('/about')
def about3():
    return 'Здесь будет информация об авторе сайта.'



if __name__ == "__main__":
    main()
