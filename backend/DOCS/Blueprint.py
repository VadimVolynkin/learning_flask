

# ============================================================================================================================
# admin.py
# ============================================================================================================================

from flask import Blueprint


admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

'admin'          # имя Blueprint, которое будет суффиксом ко всем именам методов, данного модуля
__name__         # имя исполняемого модуля, относительно которого будет искаться папка admin и соответствующие подкаталоги
template_folder  # подкаталог для шаблонов этого Blueprint(по умолчанию берется подкаталог шаблонов приложения)
static_folder    # подкаталог для статических файлов (по умолчанию берется подкаталог static приложения) 


@admin.route('/')
def index():
    return "admin"

# создание в сессии запись - админ авторизован
def login_admin():
    session['admin_logged'] = 1

# проверка адмна на авторизацию
def isLogged():
    return True if session.get('admin_logged') else False
 
# выход из авторизации - стирает запись в сессии
def logout_admin():
    session.pop('admin_logged', None)


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


# АВТОРИЗАЦИЯ
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



# ЛОГАУТ
@admin.route('/logout', methods=["POST", "GET"])
def logout():
    if not isLogged():
        return redirect(url_for('.login'))
 
    logout_admin()
 
    return redirect(url_for('.login'))



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









