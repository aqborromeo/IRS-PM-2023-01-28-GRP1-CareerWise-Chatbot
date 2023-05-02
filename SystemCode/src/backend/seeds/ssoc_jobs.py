from flask_seeder import Seeder
from sqlalchemy import delete
import json
from app.models.ssoc_job import SsocJob
from app.utils.common import is_same_db_data
from pathlib import Path

base_path = Path(__file__).parent
file_path = (base_path / "./data/ssoc_jobs.json").resolve()


class SsocJobSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 6
        self.label = 'SSOC jobs'
        self.Model = SsocJob

    # run() will be called by Flask-Seeder
    def run(self):
        file = open(file_path)

        data = json.load(file)

        data_ids = data.keys()

        for each in SsocJob.query.filter(self.Model.id.in_(data_ids)).all():
            # Only merge those items which already exist in the database
            update_item = data.pop(each.id)
            if not is_same_db_data(each, update_item):
                self.db.session.merge(self.Model(**update_item))
                print(f"Update {self.label}: {each.id}")

        # Only add those items which did not exist in the database
        if data_ids:
            insert_items = list(
                map(lambda item: self.Model(**item), data.values()))
            self.db.session.add_all(insert_items)
            print(f"Add {str(len(insert_items))} {self.label}")

            # Purge non-existent items
            delete_statement = delete(self.Model).where(
                self.Model.id.not_in(data_ids))
            self.db.session.execute(delete_statement)

        # Now we commit our modifications (merges) and inserts (adds) to the database!
        self.db.session.commit()
