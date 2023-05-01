from flask import current_app, Response, jsonify, request, make_response
from flask_restful import Resource
from flask_pydantic import validate

from datetime import datetime, timedelta

import jwt
import bcrypt

from app.middlewares.auth import Auth

from app.models.user import User
from app.models.chat import Chat
from app.models.chat_session import ChatSession


from app.db import db

auth = Auth()


class TokenApi(Resource):
    def createToken(self, user):
        JWT_SECRETKEY = current_app.config.get('JWT_SECRETKEY')
        token = jwt.encode(
            payload={
                'userId': user.id,
                'username': user.username,
                'exp': datetime.utcnow() + timedelta(minutes=30)
            },
            key=JWT_SECRETKEY, algorithm='HS256')
        return token

    def setCookie(self, token):
        successLogin = {'status': True, 'msg': 'Login Success'}
        response = Response(successLogin)
        response.set_cookie('x-auth-token', token)
        return response


class LoginApi(Resource):
    @validate()
    def post(self):
        user = None
        try:
            user = UserHandler().findUser()
        except LoginError as msg:
            raise LoginError()
        except Exception as msg:
            raise LoginError()

        try:
            token_api = TokenApi()
            token = token_api.createToken(user)
            token_api.setCookie(token)
            return {"token": token}
        except:
            raise AccessTokenError()


class RegisterApi(Resource):
    @validate()
    def post(self):
        try:
            user = UserHandler().insertNewData()
            if not user:
                raise RegisterError()
            token_api = TokenApi()
            token = token_api.createToken(user)
            token_api.setCookie(token)
            return {"token": token}
        except:
            raise RegisterError()


class LogoutApi(Resource):
    def post(self):
        resp = Response({"success": True})
        resp.delete_cookie('x-auth-token')
        return resp


class UserApi(Resource):
    @auth.middleware
    @validate()
    def get(token_data, self):
        user = DataHandler().getUser({'id': token_data['userId']})

        if not user.last_chat_session_id:
            last_chat = db.session.query(Chat).filter_by(
                user_id=token_data['userId']).order_by(Chat.updated_at.desc()).first()
            last_chat_session = None
            if not last_chat:
                last_chat_session = db.session.query(ChatSession).filter_by(
                    user_id=token_data['userId']).order_by(ChatSession.updated_at.desc()).first()
            user.last_chat_session_id = last_chat.chat_session_id if last_chat else (
                last_chat_session.id if last_chat_session else None)
            db.session.commit()
            db.session.refresh(user)

        return jsonify({
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'lastChatSessionId': user.last_chat_session_id,
        })


class UserHandler:
    def insertNewData(self):
        try:
            parameter = {
                'username': request.json.get('username'),
                'email': request.json.get('email'),
                'password': bcrypt.hashpw(
                    request.json.get('password').encode('utf-8'),
                    bcrypt.gensalt()).decode('utf-8'),
            }
            data = DataHandler().insertNewData(parameter)
            return data
        except Exception as e:
            print(e)

    def findUser(self):
        parameter = {
            'email': request.json.get('email').lower(),
        }
        user = DataHandler().getUser(parameter)
        if not user:
            raise LoginError('User is not found')
        if bcrypt.checkpw(
            request.json.get('password').encode('utf-8'),
            user.password.encode('utf-8')
        ):
            return user
        raise LoginError()


class DataHandler:

    def getUser(self, parameter):
        data = db.session.query(User).filter_by(**parameter).first()
        return data

    def insertNewData(self, parameter):
        object_to_insert = User(**parameter)

        db.session.add(object_to_insert)
        db.session.commit()
        db.session.refresh(object_to_insert)

        return object_to_insert


class LoginError(Exception):
    """Login error"""


class RegisterError(Exception):
    """Error"""


class InsertUserError(Exception):
    """Error"""


class UserNotFoundError(Exception):
    """Error"""


class AccessTokenError(Exception):
    """Error"""
