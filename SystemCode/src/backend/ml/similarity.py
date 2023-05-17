import pandas as pd
from sentence_transformers import SentenceTransformer
from scipy import spatial
from pathlib import Path

# Load task word embeddings
path = Path(__file__).parent / 'task_embeddings.pkl'
embeddings_df = pd.read_pickle(path)

# Load model
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
# model_path = str(Path(__file__).parent) + '/model'
# model = SentenceTransformer(model_path)


class SimilarityCalculator():
    def __init__(self, occupations, interest_input, experience_input, context_input, salary_input, priority='interest_open'):
        self.occupations = occupations
        self.interest_input = interest_input
        self.experience_input = experience_input
        self.context_input = context_input
        self.salary_input = salary_input

        self.priority_weights = {
            'interest': 0.4,
            'experience': 0.8
        } if priority == 'experience_open' else {
            'interest': 0.8,
            'experience': 0.4
        }
        self.build_jobs_df()

    def build_jobs_df(self):
        # Build an occupations dataframe from `occupations` database table
        jobs_df = pd.DataFrame.from_dict(self.occupations, orient='index')
        # Merge sentence embeddings
        jobs_df = jobs_df.merge(
            embeddings_df,
            on="id", suffixes=("_df1", "_df2"), how="inner")

        self.jobs_df = jobs_df

    def calc_cosine_similarity(self, input, column_name='similarity'):
        data = self.jobs_df.copy()
        input_vector = model.encode(input)
        data[column_name] = data['embeddings'].apply(
            lambda x: 1 - spatial.distance.cosine(x, input_vector))
        return data[['id', column_name]]

    def calc_euclidean_similarity(self, input_vector, column_name='similarity'):
        data = self.jobs_df.copy()
        columns = input_vector.keys()
        values = input_vector.values()

        def calc_distance(x):
            if x.isnull().any():
                return 0
            return 1 / (1 + spatial.distance.euclidean(list(values), x))

        data[column_name] = data[columns].agg(calc_distance, axis=1)
        return data[['id', column_name]]

    def calc_salary_penalty(self, value, input):
        if value and input:
            # z = adjusted by Standard Deviations
            diff = (value - input) / 730.0

            if diff > 0:
                return 0
            elif diff < -1:
                return -1
            else:
                return diff
        else:
            return 0

    def calc_salary_penalties(self, input, column_name='similarity'):
        data = self.jobs_df.copy()
        data[column_name] = data['min_salary'].apply(
            lambda x: self.calc_salary_penalty(x, input))
        return data[['id', column_name]]

    def get_all_similar(self):
        context_similarity = self.calc_euclidean_similarity(
            self.context_input, 'context_similarity')
        interest_similarity = self.calc_cosine_similarity(
            self.interest_input, 'interest_similarity')
        experience_similarity = self.calc_cosine_similarity(
            self.experience_input, 'experience_similarity')
        salary_similarity = self.calc_salary_penalties(
            self.salary_input, 'salary_similarity')

        return interest_similarity, experience_similarity, context_similarity, salary_similarity

    def aggregate_similarity(self, row):
        return 0.1 * row['context_similarity'] + 0.1 * row['salary_similarity'] + self.priority_weights['interest'] * row['interest_similarity'] + self.priority_weights['experience'] * row['experience_similarity']

    def get_recommendation(self, n=30, as_dict=True):
        interest_similarity, experience_similarity, context_similarity, salary_similarity = self.get_all_similar()
        merge_df = interest_similarity.merge(
            experience_similarity.merge(context_similarity, on='id'), on='id').merge(salary_similarity, on='id').set_index('id')
        merge_df['score'] = merge_df[['context_similarity', 'interest_similarity',
                                      'experience_similarity', 'salary_similarity']].agg(self.aggregate_similarity, axis=1)
        merge_df = merge_df.sort_values('score', ascending=False)
        merge_df = merge_df.rename(index={"id": "occupation_id"})
        return merge_df[:n].to_dict(orient='index', index=True) if as_dict else merge_df[:n]
