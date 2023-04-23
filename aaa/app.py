from flask import Flask, redirect
from flask import render_template
from flask import url_for
from flask_login import LoginManager, login_required, logout_user, login_user, current_user
from forms.user import RegisterForm, LoginForm
from forms.help import HelpingForm
from data.news import News
from data.users import User
# подключение helps.pу
from data.helps import Help
from data.marks import Marks
from data import db_session

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/blogs.db")
    db_session.create_all()
    app.run()


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
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
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        print(user)
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/helping', methods=['GET', 'POST'])
def helping():
    form = HelpingForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        problems = Help(
            problem=form.problem.data,
            geo=form.geo.data,
            number=form.number.data
        )
        db_sess.add(problems)
        db_sess.commit()
        return redirect('/home')


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/user/<string:name>/<int:id>')
def user(name, id):
    return 'User page:' + name + "-" + str(id)


@app.route('/reg')
def reg():
    return render_template('bd.html')


@app.route('/take_part')
def take_part():
    return render_template('partner.html')


@app.route('/marks')  # нужно переписать это дабы получать метки из бд в формате ниже
def get_marks():
    # db_sess = db_session.create_session()
    # marks = db_sess.query(Marks).filter(Marks.is_completed is False).first()
    # return marks
    marks = [{"id": "1",  # тестовые данные
              "title": "вскопать картошку",
              "created_date": "1681994400000",  # время в миллисекундах от (янв 1, 1970, 00:00:00.000)
              "is_completed": "False",
              "x_coord": "51.4019",
              "y_coord": "39.1103",
              "user_id": "1"},
             {"id": "2",
              "title": "починить автомобиль",
              "created_date": "1681416600000",
              "is_completed": "False",
              "x_coord": "52.4019",
              "y_coord": "39.1103",
              "user_id": "3"}]
    return marks


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    app.run(debug=True)
