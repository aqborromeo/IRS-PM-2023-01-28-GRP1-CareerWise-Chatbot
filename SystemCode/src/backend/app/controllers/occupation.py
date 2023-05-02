from flask import current_app, jsonify, Response, request
from flask_restful import Resource
from sqlalchemy import or_

from app.models.occupation import Occupation
from app.models.career_path import CareerPath
from app.models.ssoc_job import SsocJob
from app.models.chat import Chat, CreatedBy
from app.models.user import User

from app.middlewares.auth import Auth

from app.utils.common import map_row

from app.db import db


auth = Auth()


def map_career_path(career_path):
    return map_row(career_path) | {
        'source': map_row(career_path.source),
        'target': map_row(career_path.target)
    }


class OccupationsApi(Resource):
    @auth.middleware
    def get(token_data, self):
        occupations = db.session.query(Occupation).first(10)
        occupations_dict = map(map_row, occupations)
        return jsonify(occupations_dict)


class OccupationApi(Resource):
    @auth.middleware
    def get(token_data, self, id):
        occupation = db.session.query(Occupation).filter_by(
            id=id).first()
        occupation_dict = map_row(occupation)

        # Career paths
        career_paths = db.session.query(CareerPath).filter(
            or_(CareerPath.source_id == id, CareerPath.target_id == id)).all()
        career_paths_dict = list(map(map_career_path, career_paths))
        occupation_dict["careerPaths"] = career_paths_dict

        # SSOC Jobs
        ssoc_jobs = db.session.query(SsocJob).filter(
            SsocJob.occupation_id == id).all()
        ssoc_jobs_dict = list(map(map_row, ssoc_jobs))
        occupation_dict["ssocJobs"] = ssoc_jobs_dict

        return jsonify(occupation_dict)
