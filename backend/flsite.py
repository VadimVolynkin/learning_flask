from flask import Flask, render_template, url_for, request, flash, session, abort, g, redirect
# render_template                    - рендер
# url_for(endpoint, **values)        - генерирует URL-адрес по имени функции-обработчика
# request                            - объект данных текущего запроса
# session                            - объект сессии
# flash                              - мгновенные сообщения
# abort                              - функция для вызова ошибки внутри обработчика
# g                                  - хранит временную пользовательскую информацию для обработки запроса

import sqlite3
import os

from FDataBase import FDataBase
from UserLogin import UserLogin

from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# =========================================================================================================================
# КОНФИГ
# =========================================================================================================================
# все переменные заглавными буквами во фласке - конфиг


# секретный ключ для генерации сессий и токенов
SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'
DATABASE = '/tmp/flsite.db'
USERNAME = 'admin'
PASSWORD = '123'
DEBUG = True


# =========================================================================================================================
# СТРАНИЦЫ ПРИЛОЖЕНИЯ 
# =========================================================================================================================

# создаем экземпляр приложения: __name__ = имя текушего файла = имя приложения
app = Flask(__name__)

# конфигурируем приложение из параметров выше
app.config.from_object(__name__)  

# переопределение расположения базы: создадим базу в этом каталоге
app.config.update(dict(DATABASE=os.path.join(app.root_path,'flsite.db')))


# import blueprint admin
from admin.admin import admin
# регистрация модуля
app.register_blueprint(admin, url_prefix='/admin')

menu = [{"name": "Главная", "url": "/"},
        {"name": "О сайте", "url": "about"},
        {"name": "Обратная связь", "url": "contact"}]


# у 1 обработчика может быть несколько роутов
@app.route("/index")
@app.route("/")
def index():
    # рендер(шаблон, данные)
    return render_template('index.html', menu=dbase.getMenu(), posts=dbase.getPostsAnounce())


@app.route("/about")
def about():
    print(request)
    print(session)
    return render_template('about.html', title = "О сайте", menu=menu)


# обработчик формы контактов с валидацией и мгновенными сообщениями
@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == 'POST':
        print(request.form['username'])

        if len(request.form['username']) > 2:
            flash('Сообщение отправлено', category='success')
        else:
            flash('Ошибка отправки', category='error')

    return render_template('contact.html', title = "Контакты", menu=menu)


# ===== CRUD OPERATIONS ========================================================

# Create
@app.route('/add_post', methods = ['GET', 'POST'])
def addPost():

    if request.method == 'POST':
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase.addPost(request.form['name'], request.form['url'], request.form['post'])
            if not res:
                flash('Ошибка добавления статьи', category='error')
            else:
                flash('Статья успешно добавлена', category='success')
        else:
            flash('Ошибка добавления статьи', category='error')
    return render_template('add_post.html', menu = dbase.getMenu(), title = 'Добавления статьи')


# Retriev
# функция принимает id_post из url
@app.route('/post/<alias>')
@login_required
def showPost(alias):
    title, post = dbase.getPost(alias)
    if not title:
        abort(404)
    return render_template('post.html', menu=dbase.getMenu(), title=title, post=post)




# =========================================================================================================================
# БД 
# =========================================================================================================================

# установления соединения с БД
def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


# Соединение с БД, если оно еще не установлено
def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


# создание таблиц БД без запуска сервера(нужно вызвать эту функцию в консоли)
def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()



# =========================================================================================================================
# ДЕКОРАТОРЫ
# =========================================================================================================================

# декоратор до обработки запроса
dbase = None
@app.before_request
def before_request():
    """Установление соединения с БД перед выполнением запроса"""
    global dbase
    db = get_db()
    dbase = FDataBase(db)


# Закрываем соединение с БД, если оно было установлено
# вызывается в момент уничтожения контекста приложения(в момент завершения обработки запроса)
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


# ошибка 404
# декоратор указывает какой код ошибки он обрабатывает
@app.errorhandler(404)
def pageNotFount(error):
    return render_template('page404.html', title="Страница не найдена", menu=menu)



# ============================================================================================================================
# FLASK-LOGIN
# ============================================================================================================================
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

# LoginManager управляет процессом авторизации
login_manager = LoginManager(app)
# перенаправление на страницу логин, при попытке просмотра закрытого контента
login_manager.login_view = 'login'
# сообщения и категория сообщения при попытке просмотра закрытого контента
login_manager.login_message = 'Авторизуйтесь для доступа к закрытым страницам'
login_manager.login_message_category = 'success'

# load_user получает user_id из сессии(результат get_id класса UserLogin)
# load_user создает объект UserLogin при каждом запросе, если пользователь авторизован
# функция декоратора user_loader вызывается после функции декоратора before_query 
@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id, dbase)


# обработчик авторизации пользователя 
# создается объект класса UserLogin и передается функции login_user из модуля Flask-Login
# функция заносит в сессию информацию о зарегистрированном пользователе
# сессионная информация будет присутствовать во всех запросах к серверу
@app.route("/login", methods=["POST", "GET"])
def login():
    # если пользователь авторизован - вернет профиль
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    # иначе процедура авторизации
    if request.method == "POST":
        user = dbase.getUserByEmail(request.form['email'])
        print(request.form['email'])
        if user and check_password_hash(user['psw'], request.form['psw']):
            userlogin = UserLogin().create(user)
            rm = True if request.form.get('remainme') else False
            # remember - запоминает пользователя, если стоит галочка запомнить
            login_user(userlogin, remember=rm)
            # редирект на некст если есть или профиль
            return redirect(request.args.get("next") or url_for("profile"))
 
        flash("Неверная пара логин/пароль", "error")
 
    return render_template("login.html", menu=dbase.getMenu(), title="Авторизация")


# Регистрация
@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        session.pop('_flashes', None)
        if len(request.form['name']) > 4 and len(request.form['email']) > 4 \
            and len(request.form['psw']) > 4 and request.form['psw'] == request.form['psw2']:
            hash = generate_password_hash(request.form['psw'])
            res = dbase.addUser(request.form['name'], request.form['email'], hash)
            if res:
                flash("Вы успешно зарегистрированы", "success")
                return redirect(url_for('login'))
            else:
                flash("Ошибка при добавлении в БД", "error")
        else:
            flash("Неверно заполнены поля", "error")
 
    return render_template("register.html", menu=dbase.getMenu(), title="Регистрация")



# страница профиля пользователя
@app.route('/profile')
@login_required
def profile():
    return f"""<a href="{url_for('logout')}">Выйти из профиля</a>
                user info: {current_user.get_id()}"""


# logout_user() из flask_login.py удаляет данные из сессии
# далее редирект на логин
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('login'))



# =========================================================================================================================
# ЗАПУСК приложения с debug=True на локальной машине 
# =========================================================================================================================

if __name__ == "__main__":
   app.run(debug=True)




