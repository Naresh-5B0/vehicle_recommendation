from sklearn.neighbors import NearestNeighbors
import pandas as pd

class VehicleRecommender:
    def __init__(self, data):
        self.data = data
        self.model = NearestNeighbors(n_neighbors=5, metric="euclidean")
        self.model.fit(data)

    def recommend(self, user_input):
        user_df = pd.DataFrame([user_input])
        user_df = user_df.reindex(columns=self.data.columns, fill_value=0)
        _, indices = self.model.kneighbors(user_df)
        return indices[0]
