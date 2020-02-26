from flask_restful import Resource
from Models.school import SchoolModel

class School(Resource):
    def get(self, name):
        school = SchoolModel.findname(name)
        if school:
            return school.json()
        return {"Message" : "School Not Found"}, 404

    def post(self, name):
        if SchoolModel.findname(name):
            return {'Message' : 'School name {} already exists.'.format(name)}, 400
        school = SchoolModel(name)
        try:
            school.savestorage()
        except:
            return {'Message' : 'An error occured while creating school name'}

    def delete(self, name):
        school = SchoolModel.findname(name)
        if school:
            school = SchoolModel.deletestorage()
        return {'Message' : 'Store deleted'}

class SchoolList(Resource):
    def get(self):
        return {'schools' : [school.json() for school in SchoolModel.findall()]}

    
