from flask import Flask, request, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from Resources.school import School, SchoolList
from Resources.student import Student, StudentList
from Resources.user import Register, UserCheck, Login, Logout, TokenRef
from blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.secret_key = 'ISRAEL'
api = Api(app)

@app.before_first_request
def createtables():
    storage.create_all()

jwt = JWTManager(app)

@jwt.user_claims_loader
def claimstojwt(identity):
    if identity == 1:
        return {'is_admin' : True}
    return {'is_admin' : False}

@jwt.token_in_blacklist_loader
def checkblacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST

@jwt.expired_token_loader
def expiredtoken():
    return jsonify({"Description" : "Token has expired", "Error" : "token_expired"})

@jwt.invalid_token_loader
def invalidtoken(error):
    return jsonify({"Description" : "Signified Verification Failed", "Error" : "invalid_token"})

@jwt.unauthorized_loader
def missingtoken(error):
    return jsonify ({"Description" : "request does not contain an access token.", "Error" : "Authorizaton_required"}), 401

@jwt.needs_fresh_token_loader
def tokennotfresh():
    return jsonify ({"Description" : "the token is not fresh.", "Error" : "Fresh_token required"})

@jwt.revoked_token_loader
def revokedtoken():
    return jsonify ({"Description" : "the token has been revoked.", "Error" : "Token Revoked"}), 401

api.add_resource(School, '/school/<string:name>')
api.add_resource(Student, '/student/<string:name>')
api.add_resource(StudentList, '/students')
api.add_resource(SchoolList, '/schools')
api.add_resource(Register, '/register')
api.add_resource(UserCheck, '/user/<int:user_id>')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(TokenRef, '/refresh')

if __name__ == '__main__':
    from alchemydb import storage
    storage.init_app(app)
    app.run(port = 5000, debug = True)
    

