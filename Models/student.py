from alchemydb import storage

class StudentModel(storage.Model):
    __tablename__ = 'students'
    id  = storage.Column(storage.Integer, primary_key = True)
    name = storage.Column(storage.String(100))
    age = storage.Column(storage.Integer)
    gender = storage.Column(storage.String(15))

    school_id = storage.Column(storage.Integer, storage.ForeignKey('schools.id'))
    school = storage.relationship('SchoolModel')

    def __init__(self, name, age, gender, school_id):
        self.name = name
        self.age = age
        self.gender = gender
        self.school_id = school_id

    def json(self):
        return {'id' : self.id, 'name' : self.name, 'age' : self.age, 'gender' : self.gender, 'school_id' : self.school_id}

    @classmethod
    def findname(cls, name):
        return cls.query.filter_by(name = name).first()

    def savestorage(self):
        storage.session.add(self)
        storage.session.commit()

    def deletestorage(self):
        storage.session.delete(self)
        storage.session.commit()

    @classmethod    
    def findall(cls):
        return cls.query.all()
    
