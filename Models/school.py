from alchemydb import storage

class SchoolModel(storage.Model):
    __tablename__ = 'schools'
    id = storage.Column(storage.Integer, primary_key = True)
    name = storage.Column(storage.String(100))

    students = storage.relationship('StudentModel', lazy = 'dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'id' : self.id, 'name' : self.name,'students' : [student.json() for student in self.students.all()]}

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


    


        

        
        
