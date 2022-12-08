from tqdm import tqdm
import pandas as pd
import numpy as np
import json


raw_review = pd.read_pickle("../data/raw_review.pkl")
with open("../data/normalized_stars.npy", "rb") as f:
    stars = np.load(f)

adj_list = [
    'bad', 'worst', 'fresh', 'ridiculous', 'nice',
    'yummy', 'wonderful', 'awful', 'good', 'great',
    'rude', 'friendly', 'helpful', 'welcoming',
    'fast', 'clean', 'warm', 'dirty'
]
adj_map = dict(zip(adj_list, [0] * len(adj_list)))
for adj in adj_list:
    condition = raw_review.text.str.contains(adj, case=False)
    adj_map[adj] = stars[condition.values].mean() - 3
all_n = {
    "dish": [
        "shrimp", "rib", "beef", "fish",
        "chicken", "peach", "carne asada", "tortilla"
    ],
    "sauce": [
        "salsa", "guacamole", "chipotle", "nacho cheese", "green sauce"
    ],
    "service": ["service", "waiter"],
    "enviroment": ["view", "environment", "atmosphere", "ambiance"]
}
cat_map = dict(zip(all_n.keys(), [0] * 4))
n_map = {cat: {n: 0 for n in all_n[cat]} for cat in all_n}
for cat in cat_map.keys():
    tmp = 0
    for n in tqdm(all_n[cat]):
        con_n = raw_review.text.str.contains(n, case=False)
        df_tmp = raw_review.text[con_n]
        stars_tmp = stars[con_n.values]
        n_score = stars_tmp.mean() - 3
        cum = 0
        for adj in adj_list:
            w = adj + " " + n
            con_adj = df_tmp.str.contains(w, case=False)
            if stars_tmp[con_adj].shape[0] == 0:
                continue
            cum += adj_map[adj] * stars_tmp[con_adj].mean()
        n_map[cat][n] = cum / stars_tmp.shape[0]
        tmp += n_map[cat][n]
    cat_map[cat] = tmp / len(all_n[cat])

with open("Adjectives.json", "w") as outfile:
    json.dump(adj_map, outfile)
with open("Noun.json", "w") as outfile:
    json.dump(n_map, outfile)
with open("Category.json", "w") as outfile:
    json.dump(cat_map, outfile)
