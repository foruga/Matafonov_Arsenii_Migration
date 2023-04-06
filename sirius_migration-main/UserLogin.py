class UserLogin:

    def FromDB(self, id, db):
        self.__user = db.getUser(id)

    def create(self, user):
        self.__user = user

    def get_id(self):
        return str(self.__user['id'])

    def is_loginned(self):
        return True
        
