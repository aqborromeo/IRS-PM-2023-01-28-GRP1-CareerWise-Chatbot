from flask_seeder import Seeder
from sqlalchemy import delete
import json
from app.models.career_path import CareerPath
from app.utils.common import is_same_db_data
from pathlib import Path

base_path = Path(__file__).parent
file_path = (base_path / "./career_paths.json").resolve()


class CareerPathSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 5

    # run() will be called by Flask-Seeder
    def run(self):
        file = open(file_path)

        data = json.load(file)

        data_ids = data.keys()

        for each in CareerPath.query.filter(CareerPath.id.in_(data_ids)).all():
            # Only merge those items which already exist in the database
            update_item = data.pop(each.id)
            if not is_same_db_data(each, update_item):
                self.db.session.merge(CareerPath(**update_item))
                print("Update career path: %s" % each.id)

        # Only add those items which did not exist in the database
        if data_ids:
            insert_items = list(
                map(lambda item: CareerPath(**item), data.values()))
            self.db.session.add_all(insert_items)
            print("Add %s career paths" % str(len(insert_items)))

            # Purge non-existent items
            delete_statement = delete(CareerPath).where(
                CareerPath.id.not_in(data_ids))
            self.db.session.execute(delete_statement)

        # Now we commit our modifications (merges) and inserts (adds) to the database!
        self.db.session.commit()
