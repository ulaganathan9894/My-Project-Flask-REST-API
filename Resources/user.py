from flask_restful import Resource, reqparse
from Models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import jwt_required, jwt_refresh_token_required, create_access_token, create_refresh_token, get_raw_jwt, get_jwt_identity

from blacklist import BLACKLIST

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                          type = str,
                          required = True,
                          help = 'this field cannot be blank'
                          )
_user_parser.add_argument('password',
                          type = str,
                          required = True,
                          help = 'Please atleast 8 characters letters must be mentioned'
                          )

class Register(Resource):
    def post(self):
        request_data = _user_parser.parse_args()
        if UserModel.findusername(request_data['username']):
            return {'Message' : 'A user with that username already exist'}, 400

        user = UserModel(**request_data)
        user.savestorage()
        return {"Message" : "Userid was successfully created"}, 201

class UserCheck(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.findid(user_id)
        if not user:
            return {'Message' : 'User not found'}, 404
        return user.json()
    
    @classmethod
    def delete(cls, user_id):
        user = UserModel.findid(user_id)
        if not user:
            return {'Message' : 'User not found'}, 404
        user.deletestorage()

class Login(Resource):
    @classmethod
    def post(cls):
        request_data = _user_parser.parse_args()
        user = UserModel.findusername(request_data['username'])
        if user and safe_str_cmp(user.password, request_data['password']):
            accesstoken = create_access_token(identity = user.id, fresh = True)
            refreshtoken = create_refresh_token(user.id)
            return {'access token' :accesstoken, 'refresh token' : refreshtoken}, 200
        return {'Message' : 'Invalid credential'}, 401


class Logout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {"Message" : "Successfully Logout."}, 200

class TokenRef(Resource):
    @jwt_refresh_token_required
    def post(self):
        currentuser = get_jwt_identity()
        newtoken = create_access_token(identity = currentuser, fresh = False)
        return {'access token' : newtoken}, 200
        pass
