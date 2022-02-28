import os
import flask
from flask import Flask, render_template, request, flash, redirect, url_for
from Units.DataBase import SQLAlchemy, DataBase
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from random import choice
from werkzeug.security import generate_password_hash, check_password_hash
from Units.SiteUser import SiteUser
from validate_email import validate_email


class UserLogin:
    """ Класс для описания пользователя, который вошел в аккаунт """
    def fromDB(self, site_user_id, db: DataBase):
        self.__user = db.get_site_user(site_user_id)
        return self

    def create(self, reader):
        self.__user = reader
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.__user.ID)


database = SQLAlchemy()

app = Flask(__name__,
            template_folder='../templates',
            static_folder='../static')

login_manager = LoginManager(app)  # Создаем менеджер для регистрации и входа в аккаунт пользователями
login_manager.login_view = 'api_login'

app.config['DEBUG'] = True  # Ставим DEBUG = True для тестов, потом нужно поменять на False
app.config['SECRET_KEY'] = 'SsdSvdhstebfFSvfhsvdCFDDGCEVsbfgsvfcaFCbsdfscFSV'  # Выгружаем из окружения секретный ключ


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, database)  # Берем пользователя из базы данных


@app.route('/login', methods=['GET', 'POST'])
def api_login():
    """ Вход пользователя в аккаунт """
    user = database.get_site_user(current_user.get_id())  # Берем пользователя из бд

    if user:
        return redirect(url_for('index'))  # Редиректим пользователя на главную страницу, если он уже вошел в аккаунт

    shoppers = database.get_shoppers()

    if request.method == 'POST':
        # Обработчик POST запроса
        email = request.form.get('email')  # Получаем почту из формы
        password = request.form.get('password')  # Получаем пароль из формы

        next_url = request.args.get('next')

        if not email or not password:
            # Проверяем данные на валидность
            msg = 'Error: invalid data'
            return render_template('login.html', user=user, message=msg, popular_shopper=choice(shoppers))

        user = database.get_site_user_by_email(email)
        if user and password and check_password_hash(user.password, password):  # Проверяем правильно ли введен пароль
            userlogin = UserLogin().create(user)  # Создаем объект зарегистрированного пользователя
            login_user(userlogin)
            if next_url:
                return redirect(next_url)  # После входа - переносим пользователя на главную страницу

            return redirect(url_for('index'))  # После входа - переносим пользователя на главную страницу

    return render_template('login.html', user=user, popular_shopper=choice(shoppers))


@app.route('/registration', methods=['GET', 'POST'])
def api_registration():
    """ Регистрация пользователя """
    user = database.get_site_user(current_user.get_id())

    if user:
        return redirect(url_for('index'))  # Редиректим пользователя на главную страницу, если он уже вошел в аккаунт

    shoppers = database.get_shoppers()

    if request.method == 'POST':
        # Обрабатываем POST запрос
        email = request.form.get('email')  # Получаем поле email из html формы
        password = request.form.get('password')  # Получаем поле password из html формы
        confirm_password = request.form.get('confirm-password')  # Получаем поле confirm_password из html формы

        print(email)
        print(password)
        print(confirm_password)

        if not email or not password or not confirm_password:
            # Проверяем данные на валидность
            msg = 'Error: invalid data'
            return render_template('registration.html', message=msg, popular_shopper=choice(shoppers))

        if not password == confirm_password:
            # Проверяем сходство паролей
            msg = 'Error: password != confirm_password'
            return render_template('registration.html',  message=msg, popular_shopper=choice(shoppers))

        password = generate_password_hash(password)  # Хешируем пароль

        database.add_user(SiteUser(None, [], False, email, password))  # Создаем пользователя в бд
        msg = 'Done: you registered successfully'
        flash(msg)
        return redirect(url_for('api_login'))  # Редиректим пользователя на страницу входа в аккаунт

    return render_template('registration.html', popular_shopper=choice(shoppers))


@app.route('/sign_out', methods=['GET'])
@login_required
def api_sign_out():
    """ Выход из аккаунта """
    logout_user()
    flash('Вы успешно вышли из аккаунта')
    return redirect(url_for('index'))


@app.route('/')
def index():
    """ Главная страница сайта """
    user = database.get_site_user(current_user.get_id())  # Берем пользователя из библиотеки
    shoppers = database.get_shoppers()
    return render_template('index.html', active="home",
                           popular_shopper=choice(shoppers))


@app.route('/add-to-cart')
@login_required
def add_to_cart():
    user = database.get_site_user(current_user.get_id())  # Берем пользователя из библиотеки
    return redirect(url_for('index'))


@app.route('/cart')
@login_required
def cart():
    shoppers = database.get_shoppers()
    return render_template('catalog.html', active="cart", shoppers=shoppers,
                           popular_shopper=choice(shoppers))


@app.route('/catalog', methods=['GET', 'POST'])
def catalog():
    """ Главная страница сайта """
    user = database.get_site_user(current_user.get_id())
    shoppers = database.get_shoppers()

    if request.method == 'POST':
        search = request.form.get('search')
        if not search:
            return render_template('catalog.html', active="catalog", shoppers=shoppers,
                                   popular_shopper=choice(shoppers))

        search = ''.join([letter for letter in search if letter.isalpha()]).lower()
        shoppers = [shopper for shopper in database.get_shoppers()
                    if ''.join([letter for letter in shopper.title if letter.isalpha()]).lower().startswith(search)]
        return render_template('catalog.html', active="catalog", shoppers=shoppers,
                               popular_shopper=choice(database.get_shoppers()))

    return render_template('catalog.html', active="catalog", shoppers=shoppers,
                           popular_shopper=choice(shoppers))


app.run()
