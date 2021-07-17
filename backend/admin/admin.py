from flask import Blueprint, session, redirect, url_for, request, render_template


admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

# 'admin'          # имя Blueprint, которое будет суффиксом ко всем именам методов, данного модуля
# __name__         # имя исполняемого модуля, относительно которого будет искаться папка admin и соответствующие подкаталоги
# template_folder  # подкаталог для шаблонов этого Blueprint(по умолчанию берется подкаталог шаблонов приложения)
# static_folder    # подкаталог для статических файлов (по умолчанию берется подкаталог static приложения) 


# @admin.route('/')
# def index():
#     return "admin"

@admin.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        if request.form['user'] == "admin" and request.form['psw'] == "12345":
            login_admin()
            return redirect(url_for('.index'))
        else:
            flash("Неверная пара логин/пароль", "error")
 
    return render_template('admin/login.html', title='Админ-панель')

# создание в сессии запись - админ авторизован
def login_admin():
    session['admin_logged'] = 1

# проверка адмна на авторизацию
def isLogged():
    return True if session.get('admin_logged') else False
 
# выход из авторизации - стирает запись в сессии
def logout_admin():
    session.pop('admin_logged', None)

# обработчик логаута
@admin.route('/logout', methods=["POST", "GET"])
def logout():
    if not isLogged():
        return redirect(url_for('.login'))
 
    logout_admin()
 
    return redirect(url_for('.login'))


menu = [{'url': '.index', 'title': 'Панель'},
        {'url': '.logout', 'title': 'Выйти'}]

# главная админ-панели
@admin.route('/')
def index():
    if not isLogged():
        return redirect(url_for('.login'))
 
    return render_template('admin/index.html', menu=menu, title='Админ-панель')





