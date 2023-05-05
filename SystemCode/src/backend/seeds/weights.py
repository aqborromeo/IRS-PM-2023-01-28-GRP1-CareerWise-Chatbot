from flask_seeder import Seeder

from app.models.question import Question
from app.models.weight import Weight
from app.utils.common import is_same_db_data


class WeightSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 3

    # run() will be called by Flask-Seeder
    def run(self):
        new_weights = {
            # Work Style
            "style_stress_tolerance": {
                # "style_self_control": {
                #     "weight_value": 0.77
                # },
                "style_stress_tolerance": {
                    "weight_value": 1.0
                }
            },
            "style_achievement_effort": {
                "style_achievement_effort": {
                    "weight_value": 1.0
                },
                # "style_persistence": {
                #     "weight_value": 0.84
                # },
                # "style_initiative": {
                #     "weight_value": 0.79
                # }
            },
            "style_social_orientation": {
                # "style_concern_for_others": {
                #     "weight_value": 0.83
                # },
                "style_social_orientation": {
                    "weight_value": 1.0
                }
            },
            "style_independence": {
                "style_independence": {
                    "weight_value": 1.0
                }
            },
            "style_innovation": {
                "style_innovation": {
                    "weight_value": 1.0
                }
            },

            # Work Context
            "context_duration_of_typical_work_week": {
                "context_duration_of_typical_work_week": {
                    "weight_value": 1.0
                }
            },
            "context_outdoors_exposed_to_weather": {
                "context_outdoors_exposed_to_weather": {
                    "weight_value": 1.0
                },
                # "context_outdoors_under_cover": {
                #     "weight_value": 0.85
                # },
                # "context_in_an_enclosed_vehicle_or_equipment": {
                #     "weight_value": 0.83
                # },
                # "context_very_hot_or_cold_temperatures": {
                #     "weight_value": 0.82
                # }
            },
            "context_r_spend_time_walking_and_running": {
                # "context_spend_time_sitting": {
                #     "weight_value": 0.84
                # },
                # "context_spend_time_standing": {
                #     "weight_value": 0.85
                # },
                "context_spend_time_walking_and_running": {
                    "weight_value": 1.0
                },
                # "context_spend_time_bending_or_twisting_the_body": {
                #     "weight_value": 0.79
                # }
            },
            "context_deal_with_unpleasant_or_angry_people": {
                "context_deal_with_unpleasant_or_angry_people": {
                    "weight_value": 1.0
                }
            },
            "context_exposed_to_hazardous_conditions": {
                # "context_exposed_to_contaminants": {
                #     "weight_value": 0.8
                # },
                "context_exposed_to_hazardous_conditions": {
                    "weight_value": 1.0
                },
                # "context_wear_common_protective_or_safety_equipment_such_as_safety_shoes_glasses_gloves_hearing_protection_hard_hats_or_life_jackets": {
                #     "weight_value": 0.79
                # }
            }
        }

        for question in Question.query.filter(Question.code.in_(new_weights.keys())).all():
            current_new_weights = new_weights[question.code]

            for weight in self.db.session.query(Weight).filter(Weight.question_id == question.id, Weight.variable.in_(current_new_weights.keys())).all():
                # Only merge options which already exist in the database
                update_weight = current_new_weights.pop(weight.variable)
                update_weight['id'] = weight.id

                if not is_same_db_data(weight, update_weight):
                    self.db.session.merge(Weight(**update_weight))

            # Only add those options which did not exist in the database
            def map_items(key):
                item = current_new_weights[key]
                item["variable"] = key
                item["question_id"] = question.id
                return Weight(**item)

            current_new_weights_keys = current_new_weights.keys()
            if current_new_weights_keys:
                insert_weights = list(
                    map(map_items, current_new_weights_keys))
                self.db.session.add_all(insert_weights)
                print("Add %s weights" % str(len(insert_weights)))
            self.db.session.commit()
