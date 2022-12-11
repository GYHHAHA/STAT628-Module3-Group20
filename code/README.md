# Code

Codes should be run by the following order:

```
1. generate_raw.py
2. generate_fea.py
3. feature_select.py
4. linear_fitting.py
5. normalize_star.py
6. score_compute.py
```

Code for linear regression analysis can be run within a Rmd file: 
```
lm_business_data.Rmd (load data after one-hot encoding; impute missing value with mode; run all subsets regression; fit linear model; model diagnostics)
require packages: 
library(tidyverse)
library(dplyr)
library(ggplot2)
library(MASS)
library(stats)
library(leaps)
library(missMethods)
library(regclass)
```
