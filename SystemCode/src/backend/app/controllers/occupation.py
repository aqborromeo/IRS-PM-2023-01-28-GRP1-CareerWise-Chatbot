from flask import current_app, jsonify, Response, request
from flask_restful import Resource
from sqlalchemy import or_
from sqlalchemy.orm import aliased
from sqlalchemy.sql.expression import select, union_all, literal_column

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


def map_programs(cip_occupations):
    programs_dict = {}
    programs = []
    if cip_occupations:
        for cip_occupation in cip_occupations:
            for cip_program in cip_occupation.cip.cip_programs:
                program = cip_program.program
                if str(program.id) not in programs_dict:
                    programs_dict[str(program.id)] = 1
                    program_dict = map_row(program)
                    program_dict['programTrends'] = list(map(
                        map_row, program.program_trends))
                    programs.append(program_dict)
    return programs


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
        graph_fetcher = CareerPathGraphFetcher(id, CareerPath, Occupation)
        career_paths = graph_fetcher.get_graph()
        career_paths_dict = list(map(map_career_path, career_paths))
        occupation_dict["careerPaths"] = career_paths_dict

        # SSOC Jobs
        ssoc_jobs = db.session.query(SsocJob).filter(
            SsocJob.occupation_id == id).all()
        ssoc_jobs_dict = list(map(map_row, ssoc_jobs))
        occupation_dict["ssocJobs"] = ssoc_jobs_dict

        # Educational Programs
        programs = map_programs(occupation.cip_occupations)
        occupation_dict["programs"] = programs

        return jsonify(occupation_dict)


class CareerPathGraphFetcher():
    def __init__(self, start_id, graph_model, node_model):
        self.start_id = start_id
        self.graph_model = graph_model
        self.node_model = node_model

    def get_graph(self):
        start_node = self.start_id

        # get children of start node
        hierarchy = db.session.query(
            self.graph_model)\
            .filter(self.graph_model.source_id == start_node)\
            .cte(name="hierarchy", recursive=True)

        parent = aliased(hierarchy, name="p")
        children = aliased(self.graph_model, name="c")
        hierarchy = hierarchy.union_all(
            db.session.query(children)
            .filter(children.source_id == parent.c.target_id))

        graph_alias = aliased(self.graph_model, hierarchy)

        # get parents of start node
        lower_hierarchy = db.session.query(self.graph_model).filter(
            self.graph_model.target_id == start_node)

        result = db.session.query(graph_alias).union_all(lower_hierarchy).all()
        return result
