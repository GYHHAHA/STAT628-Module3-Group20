import pandas as pd
import statsmodels.api as sm


features = [
    '[CAT] Italian',
    '[TIME] Total Time',
    '[CAT] Tex-Mex',
    '[CAT] Japanese',
    '[CAT] Hardware Stores',
    '[CAT] Home & Garden',
    '[ATTR] Alcohol',
    '[CAT] Fast Food',
    '[CAT] Local Flavor',
    '[CAT] Puerto Rican',
    '[CAT] Food Stands',
    '[ATTR] BusinessAcceptsCreditCards',
    '[CAT] Arts & Entertainment',
    '[CAT] Food Trucks', 
    '[CAT] Tacos',
    '[ATTR] DriveThru'
]

df = pd.read_csv("../data/feature.csv")
X, y = df[features], df.stars
est = sm.OLS(y, sm.add_constant(X)).fit()
with open("../data/ols_result.txt", "w") as f:
    f.write(est.summary().as_text() + "\n")
