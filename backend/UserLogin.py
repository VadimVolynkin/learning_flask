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
