import matplotlib.pyplot as plt
import pandas as pd
import math

df = pd.read_pickle("data/raw_review.pkl")

target = {
    "Sanity Check": [
        "bad", "worst", "fresh", "ridiculous", "nice",
        "yummy", "wonderful", "awful",
    ],
    "Dishes": [
        "shrimp", "rib", "beef",
        "peach", "chicken", "fish", "carne asada", "tortilla",
    ],
    "Sauce": [
        "salsa", "guacamole", "chipotle",
        "nacho cheese", "green sauce", 
    ],
    "Terms Associated with Ambiance Matters": [
        "not crowded", "warm", "clean",
        "atmosphere", "ambiance",
    ],
    "Service": [
        "rude", "friendly", "helpful", "welcoming"
    ]
}
stars = pd.get_dummies(df.stars).reindex(range(1, 6), axis=1)
xticks = ["1", "2", "3", "4", "5"]
for k in target.keys():
    k_val = target[k]
    ncols = 3
    nrows = math.ceil(len(k_val) / ncols)
    fig, axs = plt.subplots(
        nrows, ncols,
        figsize=(4 * ncols, 3 * nrows),
        sharey=False,
    )
    fig.suptitle(k, size=20)
    for idx, name in enumerate(k_val):
        i, j = idx // ncols, idx % ncols
        tmp = stars[df.text.str.contains(name, regex=False)].sum(0)
        axs[i][j].set_title(name)
        axs[i][j].bar(x=xticks, height=tmp.values / stars.sum().values)
        axs[i][j].set_xticks(xticks)
        axs[i][j].set_ylim(0, 1.2* max(tmp.values / stars.sum().values))
        axs[i][j].set_ylabel("Word Freq")
    for idx in range(len(k_val), (((len(k_val) - 1) // ncols + 1) * ncols)):
        i, j = idx // ncols, idx % ncols
        axs[i][j].remove()
    fig.tight_layout()
    plt.savefig("pic/ALL/"+k+".png", dpi=100)
    plt.close()

from scipy.stats import chisquare

#chi-square test
test = pd.DataFrame()
l_name = []
l_p = []
for k in target.keys():
    k_val = target[k]
    for idx, name in enumerate(k_val):
        i, j = idx // ncols, idx % ncols
        tmp = stars[CA.text.str.contains(name, regex=False)].sum(0)
        word_freq = tmp.values
        star_freq = stars.sum().values/stars.sum().values.sum()*tmp.values.sum()
        stat, p = chisquare(f_obs=word_freq.tolist(), f_exp=star_freq.tolist())
        l_name += [name]
        l_p += [p]
test["name"] = l_name
test["p_value"] = l_p
