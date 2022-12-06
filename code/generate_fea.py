from generate_map import attr_map
import pandas as pd


df = pd.read_pickle("../data/raw_business.pkl")
cats = pd.concat(
    [
        pd.Series(
            df.categories.str.contains(c, regex=False),
            name="[CAT] " + c).astype("float64")
        for c in df.categories.str.split(", ").explode().unique()
    ],
    axis=1,
)
attrs = pd.concat(
    [
        pd.Series(
            df.attributes.str[a].replace(attr_map[a]),
            name="[ATTR] " + a)
        for a in attr_map.keys()
    ],
    axis=1,
)

def get_day_delta(day):
    s = df.hours.str[day].fillna("0:0-0:0").str.split("-")
    t1 = pd.to_timedelta(s.str[0]+":00") 
    t2 = pd.to_timedelta(s.str[1]+":00")
    t2 = t2.mask(t2 <= t1, t2 + pd.Timedelta("24 Hours"))
    delta = (t2 - t1).dt.total_seconds() / 3600
    delta = delta.mask(df.hours.str[day].isna())
    return delta

def get_all_day_delta():
    res = 0
    for d in list(df.hours[0].keys()):
        res += get_day_delta(d)
    return res

time_fea = pd.concat(
    [
        pd.Series(
            (df.hours.str["Sunday"].isna()
            | df.hours.str["Saturday"].isna()).astype("int"),
            name="[TIME] Weekends"
        ),
        pd.Series(
            get_all_day_delta().values,
            name="[TIME] Total Time"
        ),
    ],
    axis=1,
)

res = pd.concat([cats, attrs, time_fea, pd.Series(df.stars)], axis=1)
res = res.apply(lambda x: x.fillna(x.mode().iloc[0]))
res.to_csv("../data/feature.csv", index=False)
