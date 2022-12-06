import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.linear_model import Lasso


def stepwise_selection(
    X,
    y,
    threshold_in=0.05,
    threshold_out = 0.05,
):
    selected, columns = set(), set(X.columns)
    while True:
        Flag = False # record whether the current iteration should stop
        non_selected = columns.difference(selected)
        new_pval = pd.Series(index=non_selected, dtype="float64")
        for col in non_selected:
            tmp_X = sm.add_constant(X[list(selected) + [col]])
            model = sm.OLS(y, tmp_X).fit()
            new_pval[col] = model.pvalues[col]
        best_pval = new_pval.min()
        if best_pval < threshold_in:
            # Use F test to add significant feature
            best_fea = new_pval.idxmin()
            selected.add(best_fea)
            Flag = True
            print(f"Add {best_fea:10} with p-value {best_pval:.6}")
        model = sm.OLS(y, sm.add_constant(X[list(selected)])).fit()
        pvalues = model.pvalues.iloc[1:] # drop const coef
        worst_pval = pvalues.max() 
        if worst_pval > threshold_out:
            # Use t test to drop non-significant feature
            worst_fea = pvalues.idxmax()
            selected.remove(worst_fea)
            Flag = True
            print(f"Drop {worst_fea:10} with p-value {worst_pval:.6}")
        if not Flag:
            break
    return selected

df = pd.read_csv("../data/feature.csv")
X, y = df.iloc[:, :-1], df.stars # (916, 110)

print("[Start] Selection with Stepwise Regression...")
selected = stepwise_selection(X, y) # (16,)
print(f"The final selected features are {selected}.\n")
