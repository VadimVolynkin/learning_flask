# pipenv install flask-login

# ============================================================================================================================
# app.py
# ============================================================================================================================

from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

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



# обработчик запроса целевой страницы
# декоратор login_required требует авторизации
@app.route("/post/<alias>")
@login_required
def showPost(alias):
    print("Только авторизированные пользователи могут видеть это")


# =========================================================================================================================
# UserLogin 
# =========================================================================================================================
# класс описывает состояние текущего пользователя: статус авторизации, активности и способ определения уникального идентификатора

class UserLogin:

    # используется при создании объекта UserLogin() в декораторе user_loader
    # по user_id загружает пользовательские данные из БД и сохраняет в __user
    def fromDB(self, user_id, db):
        self.__user = db.getUser(user_id)
        return self
 
    # используется при создании объекта в момент авторизации пользователя
    # сохраняет информацию о user в self.__user - это нужно в методе get_id для получения id текущего пользователя 
    def create(self, user):
        self.__user = user
        return self
 
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return str(self.__user['id'])


# =========================================================================================================================
# FDataBase
# =========================================================================================================================

# добавление нового пользователя
def addUser(self, name, email, hpsw):
    try:
        # проверка наличия пользователя с таким email
        self.__cur.execute(f"SELECT COUNT() as `count` FROM users WHERE email LIKE '{email}'")
        res = self.__cur.fetchone()
        if res['count'] > 0:
            print("Пользователь с таким email уже существует")
            return False

        # сохранение пользователя в базе
        tm = math.floor(time.time())
        self.__cur.execute("INSERT INTO users VALUES(NULL, ?, ?, ?, ?)", (name, email, hpsw, tm))
        self.__db.commit()
    except sqlite3.Error as e:
        print("Ошибка добавления пользователя в БД "+str(e))
        return False

    return True


# метод получает информацию о юзере по user_id
def getUser(self, user_id):
    try:
        self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
        res = self.__cur.fetchone()
        if not res:
            print("Пользователь не найден")
            return False 

        return res
    except sqlite3.Error as e:
        print("Ошибка получения данных из БД "+str(e))

    return False


# метод получает информацию о юзере по email
def getUserByEmail(self, email):
    try:
        self.__cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
        res = self.__cur.fetchone()
        if not res:
            print("Пользователь не найден")
            return False 

        return res
    except sqlite3.Error as e:
        print("Ошибка получения данных из БД "+str(e))

    return False







