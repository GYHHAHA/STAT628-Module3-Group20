import pandas as pd


df_business = pd.read_pickle("../data/business.pkl")
df_review = pd.read_pickle("../data/review.pkl")

condition = df_business.name.fillna("").str.contains("Taco", case=False)
new_business = df_business[condition].reset_index(drop=True)

condition = df_review.business_id.isin(new_business.business_id)
new_review = df_review[condition].reset_index(drop=True)

new_business.to_pickle("../data/raw_business.pkl")
new_review.to_pickle("../data/raw_review.pkl")
