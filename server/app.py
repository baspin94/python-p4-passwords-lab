#!/usr/bin/env python3

from flask import request, session, make_response
from flask_restful import Resource

from config import app, db, api
from models import User

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

class Signup(Resource):
    def post(self):
        data = request.get_json()
        new_user = User(
            username = data['username']
        )
        new_user.password_hash = data['password']
        db.session.add(new_user)
        db.session.commit()

        response = make_response(
            new_user.to_dict(),
            201
        )

        return response

class CheckSession(Resource):
    def get(self):
        user_cookie = session.get('user_id')
        user = User.query.filter(User.id == user_cookie).first()
        if user:
            response = make_response(
                user.to_dict(), 
                200
            )
            return response
        response = make_response(
            {}, 
            204
        )
        return response

class Login(Resource):
    def post(self):
        username = request.get_json()['username']
        password = request.get_json()['password']

        user = User.query.filter(User.username == username).first()

        if user.authenticate(password):
            session['user_id'] = user.id
            response = make_response(
                user.to_dict(),
                200
            )
            return response
        
        error = {"error": "Invalid username or password."}
        
        response = make_response(
            error, 
            401
        )
        return response

class Logout(Resource):
    def delete(self):
        session['user_id'] = None

        response = make_response(
            {},
            204
        )
        return response

api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup')
api.add_resource(CheckSession, '/check_session')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
