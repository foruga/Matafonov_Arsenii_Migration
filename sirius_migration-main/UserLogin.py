class UserLogin:
    def fromDB(self, id, db):
        self.__user = db.getUser(id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def get_id(self):
        return str(self.__user['id'])

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def is_loginned(self):
        return True
        
