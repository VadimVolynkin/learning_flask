from flask import Flask, render_template, url_for, request, flash, session, abort
# render_template                    - рендер
# url_for(endpoint, **values)        - генерирует URL-адрес по имени функции-обработчика
# request                            - объект данных текущего запроса
# session                            - объект сессии
# flash                              - мгновенные сообщения
# abort                              - функция для вызова ошибки внутри обработчика

# создаем экземпляр приложения
# __name__ = имя текушего файла = имя приложения
app = Flask(__name__)

# секретный ключ для генерации сессий и токенов
app.config['SECRET_KEY'] = 'fdgdfgdfggf786hfg6hfg6h7f'

# ===== СТРАНИЦЫ ПРИЛОЖЕНИЯ ===============================================================================================

menu = [{"name": "Главная", "url": "/"},
        {"name": "О сайте", "url": "about"},
        {"name": "Обратная связь", "url": "contact"}]


# у 1 обработчика может быть несколько роутов
@app.route("/index")
@app.route("/")
def index():
    print(url_for('index'))
    # рендер(шаблон, данные)
    return render_template('index.html', title="Про Flask", menu=menu)


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


# ошибка 404
# декоратор указывает какой код ошибки он обрабатывает
@app.errorhandler(404)
def pageNotFount(error):
    return render_template('page404.html', title="Страница не найдена", menu=menu)


# страница логина
@app.route("/login", methods=["POST", "GET"])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.form['username'] == "selfedu" and request.form['psw'] == "123":
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))
 
    return render_template('login.html', title="Авторизация", menu=menu)


# страница профиля пользователя
# abort 401, если в сессии нет ключа 'userLogged'
@app.route("/profile/<username>")
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
 
    return f"Пользователь: {username}"

    
# ===== ЗАПУСК приложения с debug=True на локальной машине ================================================================

if __name__ == "__main__":
   app.run(debug=True)









