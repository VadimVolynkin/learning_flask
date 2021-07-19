
# ============================================================================================================================
# admin.py
# ============================================================================================================================

from flask import Blueprint, session, redirect, url_for, request, render_template, g


admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

'admin'          # имя Blueprint, которое будет суффиксом ко всем именам методов, данного модуля
__name__         # имя исполняемого модуля, относительно которого будет искаться папка admin и соответствующие подкаталоги
template_folder  # подкаталог для шаблонов этого Blueprint(по умолчанию берется подкаталог шаблонов приложения)
static_folder    # подкаталог для статических файлов (по умолчанию берется подкаталог static приложения) 

# создание в сессии запись - админ авторизован
def login_admin():
    session['admin_logged'] = 1

# проверка адмна на авторизацию
def isLogged():
    return True if session.get('admin_logged') else False
 
# выход из авторизации - стирает запись в сессии
def logout_admin():
    session.pop('admin_logged', None)


# обработчик логин
# url_for('.index') указывает на index в текущем Blueprint
# url_for('admin.index’) - это более конкретный вариант записи. Здесь admin – это имя Blueprint, а не название файла admin.py.
@admin.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        if request.form['user'] == "admin" and request.form['psw'] == "12345":
            login_admin()
            return redirect(url_for('.index'))
        else:
            flash("Неверная пара логин/пароль", "error")
 
    return render_template('admin/login.html', title='Админ-панель')


# обработчик логаута
@admin.route('/logout', methods=["POST", "GET"])
def logout():
    if not isLogged():
        return redirect(url_for('.login'))
 
    logout_admin()
 
    return redirect(url_for('.login'))


menu = [{'url': '.index', 'title': 'Панель'},
        {'url': '.listusers', 'title': 'Список пользователей'},
        {'url': '.listpubs', 'title': 'Список статей'},
        {'url': '.logout', 'title': 'Выйти'}]


# главная админ-панели
@admin.route('/')
def index():
    if not isLogged():
        return redirect(url_for('.login'))
 
    return render_template('admin/index.html', menu=menu, title='Админ-панель')


# вывод статей в панели администратора
@admin.route('/list-pubs')
def listpubs():
    # если пользователь не авторизован - редирек на логинпейдж
    if not isLogged():
        return redirect(url_for('.login'))
 
    # если есть соединение - получаем статьи из БД - рендерим
    list = []
    if db:
        try:
            cur = db.cursor()
            cur.execute(f"SELECT title, text, url FROM posts")
            list = cur.fetchall()
        except sqlite3.Error as e:
            print("Ошибка получения статей из БД " + str(e))
 
    return render_template('admin/listpubs.html', title='Список статей', menu=menu, list=list)


# вывод списка пользователей в админпанели 
@admin.route('/list-users')
def listusers():
    if not isLogged():
        return redirect(url_for('.login'))
 
    list = []
    if db:
        try:
            cur = db.cursor()
            cur.execute(f"SELECT name, email FROM users ORDER BY time DESC")
            list = cur.fetchall()
        except sqlite3.Error as e:
            print("Ошибка получения статей из БД " + str(e))
 
    return render_template('admin/listusers.html', title='Список пользователей', menu=menu, list=list)


# ============================================================================================================================
# БД
# ============================================================================================================================

# установдение связи с БД - берем значение link_db из g-переменной контекста приложения
db = None
@admin.before_request
def before_request():
    """Установление соединения с БД перед выполнением запроса"""
    global db
    db = g.get('link_db')
 
# закрытие соединения
@admin.teardown_request
def teardown_request(request):
    global db
    db = None
    return request


# декораторы уровня приложения как бы «обертывают» выполнение декораторов в Blueprint
@app.before_request
@admin.before_request
@admin.teardown_request
@app.teardown_appcontext 


# ============================================================================================================================
# app.py
# ============================================================================================================================

from admin.admin import admin

# регистрация модуля
app.register_blueprint(admin, url_prefix='/admin')

admin           # ссылка на созданный Blueprint
url_prefix      # префикс для всех URL модуля admin. Без него все URL внутри Blueprint будут записываться после домена сайта. 

http://127.0.0.1:5000/admin/ 
домен/<url_prefix>/<URL-blueprint> 


# ============================================================================================================================
# admin/templates/admin/base_admin.html
# ============================================================================================================================

# url_for('.static', filename='css/styles.css') - сформирует путь admin/static/css/styles.css
<!DOCTYPE html>
<html>
<head>
<link type="text/css" href="{{ url_for('.static', filename='css/styles.css')}}" rel="stylesheet" />
<title>{{ title }}</title>
</head>
<body>
{% if menu -%}
         <ul class="mainmenu">
         {% for p in menu %}
         <li><a href="{{ url_for(p.url) }}">{{p.title}}</a></li>
         {% endfor %}
         </ul>
         <div class="clear"></div>
{%- endif -%}
<div class="content">
{% block content -%}
{% endblock %}
</div>
</body>
</html>

# ============================================================================================================================
# admin/templates/admin/login.html
# ============================================================================================================================

{% extends 'admin/base_admin.html' %}
 
{% block content %}
{{ super() }}
<div id="login" class="wnd_dlg_back login_wnd">
<div class="login">
         <p class="title">Админ-панель</p>
{% for cat, msg in get_flashed_messages(True) %}
<div class="flash {{cat}}">{{msg}}</div>
{% endfor %}
         <form action="" method="post">
                   <label class="form-label">Логин: </label><input type="text" name="user" />
                   <label class="form-label">Пароль: </label><input type="password" name="psw" />
                   <p align="center"><input class="login_button" type="submit" value="Войти">
         </form>
</div>
</div>
{% endblock %}


# ============================================================================================================================
# admin/templates/admin/index.html
# ============================================================================================================================

{% extends 'admin/base_admin.html' %}
 
{% block content %}
{{ super() }}
{% endblock %}



# ============================================================================================================================
# templates/base.html
# ============================================================================================================================

# маршрут указывает на шаблон в blueprint
<a href="{{ url_for('admin.index') }}">Админ-панель</a></p>



