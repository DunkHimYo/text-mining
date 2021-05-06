import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from konlpy.tag import Okt
from apyori import apriori
from textblob import TextBlob
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import re
from  numba import jit
import seaborn as sns

sns.set_style("darkgrid", {'font.family':'Malgun Gothic',"axes.facecolor": ".40"})
def to_noun(title_list_page,slice_index):
    stemmer = SnowballStemmer('english')
    stop_words = set(stopwords.words('english'))
    all_title=np.concatenate(title_list_page[slice_index])
    okt = Okt()
    
    noun_buffer=[]
    for i in all_title:
        token = okt.nouns(i)
        blob = TextBlob(i)
        if len(token)>0:
            if len(blob)>0:
                n=WordNetLemmatizer()
                word=[n.lemmatize(w) for w in blob.words]
                result = [stemmer.stem(i).upper() for i in word if i not in stop_words]
                s=' '.join(result)
                eng_noun=re.findall('[a-zA-Z]+',s)
                eng_noun=[i for i in eng_noun if len(i)>1]
            kor_noun=[i for i in token if len(i)>1]

            kor_noun.extend(eng_noun)
            noun_buffer.append(kor_noun)  
        else:
            noun_buffer.append('')
    return noun_buffer


noun_title=to_noun(all_title,slice(0,len(all_title)))

token=np.hstack(noun_title)
frq_token = FreqDist(token)

noun = pd.DataFrame(data=np.array([list(frq_token.keys()), list(frq_token.values())]).T, columns=['word', 'n'])
noun.n = noun.n.astype('int')
noun = noun.sort_values(by='n', ascending=False)
print(noun)
noun=noun[noun.word.str.len()>1]
plt.figure(figsize=(10,10))
sns.barplot(data=noun[:30], x='n', y='word')
plt.show()
