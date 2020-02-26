from alchemydb import storage

class UserModel(storage.Model):
    __tablename__ = 'users'

    id = storage.Column(storage.Integer, primary_key = True)
    username = storage.Column(storage.String(100))
    password = storage.Column(storage.String(100))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def json(self):
        return {'id' : self.id, 'username' : self.username}
    
    @classmethod
    def findusername(cls, username):
        return cls.query.filter_by(username = username).first()
    
    @classmethod
    def findid(cls, _id_):
        return cls.query.filter_by(id = _id_).first()

    def savestorage(self):
        storage.session.add(self)
        storage.session.commit()

    def deletestorage(self):
        storage.session.delete(self)
        storage.session.commit()


