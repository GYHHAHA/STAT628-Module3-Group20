import pandas as pd
import numpy as np


raw_review = pd.read_pickle("../data/raw_review.pkl")
df_business = pd.read_pickle("../data/business.pkl")
df_review = pd.read_pickle("../data/review.pkl")

cat_map = {
    0:[3],
    1: [3],
    2: [2, 4],
    3: [2, 3, 4],
    4: [2, 3, 4, 5],
}

def transform_func(x):
    res = pd.qcut(x, q_space, duplicates="drop")
    n_cat = res.cat.categories.shape[0]
    if n_cat == 5:
        return res.cat.codes + 1
    elif n_cat == 0:
        return res.astype("float").fillna(4).astype("int")
    else:
        new_cat = cat_map[n_cat]
        return res.cat.set_categories(
            new_cat, ordered=True, rename=True
        ).values

q_space = np.linspace(0, 1, 5)
condition = df_review.user_id.isin(raw_review.user_id.unique())
sub_review = df_review[condition]
grouper_trans = sub_review.groupby("user_id")["stars"].transform
sub_review = pd.DataFrame(
    {
        "review_id": sub_review.review_id,
        "stars": grouper_trans(transform_func),
    }
)

new_stars = raw_review.merge(
    sub_review.rename(columns={"stars": "new_stars"}),
    how="left", on="review_id",
).new_stars.values
with open("data/normalized_stars.npy", "wb") as f:
    np.save(f, new_stars.astype("int"))
