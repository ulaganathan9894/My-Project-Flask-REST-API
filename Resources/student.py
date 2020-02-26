from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims, jwt_optional, get_jwt_identity
from Models.student import StudentModel

class Student(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('age',
                        type = int,
                        required = True,
                        help = 'the field cannot be left!'
                        )
    parser.add_argument('gender',
                        type = str,
                        required = True,
                        help = 'the field cannot be left!'
                        )
    parser.add_argument('school_id',
                        type = int,
                        required = True,
                        help = 'Every Student need a School_id card'
                        )
    def get(self, name):
        student = StudentModel.findname(name)
        if student:
            return student.json()
        return {"Message" : "Student name not found"}, 404

    def post(self, name):
        if StudentModel.findname(name):    
            return{'Message':'the item {} is already exist.' .format(name)}, 400
        request_data = Student.parser.parse_args()
        student = StudentModel(name, **request_data)
        try:
            student.savestorage()
        except:
            return {"Message" : "An error occured inserting the item."}, 500
        return student.json(), 201
            

    def put(self, name):
        request_data = Student.parser.parse_args()
        student = StudentModel.findname(name)
        if student is None:
            student = StudentModel(name, **request_data)
        else:
            student.age = request_data['age']
            student.gender = request_data['gender']
        student.savestorage()

        return student.json()
    
    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {"Message" : "School Admin Privilege Required"}, 404
        student = StudentModel.findname(name)
        if student:
            student.deletestorage()
        return {"Message" : "One student list successfully deleted"}     

class StudentList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        students = [student.json() for student in StudentModel.findall()]
        if user_id:
            return {'students' : students}, 200
        return {'students' : [student['name'] for student in students], 'Message' : 'Do you see More data available if you login'}, 200
        
