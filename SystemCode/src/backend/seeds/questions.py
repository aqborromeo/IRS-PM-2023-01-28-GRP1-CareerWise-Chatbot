from flask_seeder import Seeder, generator
from sqlalchemy import delete
from app.models.question import Question
from app.utils.common import is_same_db_data


class QuestionSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 1

    # run() will be called by Flask-Seeder
    def run(self):
        new_questions = {
            # Work Style
            "style_stress_tolerance": {
                "order": 10,
                "group": "style",
                "code": "style_stress_tolerance",
                "text": 'How high is your <b>stress tolerance</b>?'
            }, "style_achievement_effort": {
                "order": 20,
                "group": "style",
                "code": "style_achievement_effort",
                "text": 'Is it important for you to <b>work hard to achieve a goal</b>?'
            }, "style_social_orientation": {
                "order": 30,
                "group": "style",
                "code": "style_social_orientation",
                "text": 'Is it important for you to be able to form <b>social connection with others</b>?'
            }, "style_independence": {
                "order": 40,
                "group": "style",
                "code": "style_independence",
                "text": 'Is it important for you to be allowed to <b>work independently</b>?'
            }, "style_innovation": {
                "order": 50,
                "group": "style",
                "code": "style_innovation",
                "text": 'Is it important for you to be allowed to <b>innovate and try new ways</b> to do a job?'
            },

            # Work Context
            "context_duration_of_typical_work_week": {
                "order": 60,
                "group": "context",
                "code": "context_duration_of_typical_work_week",
                "text": 'How many <b>hours</b> do you expect to <b>work in a week</b>?'
            }, "context_outdoors_exposed_to_weather": {
                "order": 70,
                "group": "context",
                "code": "context_outdoors_exposed_to_weather",
                "text": 'How often are you willing to <b>work outdoors, exposed to the weather</b>?'
            }, "context_spend_time_walking_and_running": {
                "order": 80,
                "group": "context",
                "code": "context_spend_time_walking_and_running",
                "text": 'How often are you willing to spend time doing <b>physical activities</b> (e.g. running, walking)?'
            }, "context_deal_with_unpleasant_or_angry_people": {
                "order": 90,
                "group": "context",
                "code": "context_deal_with_unpleasant_or_angry_people",
                "text": 'How often are you willing to deal with <b>unpleasant, angry, or discourteous people</b>?'
            }, "context_exposed_to_hazardous_conditions": {
                "order": 100,
                "group": "context",
                "code": "context_exposed_to_hazardous_conditions",
                "text": 'How often are you willing to expose yourself to <b>hazardous conditions</b>?'
            },

            # Salary
            "salary_minimum": {
                "order": 110,
                "group": "salary",
                "code": "salary_minimum",
                "text": 'What is your <b>minimum expected monthly salary</b> as someone new to a job?',
                "min_response_length": 1
            }, "salary_ideal": {
                "order": 120,
                "group": "salary",
                "code": "salary_ideal",
                "text": 'What is your <b>ideal monthly salary</b> as someone new to a job?',
                "min_response_length": 1
            },

            # Education
            "education_level": {
                "order": 200,
                "group": "education",
                "code": "education_level",
                "text": 'What is your current <b>level of education</b>?'
            },
            "education_subject": {
                "order": 210,
                "group": "education",
                "code": "education_subject",
                "text": 'What <b>subjects or fields</b> are you good at?',
                "min_response_length": 1
            },

            # Open-ended
            "interest_open": {
                "order": 1,
                "group": "interest",
                "code": "interest_open",
                "text": 'Describe in detail what you would like to do for a living.',
                "min_response_length": 200
            },
            "experience_open": {
                "order": 2,
                "group": "experience",
                "code": "experience_open",
                "text": 'Describe your past work experience. <br>(If you''re studying, you can talk about your extra-curricular activities)',
                "min_response_length": 200
            },

            # Priority
            "priority": {
                "order": 400,
                "group": "priority",
                "code": "priority",
                "text": 'Which of the following is most important to you when choosing a career path?'
            }
        }

        original_new_questions = new_questions.copy()

        for each in Question.query.filter(Question.code.in_(new_questions.keys())).all():
            # Only merge those posts which already exist in the database
            update_question = new_questions.pop(each.code)
            update_question['id'] = each.id

            if not is_same_db_data(each, update_question):
                self.db.session.merge(Question(**update_question))
                print(f"Update question: {update_question['code']}")

        # Only add those posts which did not exist in the database
        new_questions_values = new_questions.values()

        if new_questions_values:
            insert_questions = list(
                map(lambda item: Question(**item), new_questions_values))
            self.db.session.add_all(insert_questions)
            print("Add %s questions" % str(len(new_questions_values)))

        # Now we commit our modifications (merges) and inserts (adds) to the database!
        self.db.session.commit()

        # Purge non-existent items
        data_codes = original_new_questions.keys()
        delete_statement = delete(Question).where(
            Question.code.not_in(data_codes))
        self.db.session.execute(delete_statement)

        self.db.session.commit()
