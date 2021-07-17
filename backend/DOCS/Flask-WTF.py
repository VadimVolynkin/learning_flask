# pipenv install flask_wtf 
# pipenv install email-validator 
# https://wtforms.readthedocs.io/en/2.3.x/

# ============================================================================================================================
# Flask-WTF
# ============================================================================================================================
# генерирует формы
# валидирует формы
# наполнять начальной информацией
# работает с reCaptcha
# защита от CSRF


# ===== поля форм
StringField       # для работы с полем ввода
PasswordField     # для работы с полем ввода пароля
BooleanField      # для checkbox полей
TextAreaField     # для работы с вводом текста
SelectField       # для работы со списком
SubmitField       # для кнопки submit



# ===== валидаторы
DataRequired      # валидатор, требующий ввода каких-либо данных
Email             # проверяет корректность введенного email-адреса
Length            # проверяет количество введенных символов 


# ============================================================================================================================
# forms.py
# ============================================================================================================================


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length
 
class LoginForm(FlaskForm):
    email = StringField("Email: ", validators=[Email()])
    psw = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=4, max=100)])
    remember = BooleanField("Запомнить", default = False)
    submit = SubmitField("Войти")





from forms import LoginForm

@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    return render_template("login.html", menu=dbase.getMenu(), title="Авторизация", form=form)




# form.hidden_tag() - скрытое поле с токеном от CSRF-атак
# form - доступ к переменным класса LoginForm
{% extends 'base.html' %}
 
{% block content %}
{{ super() }}
{% for cat, msg in get_flashed_messages(True) %}
<div class="flash {{cat}}">{{msg}}</div>
{% endfor %}
<form action="" method="post" class="form-contact">
{{ form.hidden_tag() }}
{{ form.email.label() }} {{ form.email() }}
{{ form.psw.label() }} {{ form.psw() }}
{{ form.remember.label() }} {{ form.remember() }}
{{ form.submit() }}
<hr align=left width="300px">
<a href="{{url_for('register')}}">Регистрация</a>
</form>
{% endblock %}


# form.validate_on_submit() - проверка переданных данных
@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
 
    form = LoginForm()
    if form.validate_on_submit():
        user = dbase.getUserByEmail(form.email.data)
        if user and check_password_hash(user['psw'], form.psw.data):
            userlogin = UserLogin().create(user)
            rm = form.remember.data
            login_user(userlogin, remember=rm)
            return redirect(request.args.get("next") or url_for("profile"))
 
        flash("Неверная пара логин/пароль", "error")
 
    return render_template("login.html", menu=dbase.getMenu(), title="Авторизация", form=form)















