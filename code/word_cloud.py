import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

tip = pd.read_pickle("data/tip.pkl")

text = tip["text"].tolist()

comment_words = ''
# "tacos","taco","good","great","food","best","amazing","place","service",
#"love","delicious","awesome","excellent","try","always","go","drink","order","back","will"

stopwords = set(list(STOPWORDS)+["tacos","taco","food","margarita","burrito","one","really","try","good","great","best","amazing","love","delicious",
                                 "place","awesome","excellent","always","go",".drinks","order","back","will"])

for val in text:
     
    # typecaste each val to string
    val = str(val)
 
    # split the value
    tokens = val.split()
     
    # Converts each token into lowercase
    for i in range(len(tokens)):
        tokens[i] = tokens[i].lower()
     
    comment_words += " ".join(tokens)+" "
 
wordcloud = WordCloud(width = 1600, height = 800,
                background_color ='white',
                stopwords = stopwords,
                min_font_size = 10).generate(comment_words)
 
# plot the WordCloud image                      
plt.figure(figsize = (8, 4), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)
plt.savefig("wordcloud.png",dpi=600)

plt.show()