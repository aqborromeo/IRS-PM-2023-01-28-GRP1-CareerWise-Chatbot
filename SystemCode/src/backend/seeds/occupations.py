from flask_seeder import Seeder
from sqlalchemy import insert
import json
from app.models.occupation import Occupation
from pathlib import Path

from app.utils.common import is_same_db_data

base_path = Path(__file__).parent
file_path = (base_path / "./data/occupations.json").resolve()
salaries_file_path = (base_path / "./data/onet_salaries.json").resolve()


class OccupationSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 4

    # run() will be called by Flask-Seeder
    def run(self):
        file = open(file_path)
        salaries_file = open(salaries_file_path)

        data = json.load(file)
        salaries_data = json.load(salaries_file)

        for each in Occupation.query.filter(Occupation.id.in_(data.keys())).all():
            # Only merge those posts which already exist in the database
            update_item = data.pop(each.id)
            salaries_item = salaries_data[each.id] if each.id in salaries_data else {
            }

            update_item = {**update_item, **salaries_item}
            update_item['id'] = each.id

            if not is_same_db_data(each, update_item):
                self.db.session.merge(Occupation(**update_item))
                print("Update occupation: %s" % each.id)

        # Only add those posts which did not exist in the database
        if data.keys():
            def map_id(key):
                item = data[key]
                item['id'] = key
                return item

            insert_items = list(
                map(map_id, data.keys()))
            self.db.session.execute(insert(Occupation), insert_items)
            print("Add %s occupations" % str(len(insert_items)))

        # Now we commit our modifications (merges) and inserts (adds) to the database!
        self.db.session.commit()
