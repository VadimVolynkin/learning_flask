import math, time, sqlite3

# класс создает переменную с курсором и использует ее в методе getMenu
# getMenu создает запрос и выполняет его - вернет результат или пустой список
class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getMenu(self):
        sql = '''SELECT * FROM mainmenu'''

        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print("Ошибка чтения из БД")
        return []


    def addPost(self, title, url, text):
        try:
            # проверка на совпадение url(должен быть уникальным)
            self.__cur.execute(f'SELECT COUNT() as `count` FROM posts WHERE url LIKE "{url}"')
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print('Статья с таким url уже существует')
                return False

            # запись новой статьи в БД
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO posts VALUES(NULL, ?, ?, ?, ?)", (title, text, url, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД " + str(e))
            return False
        return True

    def getPost(self, alias):
        try:
            self.__cur.execute(f'SELECT title, text FROM posts WHERE url LIKE "{alias}" LIMIT 1')
            res = self.__cur.fetchone()
            if res: return res
        except sqlite3.Error as e:
                print("Ошибка добавления статьи в БД " + str(e))
        return (False, False)

    def getPostsAnounce(self):
        try:
            self.__cur.execute('SELECT id, title, url, text FROM posts ORDER BY time DESC')
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
                print("Ошибка добавления статьи в БД " + str(e))
        return []

    
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
    



