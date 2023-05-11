from flask import current_app, jsonify, Response, request
from flask_restful import Resource

from app.models.chat_session import ChatSession, Status
from app.models.chat import Chat, CreatedBy
from app.models.user import User
from app.models.occupation import Occupation
from app.models.result import Result

from app.middlewares.auth import Auth

from ml.similarity import SimilarityCalculator
from app.utils.common import row2dict, rows2dict
from app.utils.common import map_row

from app.db import db

import re
import locale

auth = Auth()


def result_row_callback(result, row):
    return result | {
        'createdAt': result['createdAt'].strftime('%Y-%m-%dT%H:%M:%S%z'),
        'updatedAt': result['updatedAt'].strftime('%Y-%m-%dT%H:%M:%S%z'),
        'occupation': map_row(row.occupation)
    }


def map_result(result):
    result_dict = row2dict(result, snake_to_camel=True)
    return result_row_callback(result_dict, result) if result_dict else None


def map_results(results):
    return rows2dict(results, snake_to_camel=True, row_callback=result_row_callback)


def extract_number(text):
    numbers = re.findall(r'\d+[\.,]?\d*', text)
    if numbers:
        locale.setlocale(locale.LC_ALL, '')
        return locale.atof(numbers[0])
    else:
        return None


class ResultRatingApi(Resource):
    @auth.middleware
    def post(token_data, self, id, rating):
        result = self.db.session.merge(Result(id=id, user_rating=rating))
        return map_result(result)


class ResultApi(Resource):
    @auth.middleware
    def get(token_data, self, chat_session_id, id):
        result = db.session.query(Result).filter_by(
            id=id, chat_session_id=chat_session_id).first()

        return map_result(result)


class GenerateResultsApi(Resource):
    @auth.middleware
    def post(token_data, self, chat_session_id):
        chat_session = db.session.query(ChatSession).filter_by(
            id=chat_session_id, user_id=token_data['userId']).first()

        if not chat_session:
            raise MissingChatSessionError()

        if chat_session.status == Status.complete:
            results = db.session.query(Result).filter(
                Result.chat_session_id == chat_session_id).all()
            return map_results(results)

        # If no results, generate results
        generator = ResultsGenerator(token_data['userId'], chat_session)
        results = generator.generate()

        return map_results(results)


class ResultsGenerator:
    def __init__(self, user_id, chat_session):
        self.user_id = user_id
        self.chat_session = chat_session

    def get_qna_dict(self, chats):
        r = {}
        for i in range(len(chats)):
            chat = chats[i]
            if chat.created_by == CreatedBy.user and chat.question and chat.question.code:
                key = chat.question.code

                if key:
                    r[key] = chat
        return r

    def get_context_values(self, chats):
        context_groups = ['context', 'style']
        r = {}
        for i in range(len(chats)):
            chat = chats[i]
            if chat.created_by == CreatedBy.user and chat.question \
                    and chat.question.code and chat.question.group in context_groups:
                key = chat.question.code

                if key:
                    weights = chat.question.weights
                    # Handle MCQs
                    if chat.option:
                        for weight in weights:
                            r[weight.variable] = chat.option.parse_value() * \
                                weight.weight_value
        return r

    def generate(self):
        chats = self.chat_session.chats if self.chat_session else []

        if not chats:
            raise MissingChatSessionError()

        qna = self.get_qna_dict(chats)
        occupations = rows2dict(Occupation.query.all(), 'id')

        # Get interest text
        interest_input = qna['interest_open'].message_text if qna['interest_open'] else ''

        # Get experience text
        experience_input = qna['experience_open'].message_text if qna['experience_open'] else ''

        # Get context values
        context_input = self.get_context_values(chats)

        # Get salary text
        salary_input = qna['salary_minimum'].message_text if qna['salary_minimum'] else ''
        salary_input = extract_number(salary_input)

        # Calculate similarity score
        calculator = SimilarityCalculator(
            occupations, interest_input, experience_input, context_input, salary_input)

        recommendations = calculator.get_recommendation()

        # Save recommendations
        for each in Result.query.filter(Result.chat_session_id == self.chat_session.id, Result.occupation_id.in_(recommendations.keys())).all():
            # Only merge those results which already exist in the database
            update_item = recommendations.pop(each.occupation_id)
            db.session.merge(
                Result(**update_item, chat_session_id=self.chat_session.id, occupation_id=each.occupation_id))

        def map_result_values(key):
            value = recommendations[key]
            return Result(**value, chat_session_id=self.chat_session.id, occupation_id=key)

        # Only add those reesults which did not exist in the database
        insert_items = list(
            map(map_result_values, recommendations.keys()))
        db.session.add_all(insert_items)

        # Save session completed state
        self.chat_session.status = Status.complete
        db.session.commit()

        return db.session.query(Result).filter(Result.chat_session_id == self.chat_session.id).all()


class MissingChatSessionError(Exception):
    """Missing chat session error"""
